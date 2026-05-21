"""
Unit tests for Config and utilities
"""
import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.config import Config


class TestConfigInitialization:
    """Test suite for Config class initialization"""
    
    @patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token_123',
        'GITHUB_API_URL': 'https://api.github.com',
        'RISK_AUTO_FIX_THRESHOLD': '0.3',
        'RISK_HUMAN_REVIEW_THRESHOLD': '0.7',
        'SERVER_HOST': '127.0.0.1',
        'SERVER_PORT': '8000',
        'LOG_LEVEL': 'DEBUG'
    })
    def test_config_with_all_env_vars(self):
        """Test config initialization with all environment variables"""
        config = Config()
        
        assert config.github_token == 'test_token_123'
        assert config.github_api_url == 'https://api.github.com'
        assert config.risk_auto_fix_threshold == 0.3
        assert config.risk_human_review_threshold == 0.7
        assert config.server_host == '127.0.0.1'
        assert config.server_port == 8000
        assert config.log_level == 'DEBUG'
    
    @patch.dict(os.environ, {
        'GITHUB_TOKEN': 'valid_token',
    }, clear=False)
    def test_config_with_defaults(self):
        """Test config initialization with default values"""
        # Ensure other env vars are not set
        env_keys_to_clear = [
            'GITHUB_API_URL',
            'RISK_AUTO_FIX_THRESHOLD',
            'RISK_HUMAN_REVIEW_THRESHOLD',
            'SERVER_HOST',
            'SERVER_PORT',
            'LOG_LEVEL'
        ]
        
        for key in env_keys_to_clear:
            os.environ.pop(key, None)
        
        config = Config()
        
        assert config.github_token == 'valid_token'
        assert config.github_api_url == 'https://api.github.com'
        assert config.risk_auto_fix_threshold == 0.3
        assert config.risk_human_review_threshold == 0.7
        assert config.server_host == '0.0.0.0'
        assert config.server_port == 8000
        assert config.log_level == 'INFO'
    
    def test_config_validation_missing_github_token(self):
        """Test that missing GITHUB_TOKEN raises ValueError"""
        with patch.dict(os.environ, {'GITHUB_TOKEN': ''}, clear=True):
            with pytest.raises(ValueError, match="GITHUB_TOKEN is required"):
                Config()
    
    @patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token',
        'RISK_AUTO_FIX_THRESHOLD': '0.25',
        'RISK_HUMAN_REVIEW_THRESHOLD': '0.75'
    })
    def test_config_custom_risk_thresholds(self):
        """Test config with custom risk thresholds"""
        config = Config()
        
        assert config.risk_auto_fix_threshold == 0.25
        assert config.risk_human_review_threshold == 0.75
    
    @patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token',
        'SERVER_HOST': 'localhost',
        'SERVER_PORT': '9000'
    })
    def test_config_custom_server_settings(self):
        """Test config with custom server settings"""
        config = Config()
        
        assert config.server_host == 'localhost'
        assert config.server_port == 9000
    
    @patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token',
        'RISK_AUTO_FIX_THRESHOLD': 'invalid'
    })
    def test_config_invalid_threshold_value(self):
        """Test config with invalid threshold value"""
        with pytest.raises(ValueError):
            Config()
    
    @patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token',
        'SERVER_PORT': 'not_a_number'
    })
    def test_config_invalid_port_value(self):
        """Test config with invalid port value"""
        with pytest.raises(ValueError):
            Config()


class TestConfigValidation:
    """Test suite for Config validation"""
    
    @patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token',
        'RISK_AUTO_FIX_THRESHOLD': '0.3',
        'RISK_HUMAN_REVIEW_THRESHOLD': '0.7'
    })
    def test_risk_thresholds_ordering(self):
        """Test that auto_fix threshold is less than human_review threshold"""
        config = Config()
        
        # This is a reasonable expectation for configuration
        assert config.risk_auto_fix_threshold < config.risk_human_review_threshold
    
    @patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token',
        'RISK_AUTO_FIX_THRESHOLD': '0.5',
        'RISK_HUMAN_REVIEW_THRESHOLD': '0.3'
    })
    def test_invalid_threshold_ordering(self):
        """Test when thresholds are in wrong order"""
        # Config should still create but with swapped values
        config = Config()
        
        assert config.risk_auto_fix_threshold == 0.5
        assert config.risk_human_review_threshold == 0.3


class TestConfigIntegration:
    """Integration tests for Config"""
    
    @patch.dict(os.environ, {
        'GITHUB_TOKEN': 'integration_test_token',
        'GITHUB_API_URL': 'https://github.custom.com/api',
        'RISK_AUTO_FIX_THRESHOLD': '0.2',
        'RISK_HUMAN_REVIEW_THRESHOLD': '0.8',
        'SERVER_HOST': '192.168.1.1',
        'SERVER_PORT': '3000',
        'LOG_LEVEL': 'WARNING'
    })
    def test_full_config_integration(self):
        """Test complete config initialization with all custom values"""
        config = Config()
        
        # Verify all settings
        assert config.github_token == 'integration_test_token'
        assert config.github_api_url == 'https://github.custom.com/api'
        assert config.risk_auto_fix_threshold == 0.2
        assert config.risk_human_review_threshold == 0.8
        assert config.server_host == '192.168.1.1'
        assert config.server_port == 3000
        assert config.log_level == 'WARNING'
        
        # Verify it can be used
        assert config.github_token != ''
        assert isinstance(config.server_port, int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
