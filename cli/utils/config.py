"""Configuration management for CloudSathi CLI."""
import os
from pathlib import Path
from typing import Optional
import yaml


class Config:
    """Configuration manager for CLI."""

    def __init__(self):
        """Initialize configuration."""
        self.config_dir = Path.home() / ".cloudsathi"
        self.config_file = self.config_dir / "config.yaml"
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return self._default_config()

    def _default_config(self) -> dict:
        """Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "api_url": os.getenv("CLOUDSATHI_API_URL", "http://localhost:8000"),
            "output_format": "table",
            "timeout": 30
        }

    def save(self) -> None:
        """Save configuration to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)

    def set(self, key: str, value: str) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
        self.save()

    @property
    def api_url(self) -> str:
        """Get API URL from config or environment.
        
        Returns:
            API URL
        """
        return os.getenv("CLOUDSATHI_API_URL") or self.get("api_url", "http://localhost:8000")
