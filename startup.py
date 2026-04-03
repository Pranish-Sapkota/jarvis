#!/usr/bin/env python3
"""
JARVIS Startup Script
Easy launcher for different JARVIS modes
"""

import sys
import subprocess
import os
from pathlib import Path


def print_header():
    """Print welcome header."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║            🤖 JARVIS - AI Voice Assistant 🤖             ║
    ║                      Startup Menu                        ║
    ║                                                           ║
    ║  A smart desktop assistant for voice-controlled automation ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)


def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...\n")

    dependencies = {
        "speech_recognition": "SpeechRecognition",
        "pyttsx3": "Text-to-Speech",
        "pyaudio": "PyAudio (Optional)",
    }

    missing = []

    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {name} installed")
        except ImportError:
            print(f"✗ {name} NOT installed")
            missing.append((module, name))

    if missing:
        print("\n⚠️  Missing dependencies detected!")
        print("\nInstall with:")
        print("  pip install -r requirements.txt")

        response = input("\nInstall now? (y/n): ").strip().lower()
        if response == 'y':
            print("\nInstalling dependencies...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
            )
            print("✓ Dependencies installed!")
        else:
            print("⚠️  Some features may not work without dependencies")

    print()


def show_menu():
    """Display main menu."""
    print("\nSelect startup mode:\n")
    print("  1. 🎤 Voice Mode (with microphone)")
    print("  2. ⌨️  Text Mode (type commands)")
    print("  3. 🎨 GUI Mode (modern interface)")
    print("  4. 📚 View Examples")
    print("  5. ⚙️  Configuration")
    print("  6. ❓ Help")
    print("  0. ❌ Exit")
    print()


def launch_voice_mode():
    """Launch voice mode."""
    print("\n🎤 Starting Voice Mode...\n")
    print("Instructions:")
    print("  - Say 'jarvis' followed by your command")
    print("  - Example: 'jarvis open google'")
    print("  - Say 'jarvis help' to see available commands")
    print("  - Say 'jarvis exit' to quit\n")

    input("Press Enter to start...")
    subprocess.run([sys.executable, "jarvis_assistant.py"])


def launch_text_mode():
    """Launch text mode."""
    print("\n⌨️  Starting Text Mode...\n")
    print("Instructions:")
    print("  - Type commands like: 'jarvis open google'")
    print("  - Type 'help' for available commands")
    print("  - Type 'quit' to exit\n")

    subprocess.run([sys.executable, "jarvis_assistant.py", "--text-mode"])


def launch_gui_mode():
    """Launch GUI mode."""
    print("\n🎨 Starting GUI Mode...\n")
    print("Instructions:")
    print("  - Click 'START RECORDING' to record voice commands")
    print("  - Or type commands in the text field")
    print("  - View command history on the right panel")
    print("  - Use quick command suggestions at the bottom\n")

    try:
        subprocess.run([sys.executable, "jarvis_gui.py"])
    except FileNotFoundError:
        print("✗ Error: jarvis_gui.py not found")
    except Exception as e:
        print(f"✗ Error launching GUI: {e}")
        print("\nFalling back to text mode...\n")
        subprocess.run([sys.executable, "jarvis_assistant.py", "--text-mode"])


def show_examples():
    """Show example file."""
    print("\n📚 Opening Examples...\n")

    try:
        subprocess.run([sys.executable, "examples.py"])
    except FileNotFoundError:
        print("✗ Error: examples.py not found")


def show_configuration():
    """Show configuration menu."""
    print("\n⚙️  Configuration Menu\n")

    print("Options:")
    print("  1. View current configuration")
    print("  2. Edit configuration file")
    print("  3. Reset to defaults")
    print("  0. Back to main menu")
    print()

    choice = input("Select option: ").strip()

    if choice == "1":
        show_config()
    elif choice == "2":
        edit_config()
    elif choice == "3":
        reset_config()
    elif choice != "0":
        print("✗ Invalid choice")


def show_config():
    """Display current configuration."""
    try:
        from jarvis_config import JARVISConfig

        print("\n📋 Current Configuration:\n")
        config = JARVISConfig.get_config_dict()

        for key, value in config.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for k, v in list(value.items())[:3]:
                    print(f"  - {k}: {v}")
                if len(value) > 3:
                    print(f"  ... and {len(value)-3} more items")
            else:
                print(f"{key}: {value}")

        print()
    except Exception as e:
        print(f"✗ Error reading configuration: {e}")


def edit_config():
    """Edit configuration file."""
    config_file = "jarvis_config.py"

    print(f"\n✎ Opening {config_file} in editor...\n")

    # Try different editors
    editors = ["nano", "vim", "code", "notepad"]

    for editor in editors:
        try:
            subprocess.run([editor, config_file])
            return
        except FileNotFoundError:
            continue

    print("✗ No text editor found. Please edit jarvis_config.py manually.")
    print(f"  Location: {os.path.abspath(config_file)}")


def reset_config():
    """Reset configuration to defaults."""
    response = input("\n⚠️  Reset configuration to defaults? (y/n): ").strip().lower()

    if response == 'y':
        try:
            subprocess.run([sys.executable, "jarvis_config.py"])
            print("✓ Configuration reset to defaults")
        except Exception as e:
            print(f"✗ Error: {e}")


def show_help():
    """Display help information."""
    help_text = """
╔═════════════════════════════════════════════════════════════════╗
║                     JARVIS Help Information                    ║
╚═════════════════════════════════════════════════════════════════╝

📖 QUICK START:

  Voice Mode:
    Say: "jarvis [command]"
    Example: "jarvis open google"
    Example: "jarvis play despacito on youtube"
    Example: "jarvis search python on google"

  Text Mode:
    Type: "jarvis [command]"
    Example: "jarvis open facebook"

🎯 COMMON COMMANDS:

  🎵 Music Playback:
    - "jarvis play [song name] on youtube"

  🔍 Web Search:
    - "jarvis search [query] on google"

  🌐 Website Navigation:
    - "jarvis open [website]"
    - "jarvis navigate to [website]"
    - "jarvis go to [website]"

  ℹ️ System:
    - "jarvis help" - Show help
    - "jarvis status" - Show status
    - "jarvis history" - Show history
    - "jarvis exit" - Exit application

📊 SUPPORTED WEBSITES:

  Social Media: facebook, twitter, instagram, linkedin
  Video: youtube, netflix, twitch
  Communication: gmail, discord, slack
  Development: github, stackoverflow
  Search: google, wikipedia
  And many more!

🔧 TROUBLESHOOTING:

  Q: Microphone not detected
  A: Check microphone connection and permissions

  Q: Voice not recognized
  A: Speak clearly and adjust microphone in settings

  Q: Website not opening
  A: Check internet connection and website URL

📚 MORE INFORMATION:

  - Read README.md for detailed documentation
  - Run examples.py to see usage patterns
  - Check jarvis_config.py for advanced settings

🌐 REQUIREMENTS:

  - Python 3.8+
  - Internet connection (for web operations)
  - Microphone (for voice input, optional)

💡 TIPS:

  - Use clear, distinct pronunciation for voice commands
  - Custom commands can be added via jarvis_config.py
  - Command history is automatically saved
  - Switch between voice and text mode anytime

❓ Still need help?

  1. Check the README.md file
  2. Review examples.py
  3. Edit jarvis_config.py for settings
  4. Read the inline code documentation

╚═════════════════════════════════════════════════════════════════╝
"""
    print(help_text)
    input("Press Enter to continue...")


def main():
    """Main startup routine."""
    print_header()

    # Check dependencies on first run
    if not Path(".dependencies_checked").exists():
        check_dependencies()
        Path(".dependencies_checked").touch()

    while True:
        show_menu()
        choice = input("Enter your choice (0-6): ").strip()

        try:
            if choice == "1":
                launch_voice_mode()
            elif choice == "2":
                launch_text_mode()
            elif choice == "3":
                launch_gui_mode()
            elif choice == "4":
                show_examples()
            elif choice == "5":
                show_configuration()
            elif choice == "6":
                show_help()
            elif choice == "0":
                print("\n👋 Goodbye!\n")
                break
            else:
                print("\n✗ Invalid choice. Please try again.\n")

        except KeyboardInterrupt:
            print("\n\n⏹️  Interrupted by user")
            response = input("Exit JARVIS? (y/n): ").strip().lower()
            if response == 'y':
                print("\n👋 Goodbye!\n")
                break
        except Exception as e:
            print(f"\n✗ Error: {e}\n")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)
