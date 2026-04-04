"""
JARVIS Configuration File
Customize settings, websites, and many command behaviors here.
"""

import json
from pathlib import Path

class JARVISConfig:
    """Configuration manager for JARVIS."""
    
    # Voice settings
    VOICE_ENABLED = True
    SPEECH_RATE = 150  # Words per minute (50-300)
    SPEECH_VOLUME = 0.9  # 0.0-1.0
    
    # Recognition settings
    AUDIO_TIMEOUT = 10  # Seconds to wait for speech
    PHRASE_TIME_LIMIT = 10  # Maximum duration of speech
    ENERGY_THRESHOLD = 4000  # Microphone sensitivity
    
    # Assistant settings
    WAKE_WORD = "jarvis"
    ENABLE_CONFIRMATION_MESSAGES = True
    ENABLE_COMMAND_HISTORY = True
    HISTORY_FILE = "command_history.json"
    MAX_HISTORY_SIZE = 100
    
    # GUI settings
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    THEME = "dark"
    COLOR_SCHEME = "blue"
    
    # Custom websites
    CUSTOM_WEBSITES = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "instagram": "https://www.instagram.com",
        "linkedin": "https://www.linkedin.com",
        "github": "https://www.github.com",
        "reddit": "https://www.reddit.com",
        "stackoverflow": "https://stackoverflow.com",
        "wikipedia": "https://www.wikipedia.org",
        "amazon": "https://www.amazon.com",
        "netflix": "https://www.netflix.com",
        "spotify": "https://www.spotify.com",
        "twitch": "https://www.twitch.tv",
        "discord": "https://discord.com",
        "slack": "https://slack.com",
    }
    
    # Custom commands
    CUSTOM_COMMANDS = {
        "weather": {
            "description": "Get current weather",
            "action": "open_website",
            "params": "https://weather.com"
        },
        "news": {
            "description": "Open news website",
            "action": "open_website",
            "params": "https://news.google.com"
        },
        "email": {
            "description": "Open Gmail",
            "action": "open_website",
            "params": "https://mail.google.com"
        }
    }
    
    # Logging settings
    ENABLE_LOGGING = True
    LOG_FILE = "jarvis.log"
    
    # API Keys (keep empty or add your own)
    OPENWEATHER_API_KEY = ""
    NEWS_API_KEY = ""
    
    @classmethod
    def load_from_file(cls, filepath: str = "jarvis_config.json"):
        """Load configuration from JSON file."""
        try:
            if Path(filepath).exists():
                with open(filepath, 'r') as f:
                    config = json.load(f)
                    for key, value in config.items():
                        if hasattr(cls, key):
                            setattr(cls, key, value)
                print(f"✓ Configuration loaded from {filepath}")
        except Exception as e:
            print(f"⚠️  Could not load config: {e}")
    
    @classmethod
    def save_to_file(cls, filepath: str = "jarvis_config.json"):
        """Save current configuration to JSON file."""
        try:
            config = {
                'VOICE_ENABLED': cls.VOICE_ENABLED,
                'SPEECH_RATE': cls.SPEECH_RATE,
                'WAKE_WORD': cls.WAKE_WORD,
                'WINDOW_WIDTH': cls.WINDOW_WIDTH,
                'WINDOW_HEIGHT': cls.WINDOW_HEIGHT,
                'CUSTOM_WEBSITES': cls.CUSTOM_WEBSITES,
            }
            with open(filepath, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✓ Configuration saved to {filepath}")
        except Exception as e:
            print(f"✗ Error saving config: {e}")
    
    @classmethod
    def get_config_dict(cls) -> dict:
        """Get all configuration as dictionary."""
        return {
            'VOICE_ENABLED': cls.VOICE_ENABLED,
            'SPEECH_RATE': cls.SPEECH_RATE,
            'SPEECH_VOLUME': cls.SPEECH_VOLUME,
            'WAKE_WORD': cls.WAKE_WORD,
            'ENABLE_CONFIRMATION_MESSAGES': cls.ENABLE_CONFIRMATION_MESSAGES,
            'ENABLE_COMMAND_HISTORY': cls.ENABLE_COMMAND_HISTORY,
            'WINDOW_WIDTH': cls.WINDOW_WIDTH,
            'WINDOW_HEIGHT': cls.WINDOW_HEIGHT,
            'THEME': cls.THEME,
            'CUSTOM_WEBSITES': cls.CUSTOM_WEBSITES,
        }


if __name__ == "__main__":
    # Save default configuration
    JARVISConfig.save_to_file()
    print("\nCurrent Configuration:")
    print(json.dumps(JARVISConfig.get_config_dict(), indent=2))
