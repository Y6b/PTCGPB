import json
import os
from src.utils.logger import logger

class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self._default_config()
        self.load_config()

    def _default_config(self):
        return {
            "general": {
                "bot_language": "English",
                "instances": 1,
                "columns": 3,
                "delete_method": "Create Bots (13P)",
                "open_extra_pack": False,
                "spend_hourglass": False
            },
            "wonderpick": {
                "min_stars": 0,
                "full_art_check": False
            },
            "save_for_trade": {
                "enabled": False
            },
            "system": {
                "debug_mode": False
            }
        }

    def load_config(self):
        """Loads configuration from JSON file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Recursively update default config to retain missing keys
                    self._update_dict(self.config, loaded_config)
                logger.info(f"Loaded config from {self.config_path}")
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
        else:
            logger.info(f"Config file not found, using defaults. Will create {self.config_path} on save.")

    def save_config(self):
        """Saves current configuration to JSON file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            logger.info(f"Saved config to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def _update_dict(self, d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = self._update_dict(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    def get(self, section, key=None):
        """Gets a config value. If key is None, returns the whole section."""
        if section not in self.config:
            return None
        if key is None:
            return self.config[section]
        return self.config[section].get(key)

    def set(self, section, key, value):
        """Sets a config value and saves."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config()
