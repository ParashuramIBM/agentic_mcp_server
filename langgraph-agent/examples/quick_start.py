#!/usr/bin/env python3
"""
Quick Start Script - Test the LangGraph DevOps Agent

This script demonstrates basic usage of the agent and helps verify your setup.

Usage:
    export AGENTIC_STUDIO_API_KEY="your-api-key"
    python quick_start.py
"""

import os
import sys
from agent_client import AgentClient, AgentResponse


def print_header(text: str):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_result(result: AgentResponse):
    """Print agent response in a formatted way"""
    print(f"\n✅ Status: {result.status}")
    print(f"📊 Confidence: {result.confidence_score:.2%}")
    print(f"🆔 Request ID: {result.request_id}")
    
    if result.error:
        print(f"❌ Error: {result.error}")
        return
    
    print(f"\n📝 Response:")
    print(result.message[:200] + "..." if len(result.message) > 200 else result.message)
    
    if result.artifacts:
        print(f"\n📦 Artifacts Generated:")
        for name in result.artifacts.keys():
            print(f"   - {name}")
    
    if result.metadata:
        print(f"\n⚙️  Metadata:")
        if "processing_time_ms" in result.metadata:
            print(f"   - Processing time: {result.metadata['processing_time_ms']}ms")
        if "tokens_used" in result.metadata:
            print(f"   - Tokens used: {result.metadata['tokens_used']}")
        if "model" in result.metadata:
            print(f"   - Model: {result.metadata['model']}")


def check_api_key():
    """Check if API key is set"""
    api_key = os.getenv("AGENTIC_STUDIO_API_KEY")
    if not api_key:
        print("❌ Error: AGENTIC_STUDIO_API_KEY environment variable not set")
        print("\nTo get your API key:")
        print("1. Visit: https://agentstudio.servicesessentials.ibm.com/settings")
        print("2. Navigate to 'API Keys' section")
        print("3. Click 'Generate New API Key'")
        print("4. Copy the key and set it:")
        print("   export AGENTIC_STUDIO_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    print(f"✅ API key found: {api_key[:10]}...{api_key[-10:]}")
    return api_key


def test_agent_card(client: AgentClient):
    """Test getting agent card"""
    print_header("Test 1: Get Agent Card (Discovery)")
    
    try:
        card = client.get_agent_card()
        print(f"\n✅ Agent: {card.get('name', 'N/A')}")
        print(f"📌 Version: {card.get('version', 'N/A')}")
        print(f"🔧 Framework: {card.get('framework', 'N/A')}")
        print(f"🤖 Model: {card.get('model', 'N/A')}")
        print(f"🎯 Pattern: {card.get('pattern', 'N/A')}")
        
        capabilities = card.get('capabilities', [])
        if capabilities:
            print(f"\n💪 Capabilities:")
            for cap in capabilities:
                print(f"   - {cap}")
        
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_create_dockerfile(client: AgentClient):
    """Test creating a Dockerfile"""
    print_header("Test 2: Create Dockerfile")
    
    print("\n📋 Request: Create a production-ready Dockerfile for Python FastAPI")
    
    try:
        result = client.create_dockerfile(
            language="python",
            framework="fastapi",
            environment="production",
            features=["multi-stage", "security-hardened"]
        )
        
        print_result(result)
        
        # Show a snippet of the Dockerfile
        if "dockerfile" in result.artifacts:
            dockerfile = result.artifacts["dockerfile"]
            all_lines = dockerfile.split('\n')
            preview_lines = all_lines[:10]
            print(f"\n📄 Dockerfile Preview (first 10 lines):")
            for line in preview_lines:
                print(f"   {line}")
            if len(all_lines) > 10:
                remaining = len(all_lines) - 10
                print(f"   ... ({remaining} more lines)")
        
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_create_k8s_manifests(client: AgentClient):
    """Test creating Kubernetes manifests"""
    print_header("Test 3: Create Kubernetes Manifests")
    
    print("\n📋 Request: Generate Kubernetes deployment and service for my-app")
    
    try:
        result = client.create_kubernetes_manifests(
            app_name="my-app",
            environment="production",
            replicas=3,
            port=8000
        )
        
        print_result(result)
        
        # Show manifest names
        if result.artifacts:
            print(f"\n📄 Generated Manifests:")
            for name, content in result.artifacts.items():
                lines = len(content.split('\n'))
                print(f"   - {name} ({lines} lines)")
        
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_create_cicd_pipeline(client: AgentClient):
    """Test creating CI/CD pipeline"""
    print_header("Test 4: Create CI/CD Pipeline")
    
    print("\n📋 Request: Create GitHub Actions pipeline with testing and deployment")
    
    try:
        result = client.create_cicd_pipeline(
            provider="github",
            language="python",
            stages=["test", "security-scan", "build", "deploy"]
        )
        
        print_result(result)
        
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_custom_request(client: AgentClient):
    """Test a custom request"""
    print_header("Test 5: Custom Request")
    
    print("\n📋 Request: Create a docker-compose.yml for a Python FastAPI app with PostgreSQL")
    
    try:
        result = client.invoke(
            message="Create a docker-compose.yml for a Python FastAPI application with PostgreSQL database",
            context={
                "language": "python",
                "framework": "fastapi",
                "database": "postgresql"
            }
        )
        
        print_result(result)
        
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def main():
    """Main function"""
    print_header("🚀 LangGraph DevOps Agent - Quick Start")
    
    print("\nThis script will test the deployed agent with various requests.")
    print("Make sure you have set your AGENTIC_STUDIO_API_KEY environment variable.")
    
    # Check API key
    check_api_key()
    
    # Initialize client
    print("\n🔧 Initializing agent client...")
    try:
        client = AgentClient()
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Agent Card", test_agent_card),
        ("Create Dockerfile", test_create_dockerfile),
        ("Create K8s Manifests", test_create_k8s_manifests),
        ("Create CI/CD Pipeline", test_create_cicd_pipeline),
        ("Custom Request", test_custom_request)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func(client)
            results.append((name, success))
        except KeyboardInterrupt:
            print("\n\n⚠️  Tests interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print_header("📊 Test Summary")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    print("\n📋 Results:")
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {name}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your agent is working correctly.")
        print("\n📚 Next steps:")
        print("   1. Check out examples/README.md for more usage patterns")
        print("   2. Read CREATE_NEW_AGENT_GUIDE.md to create your own agent")
        print("   3. Explore the agent_client.py source code")
    else:
        print("\n⚠️  Some tests failed. Please check:")
        print("   1. Your API key is correct")
        print("   2. You have network connectivity")
        print("   3. The agent endpoint is accessible")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

# Made with Bob
