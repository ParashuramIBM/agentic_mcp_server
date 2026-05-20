import aiohttp
import json
from typing import Dict, List, Any, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)

class FreeLLMService:
    def __init__(self, config):
        self.config = config
        self.provider = config.llm_provider
        
    async def analyze_failure(self, prompt: str) -> Dict[str, Any]:
        """Analyze pipeline failure using free LLM"""
        if self.provider == "ollama":
            return await self._call_ollama(prompt)
        elif self.provider == "huggingface":
            return await self._call_huggingface(prompt)
        elif self.provider == "gemini":
            return await self._call_gemini(prompt)
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")
    
    async def _call_ollama(self, prompt: str) -> Dict[str, Any]:
        """Call local Ollama instance (completely free)"""
        url = f"{self.config.ollama_base_url}/api/generate"
        
        # System prompt for CI/CD analysis
        system_prompt = """You are a CI/CD pipeline expert. Analyze the failure and provide:
1. Root cause analysis
2. Severity (low/medium/high)
3. Suggested fix with specific code changes
4. Risk assessment
        
Format your response as JSON with keys: root_cause, severity, suggested_fix, risk_assessment"""
        
        full_prompt = f"{system_prompt}\n\nPipeline failure details:\n{prompt}"
        
        payload = {
            "model": self.config.ollama_model,
            "prompt": full_prompt,
            "stream": False,
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        response_text = result.get("response", "")
                        return self._parse_llm_response(response_text)
                    else:
                        logger.error(f"Ollama API error: {resp.status}")
                        return self._get_fallback_response()
        except Exception as e:
            logger.error(f"Ollama request failed: {str(e)}")
            return self._get_fallback_response()
    
    async def _call_huggingface(self, prompt: str) -> Dict[str, Any]:
        """Call Hugging Face Inference API (free tier)"""
        api_url = f"https://api-inference.huggingface.co/models/{self.config.huggingface_model}"
        headers = {
            "Authorization": f"Bearer {self.config.huggingface_api_key}"
        }
        
        # Simplified prompt for code models
        payload = {
            "inputs": f"Analyze this CI/CD pipeline failure and suggest a fix:\n{prompt}\n\nProvide: root cause, severity (low/medium/high), suggested fix, risk assessment.",
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.3,
                "return_full_text": False
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        # Hugging Face returns list of generated text
                        if isinstance(result, list) and len(result) > 0:
                            response_text = result[0].get("generated_text", "")
                        else:
                            response_text = str(result)
                        return self._parse_llm_response(response_text)
                    else:
                        logger.error(f"HuggingFace API error: {resp.status}")
                        return self._get_fallback_response()
        except Exception as e:
            logger.error(f"HuggingFace request failed: {str(e)}")
            return self._get_fallback_response()
    
    async def _call_gemini(self, prompt: str) -> Dict[str, Any]:
        """Call Google Gemini API (free tier)"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.gemini_model}:generateContent?key={self.config.gemini_api_key}"
        
        # System instruction for Gemini
        system_instruction = "You are a CI/CD pipeline expert. Analyze failures and provide structured responses with root cause, severity, suggested fix, and risk assessment."
        
        payload = {
            "system_instruction": {
                "parts": [{"text": system_instruction}]
            },
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 1000,
                "topP": 0.95
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        # Extract text from Gemini response
                        if "candidates" in result and len(result["candidates"]) > 0:
                            response_text = result["candidates"][0]["content"]["parts"][0]["text"]
                        else:
                            response_text = str(result)
                        return self._parse_llm_response(response_text)
                    else:
                        logger.error(f"Gemini API error: {resp.status}")
                        return self._get_fallback_response()
        except Exception as e:
            logger.error(f"Gemini request failed: {str(e)}")
            return self._get_fallback_response()
    
    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response into structured format"""
        # Try to parse as JSON first
        try:
            # Look for JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback to text parsing
        response_lower = response_text.lower()
        
        # Extract severity
        if "high" in response_lower:
            severity = "high"
        elif "medium" in response_lower:
            severity = "medium"
        else:
            severity = "low"
        
        # Extract sections
        sections = {
            "root_cause": self._extract_section(response_text, "root cause"),
            "suggested_fix": self._extract_section(response_text, "suggested fix"),
            "risk_assessment": self._extract_section(response_text, "risk assessment")
        }
        
        return {
            "raw_analysis": response_text,
            "severity": severity,
            "suggested_fix": sections["suggested_fix"] or "Manual review required",
            "root_cause": sections["root_cause"] or "Unable to determine",
            "risk_assessment": sections["risk_assessment"] or "Unknown risk"
        }
    
    def _extract_section(self, text: str, section_name: str) -> Optional[str]:
        """Extract a section from the response text"""
        import re
        patterns = [
            rf'{section_name}[\s:]+(.+?)(?=\n\n|\n[A-Z]|$)',
            rf'{section_name}[\s:]+(.+?)(?=\n\n|\n[A-Z]|$)',
            rf'{section_name}:(.+?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        return None
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Return fallback response when LLM is unavailable"""
        return {
            "raw_analysis": "LLM service unavailable. Manual inspection required.",
            "severity": "medium",
            "suggested_fix": "Please review logs manually and investigate the failure.",
            "root_cause": "Unable to determine automatically",
            "risk_assessment": "Manual review needed"
        }

    async def generate_patch(self, analysis: Dict, file_content: str) -> Optional[str]:
        """Generate a code patch based on analysis"""
        prompt = f"""
Based on this analysis: {analysis.get('suggested_fix', '')}

Original code:
```python
{file_content[:2000]}