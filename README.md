# 🤖 JARVIS - Advanced AI Voice Assistant

A smart desktop assistant capable of understanding natural language commands and executing system-level and web-based actions efficiently. Similar to JARVIS from Iron Man, this assistant listens to your voice commands and performs automated tasks.

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Supported Commands](#supported-commands)
- [Configuration](#configuration)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)
- [Advanced Features](#advanced-features)
- [Architecture](#architecture)

---

## ✨ Features

### Core Capabilities
- **🎤 Voice Input Recognition** - Understand spoken commands using Google Speech Recognition API
- **🎵 YouTube Automation** - Play music on YouTube with voice commands
- **🔍 Google Search** - Perform web searches directly from voice commands
- **🌐 Website Navigation** - Open any website by name with automatic URL resolution
- **🤖 Natural Language Processing** - Flexible phrasing support for commands
- **📊 Command History** - Maintain and view all executed commands
- **🎯 Wake Word Detection** - Custom wake word support (default: "jarvis")

### User Interface Options
- **Command Line Interface (CLI)** - Terminal-based interaction
- **Text Mode** - Type commands instead of speaking (no microphone needed)
- **Modern GUI** - Beautiful Tkinter-based graphical interface with real-time feedback
- **Dark Theme** - Eye-friendly dark mode with modern aesthetics

### Advanced Features
- Modular command architecture for easy extensibility
- Comprehensive error handling and recovery
- Command history persistence (JSON storage)
- Custom website and command registration
- Configurable voice properties (speed, volume, gender)
- Cross-platform compatibility (Windows, macOS, Linux)

---

## 🚀 Installation

### Prerequisites
- **Python 3.8+**
- **Microphone** (for voice input)
- **Internet Connection** (for voice recognition and web operations)
- **pip** (Python package manager)

### Step 1: Clone or Download Files

```bash
# Create project directory
mkdir jarvis-assistant
cd jarvis-assistant

# Copy all JARVIS files here
# Files needed:
# - jarvis_assistant.py
# - jarvis_gui.py
# - jarvis_config.py
# - requirements.txt
```

### Step 2: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# If you encounter issues with PyAudio on Windows:
# Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Then: pip install <wheel_file>.whl

# For macOS:
brew install portaudio
pip install pyaudio

# For Linux (Ubuntu/Debian):
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Step 3: Verify Installation

```bash
# Test voice recognition
python -c "import speech_recognition; print('✓ Speech Recognition OK')"

# Test text-to-speech
python -c "import pyttsx3; print('✓ Text-to-Speech OK')"

# Test GUI library
python -c "import customtkinter; print('✓ GUI Framework OK')"
```

---

## ⚡ Quick Start

### Option 1: Command Line (Voice Mode)

```bash
python jarvis_assistant.py
```

**Output:**
```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║            🤖 JARVIS - AI Voice Assistant 🤖             ║
║                      Version 1.0.0                       ║
║                                                           ║
║  A smart desktop assistant for voice-controlled automation ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

JARVIS activated. Say jarvis to give me a command, or say help for options.

✓ JARVIS is running. Say 'jarvis' to start, or type commands directly.
Type 'quit' to exit.

🎧 Listening... (speak now)
```

**How to use:**
1. Speak commands starting with the wake word ("jarvis")
2. Say your command (e.g., "jarvis play despacito on youtube")
3. Wait for confirmation
4. Say "jarvis exit" or "jarvis quit" to stop

### Option 2: Text Mode (No Microphone Required)

```bash
python jarvis_assistant.py --text-mode
```

**Example interaction:**
```
You: jarvis open google
🤖 JARVIS: Opening google
```

### Option 3: Modern GUI Application

```bash
python jarvis_gui.py
```

Features:
- 🎙️ Click "START RECORDING" button to record voice commands
- ⌨️ Type commands in the text field
- 📜 View command history in real-time
- 💡 Quick command suggestions
- 📊 Beautiful output display

### Option 4: Custom Wake Word

```bash
python jarvis_assistant.py --wake-word "hey assistant"
```

---

## 📖 Usage Guide

### Command Syntax

Commands follow flexible patterns. JARVIS understands natural variations:

```
# YouTube Music
"jarvis play [song name] on youtube"
"jarvis youtube play [song name]"
"play [song name]"  # If wake word is omitted

# Google Search
"jarvis search [query] on google"
"jarvis google search [query]"

# Website Navigation
"jarvis open [website]"
"jarvis navigate to [website]"
"jarvis go to [website]"

# System Commands
"jarvis help"           # Show available commands
"jarvis status"         # Show system status
"jarvis history"        # Show command history
"jarvis exit"          # Exit the application
```

### Example Commands

#### 🎵 Music Playback

```bash
# Play a specific song
"jarvis play bohemian rhapsody on youtube"

# Play an artist
"jarvis play taylor swift on youtube"

# Play a playlist
"jarvis play lofi beats on youtube"
```

**Result:** Opens YouTube and searches for the song

#### 🔍 Web Search

```bash
# Search with keywords
"jarvis search python programming on google"

# Search for news
"jarvis search latest ai news on google"

# Search with quotes
"jarvis search best python libraries on google"
```

**Result:** Opens Google with search results

#### 🌐 Website Navigation

```bash
# Open social media
"jarvis open facebook"
"jarvis open instagram"
"jarvis open twitter"

# Open development sites
"jarvis open github"
"jarvis open stackoverflow"

# Open video platforms
"jarvis open youtube"
"jarvis open twitch"

# Open communication tools
"jarvis open discord"
"jarvis open slack"
```

**Result:** Opens the website in default browser

#### ❓ System Commands

```bash
# Get help
"jarvis help"

# Check system status
"jarvis status"

# View history
"jarvis history"

# Exit gracefully
"jarvis exit"
"jarvis quit"
```

---

## 🎯 Supported Commands

### Built-in Website Support

The following websites are pre-configured and can be opened instantly:

**Social Media:**
- Facebook, Twitter/X, Instagram, LinkedIn, TikTok, Snapchat

**Video & Streaming:**
- YouTube, Netflix, Twitch, Disney+, HBO Max

**Communication:**
- Gmail, Slack, Discord, Telegram, WhatsApp

**Development:**
- GitHub, Stack Overflow, GitLab, Codepen, Replit

**Search & Reference:**
- Google, Wikipedia, Bing, DuckDuckGo

**Shopping:**
- Amazon, eBay, Etsy, Shopify

**AI & Tech:**
- ChatGPT, Copilot, Perplexity, Claude, Gemini

### Adding Custom Websites

```python
from jarvis_assistant import JARVIS, URLResolver

# Initialize JARVIS
jarvis = JARVIS()

# Add custom website
URLResolver.add_website("mysite", "https://mysite.com")
URLResolver.add_website("company", "https://company.internal.com")

# Now you can use:
# "jarvis open mysite"
# "jarvis open company"
```

### Adding Custom Commands

```python
from jarvis_assistant import JARVIS

jarvis = JARVIS()

# Define custom command handler
def weather_command(command):
    jarvis.voice_engine.speak("Opening weather website")
    import webbrowser
    webbrowser.open("https://weather.com")
    return "Weather opened"

# Register command
jarvis.add_command("weather", weather_command)

# Use it
# "jarvis weather"
```

---

## ⚙️ Configuration

### Modifying Settings

Edit `jarvis_config.py` to customize JARVIS:

```python
class JARVISConfig:
    # Voice Settings
    VOICE_ENABLED = True
    SPEECH_RATE = 150  # 50-300 words per minute
    SPEECH_VOLUME = 0.9  # 0.0-1.0
    
    # Recognition Settings
    AUDIO_TIMEOUT = 10
    PHRASE_TIME_LIMIT = 10
    ENERGY_THRESHOLD = 4000
    
    # Assistant Settings
    WAKE_WORD = "jarvis"  # Change wake word here
    ENABLE_CONFIRMATION_MESSAGES = True
    MAX_HISTORY_SIZE = 100
    
    # Add custom websites
    CUSTOM_WEBSITES = {
        "mysite": "https://mysite.com",
        "internal": "https://internal.company.com"
    }
```

### Save Configuration

```bash
python jarvis_config.py  # Saves default config to jarvis_config.json
```

### Voice Properties

```python
# Make JARVIS speak faster
config.SPEECH_RATE = 200  # Faster

# Make JARVIS speak slower for clarity
config.SPEECH_RATE = 100  # Slower

# Adjust microphone sensitivity
config.ENERGY_THRESHOLD = 3000  # More sensitive
config.ENERGY_THRESHOLD = 5000  # Less sensitive
```

---

## 📁 File Structure

```
jarvis-assistant/
├── jarvis_assistant.py      # Main application with CLI
├── jarvis_gui.py            # Modern GUI version
├── jarvis_config.py         # Configuration management
├── requirements.txt         # Python dependencies
├── command_history.json     # Auto-generated command history
├── jarvis.log              # Auto-generated log file
└── README.md               # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `jarvis_assistant.py` | Core JARVIS engine with voice recognition, command processing, and execution |
| `jarvis_gui.py` | Modern GUI interface using customtkinter |
| `jarvis_config.py` | Configuration management and customization |
| `requirements.txt` | All required Python packages |
| `command_history.json` | Persistent storage of executed commands |

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'speech_recognition'"

**Solution:**
```bash
pip install SpeechRecognition
```

### Issue: "ModuleNotFoundError: No module named 'pyttsx3'"

**Solution:**
```bash
pip install pyttsx3
```

### Issue: "ModuleNotFoundError: No module named 'pyaudio'"

**Solution:**

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Issue: Voice not recognized / Microphone not working

**Troubleshooting steps:**

1. **Check microphone connection:**
   ```bash
   python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_device_count())"
   ```

2. **Test microphone with SpeechRecognition:**
   ```bash
   python -c "
   import speech_recognition as sr
   r = sr.Recognizer()
   with sr.Microphone() as source:
       print('Say something...')
       audio = r.listen(source, timeout=5)
       print('Audio captured')
   "
   ```

3. **Adjust energy threshold in `jarvis_config.py`:**
   ```python
   ENERGY_THRESHOLD = 3000  # Lower = more sensitive
   ```

### Issue: Text-to-speech not working

**Solution:**
```bash
# Reinstall pyttsx3
pip uninstall pyttsx3
pip install pyttsx3
```

### Issue: GUI doesn't start

**Solution:**
```bash
# Install customtkinter
pip install customtkinter

# Update Tkinter
# Windows/macOS: Usually bundled with Python
# Linux: sudo apt-get install python3-tk
```

### Issue: Internet errors when searching or playing music

**Solution:**
- Check your internet connection
- Try a different DNS (Google: 8.8.8.8, Cloudflare: 1.1.1.1)
- Ensure firewall allows Python to access the internet

---

## 🎁 Advanced Features

### Creating Custom Command Modules

```python
from jarvis_assistant import JARVIS

class WeatherModule:
    def __init__(self, jarvis):
        self.jarvis = jarvis
        self.register_commands()
    
    def register_commands(self):
        self.jarvis.add_command("weather", self.get_weather)
        self.jarvis.add_command("forecast", self.get_forecast)
    
    def get_weather(self, command):
        self.jarvis.voice_engine.speak("Fetching weather data")
        import webbrowser
        webbrowser.open("https://weather.com")
        return "Weather opened"
    
    def get_forecast(self, command):
        self.jarvis.voice_engine.speak("Opening weather forecast")
        import webbrowser
        webbrowser.open("https://weather.gov/forecast")
        return "Forecast opened"

# Use it
jarvis = JARVIS()
weather = WeatherModule(jarvis)
jarvis.start()
```

### Accessing Command History Programmatically

```python
from jarvis_assistant import CommandHistory

history = CommandHistory()
history.load_from_file("command_history.json")

# Get last 5 commands
last_commands = history.get_last(5)

for cmd in last_commands:
    print(f"{cmd['timestamp']}: {cmd['command']}")
    print(f"Response: {cmd['response']}\n")
```

### Integration with External APIs

```python
from jarvis_assistant import JARVIS, CommandProcessor
import requests

def weather_api_handler(command):
    query = command.replace("weather for", "").strip()
    
    # Call OpenWeatherMap API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={query}&appid=YOUR_API_KEY"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        
        result = f"Weather in {query}: {temp}K, {description}"
        return result
    
    return "Could not fetch weather"

jarvis = JARVIS()
jarvis.add_command("weather", weather_api_handler)
jarvis.start()
```

---

## 🏗️ Architecture

### Component Architecture

```
┌─────────────────────────────────────────┐
│         User Interface Layer            │
│  ┌──────────────┐  ┌──────────────┐    │
│  │     CLI      │  │     GUI      │    │
│  └──────┬───────┘  └──────┬───────┘    │
└─────────┼──────────────────┼────────────┘
          │                  │
┌─────────┴──────────────────┴────────────┐
│      Voice Processing Layer             │
│  ┌──────────────┐  ┌──────────────┐    │
│  │ Recognition  │  │  Synthesis   │    │
│  │  (Listen)    │  │   (Speak)    │    │
│  └──────┬───────┘  └──────┬───────┘    │
└─────────┼──────────────────┼────────────┘
          │                  │
┌─────────┴──────────────────┴────────────┐
│     Command Processing Layer            │
│  ┌──────────────┐  ┌──────────────┐    │
│  │   Parser     │  │  Processor   │    │
│  │   (NLP)      │  │  (Execute)   │    │
│  └──────┬───────┘  └──────┬───────┘    │
└─────────┼──────────────────┼────────────┘
          │                  │
┌─────────┴──────────────────┴────────────┐
│        Action Execution Layer           │
│  ┌──────────────┐  ┌──────────────┐    │
│  │  Web Browser │  │  System Cmds │    │
│  │  Navigation  │  │  Execution   │    │
│  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────┘
```

### Class Hierarchy

- **VoiceEngine** - Handles audio input/output
- **URLResolver** - Maps website names to URLs
- **CommandProcessor** - Processes and executes commands
- **CommandHistory** - Maintains command history
- **JARVIS** - Main orchestrator class
- **JARVISGUIApp** - GUI application layer

---

## 🚀 Performance Optimization

### Reducing Response Time

```python
# Pre-compile regex patterns
import re
YOUTUBE_PATTERN = re.compile(r"play\s+(.+?)\s+on\s+youtube", re.I)

# Cache website URLs
URL_CACHE = {}

# Use threading for long operations
import threading
thread = threading.Thread(target=long_operation, daemon=True)
thread.start()
```

### Improving Voice Recognition

```python
# Adjust noise threshold
recognizer.energy_threshold = 3000

# Use faster language model (if available)
config.SPEECH_RATE = 200

# Pre-warm microphone
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)
```

---

## 📝 Logging

JARVIS logs all activities when enabled:

```python
# Enable logging in config
config.ENABLE_LOGGING = True
config.LOG_FILE = "jarvis.log"

# View logs
tail -f jarvis.log
```

Log entries include:
- Timestamps
- Commands issued
- Responses generated
- Errors and exceptions
- System status changes

---

## 🤝 Contributing

Want to add features? Here's how:

1. **Create a new command handler:**
   ```python
   def my_command_handler(command):
       # Process command
       response = "Action completed"
       return response
   ```

2. **Register with JARVIS:**
   ```python
   jarvis.add_command("mycommand", my_command_handler)
   ```

3. **Test thoroughly:**
   ```python
   jarvis.process("jarvis mycommand")
   ```

---

## 📄 License

This project is provided as-is for educational and personal use.

---

## 🆘 Support

### Frequently Asked Questions

**Q: Can JARVIS work offline?**
A: No, JARVIS requires internet for voice recognition and web operations.

**Q: Can I change the voice gender?**
A: Yes, modify the voice selection in `VoiceEngine.__init__()`.

**Q: How do I add a new website?**
A: Use `URLResolver.add_website("name", "url")` or edit `jarvis_config.py`.

**Q: Can JARVIS control other applications?**
A: Currently, JARVIS focuses on web-based automation. Local app control requires system-specific APIs.

**Q: Is my microphone always listening?**
A: No, JARVIS only listens when you press "START RECORDING" (GUI) or after you say the wake word (CLI).

---

## 🎯 Roadmap

Future enhancements planned:

- [ ] Machine learning-based command prediction
- [ ] Multi-language support
- [ ] Email integration
- [ ] Calendar integration
- [ ] Smart home control (IoT)
- [ ] Custom plugin system
- [ ] Cloud synchronization
- [ ] Mobile app companion
- [ ] Advanced NLP with transformers
- [ ] Offline voice recognition

---

## 📞 Contact

For issues, questions, or suggestions:
- Create detailed bug reports
- Include error messages and logs
- Specify your OS and Python version
- Describe steps to reproduce

---

**Made with ❤️ by Advanced AI Systems**

*"With great AI comes great responsibility."* - Uncle Ben, probably
# jarvis
