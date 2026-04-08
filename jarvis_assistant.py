#!/usr/bin/env python3
"""
JARVIS - Advanced AI Voice Assistant System
A smart desktop assistant capable of understanding natural language commands
and executing system-level and web-based actions efficiently.

Author: Advanced AI Systems
Version: 1.0.2
Python: 3.8+
"""

import os
import sys
import json
import webbrowser
import threading
import time
from datetime import datetime
from typing import Dict, List, Callable, Optional
import re
from pathlib import Path

# ── Python 3.12+ distutils compatibility shim ────────────────────────────────
# distutils was removed in Python 3.12. pyaudio and some speech_recognition
# internals still import it. Provide a minimal shim before those imports so
# they don't crash with "No module named 'distutils'".
import sys as _sys
if _sys.version_info >= (3, 12):
    try:
        import distutils  # noqa: F401 – already available (e.g. via setuptools)
    except ModuleNotFoundError:
        try:
            # setuptools ≥ 60 ships its own distutils; just activating the
            # import is enough to make the alias available.
            import setuptools  # noqa: F401
            import distutils  # noqa: F401
        except ModuleNotFoundError:
            # Last-resort stub: create a bare-minimum distutils package so
            # downstream code can at least `import distutils` without crashing.
            import types as _types
            _dist = _types.ModuleType("distutils")
            _dist.version = _types.ModuleType("distutils.version")  # type: ignore[attr-defined]
            _sys.modules["distutils"] = _dist
            _sys.modules["distutils.version"] = _dist.version  # type: ignore[attr-defined]
# ─────────────────────────────────────────────────────────────────────────────

# Voice and speech recognition
try:
    import speech_recognition as sr
except ImportError:
    print("⚠️  speech_recognition not installed. Installing...")
    os.system("pip install SpeechRecognition")
    import speech_recognition as sr

try:
    import pyttsx3
except ImportError:
    print("⚠️  pyttsx3 not installed. Installing...")
    os.system("pip install pyttsx3")
    import pyttsx3

# pyaudio must be installed BEFORE speech_recognition tries to open a Microphone.
# On Python 3.12+ use the pre-built wheel from pipwin or the unofficial binary.
try:
    import pyaudio as _pyaudio_test  # noqa: F401
except ImportError:
    print("⚠️  pyaudio not found. Attempting install...")
    ret = os.system("pip install pyaudio")
    if ret != 0:
        # pipwin carries pre-built Windows wheels and works without a compiler
        os.system("pip install pipwin && pipwin install pyaudio")
    try:
        import pyaudio as _pyaudio_test  # noqa: F401
    except ImportError:
        print(
            "✗ pyaudio could not be installed automatically.\n"
            "  On Windows run:  pip install pipwin && pipwin install pyaudio\n"
            "  On Linux run:    sudo apt-get install python3-pyaudio\n"
            "  On macOS run:    brew install portaudio && pip install pyaudio\n"
            "JARVIS will fall back to text mode."
        )


class CommandHistory:
    """Maintains a history of executed commands."""

    def __init__(self, max_history: int = 100):
        self.history: List[Dict] = []
        self.max_history = max_history

    def add(self, command: str, response: str, timestamp: Optional[str] = None):
        """Add a command to history."""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.history.append({
            "timestamp": timestamp,
            "command": command,
            "response": response
        })

        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_last(self, count: int = 5) -> List[Dict]:
        """Get last N commands."""
        return self.history[-count:]

    def save_to_file(self, filepath: str = "command_history.json"):
        """Save history to JSON file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.history, f, indent=2)
            print(f"✓ History saved to {filepath}")
        except Exception as e:
            print(f"✗ Error saving history: {e}")

    def load_from_file(self, filepath: str = "command_history.json"):
        """Load history from JSON file."""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    self.history = json.load(f)
                print(f"✓ History loaded from {filepath}")
        except Exception as e:
            print(f"✗ Error loading history: {e}")


class VoiceEngine:
    """Handles voice input and output."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000

        # Serialise TTS calls — pyttsx3 engine is not thread-safe
        self._tts_lock = threading.Lock()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)

        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)

        self.is_listening = False

        # Detect microphone availability ONCE at startup instead of failing
        # silently on every listen() call and looping forever.
        self.mic_available = self._check_mic()

    # ── Mic availability check ───────────────────────────────────────────────

    def _check_mic(self) -> bool:
        """Return True if a working microphone + pyaudio are available."""
        try:
            import pyaudio  # noqa: F401
            mics = sr.Microphone.list_microphone_names()
            if not mics:
                print("✗ No microphones detected by the system.")
                return False
            return True
        except (ImportError, ModuleNotFoundError) as e:
            print(
                f"✗ pyaudio / distutils missing ({e}).\n"
                "  Voice input is unavailable. JARVIS will fall back to text mode.\n"
                "  Fix: pip install setuptools pyaudio   (then restart)"
            )
            return False
        except Exception as e:
            print(f"✗ Microphone check failed: {e}")
            return False

    # ── TTS ──────────────────────────────────────────────────────────────────

    def speak(self, text: str, async_mode: bool = True):
        """Convert text to speech."""
        print(f"🎤 JARVIS: {text}")
        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)

    def _speak_sync(self, text: str):
        """Synchronous TTS — serialised via lock."""
        with self._tts_lock:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"✗ TTS Error: {e}")

    # ── STT ──────────────────────────────────────────────────────────────────

    def listen(self, timeout: int = 10, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice input and convert to text.

        Returns None on failure.  Raises RuntimeError if the mic is not
        available so the caller can fall back to text mode instead of
        spinning in an infinite error loop.
        """
        if not self.mic_available:
            raise RuntimeError(
                "Microphone not available (pyaudio / distutils missing). "
                "Switching to text mode."
            )

        try:
            self.is_listening = True
            print("🎧 Listening... (speak now)")

            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            print("🔄 Processing audio...")
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You: {text}")
            return text.lower()

        except sr.WaitTimeoutError:
            # Silence timeout — not an error, just loop again
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I couldn't understand that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            self.speak(f"Network error. Please check your internet connection.")
            print(f"✗ STT network error: {e}")
            return None
        except Exception as e:
            # Any other error: print it once but DO NOT speak in a tight loop
            print(f"✗ Listen error: {e}")
            time.sleep(1)   # brief pause so the loop doesn't spin at 100 % CPU
            return None
        finally:
            self.is_listening = False


class URLResolver:
    """Resolves website names to URLs."""

    # FIX 6: Removed the duplicate "github" key (second entry overwrote the first)
    WEBSITES = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "x": "https://www.twitter.com",
        "instagram": "https://www.instagram.com",
        "linkedin": "https://www.linkedin.com",
        "github": "https://www.github.com",
        "gmail": "https://mail.google.com",
        "reddit": "https://www.reddit.com",
        "stackoverflow": "https://stackoverflow.com",
        "wikipedia": "https://www.wikipedia.org",
        "amazon": "https://www.amazon.com",
        "ebay": "https://www.ebay.com",
        "netflix": "https://www.netflix.com",
        "spotify": "https://www.spotify.com",
        "twitch": "https://www.twitch.tv",
        "discord": "https://discord.com",
        "slack": "https://slack.com",
        "chatgpt": "https://chat.openai.com",
        "copilot": "https://copilot.microsoft.com",
        "perplexity": "https://www.perplexity.ai"
    }

    @classmethod
    def resolve(cls, website_name: str) -> Optional[str]:
        """Resolve website name to URL."""
        website_name = website_name.lower().strip()

        if website_name in cls.WEBSITES:
            return cls.WEBSITES[website_name]

        for site, url in cls.WEBSITES.items():
            if site in website_name or website_name in site:
                return url

        if "." not in website_name:
            website_name = f"{website_name}.com"

        if not website_name.startswith("http"):
            website_name = f"https://www.{website_name}"

        return website_name

    @classmethod
    def add_website(cls, name: str, url: str):
        """Add a custom website mapping."""
        cls.WEBSITES[name.lower()] = url


class CommandProcessor:
    """Processes and executes voice commands."""

    def __init__(self, voice_engine: VoiceEngine, command_history: "CommandHistory"):
        self.voice_engine = voice_engine
        # FIX 2: Accept command_history so handle_show_history can actually use it
        self.command_history = command_history
        self.commands: Dict[str, Callable] = {}
        self._exit_requested = False
        self._register_default_commands()

    def _register_default_commands(self):
        """Register default command handlers."""
        self.register("play", self.handle_youtube_play)
        self.register("search", self.handle_google_search)
        self.register("open", self.handle_open_website)
        self.register("navigate", self.handle_open_website)
        self.register("go to", self.handle_open_website)
        self.register("help", self.handle_help)
        self.register("exit", self.handle_exit)
        self.register("quit", self.handle_exit)
        self.register("hello", self.handle_greeting)
        self.register("hi", self.handle_greeting)
        self.register("status", self.handle_status)
        self.register("history", self.handle_show_history)

    def register(self, trigger: str, handler: Callable):
        """Register a command handler."""
        self.commands[trigger.lower()] = handler

    def process(self, command: str) -> Optional[str]:
        """Process a voice command."""
        if not command:
            return None

        command_lower = command.lower().strip()

        for trigger, handler in self.commands.items():
            if trigger in command_lower:
                try:
                    response = handler(command)
                    return response
                except Exception as e:
                    error_response = f"Error executing command: {e}"
                    self.voice_engine.speak(error_response)
                    return error_response

        unknown_response = "I'm not sure how to do that. Say 'help' to hear available commands."
        self.voice_engine.speak(unknown_response)
        return unknown_response

    # ── Command Handlers ──────────────────────────────────────────────────────

    def handle_youtube_play(self, command: str) -> str:
        """Handle YouTube music playback command."""
        # FIX 3: Added a broad fallback pattern so plain "play <song>" works
        patterns = [
            r"play\s+(.+?)\s+on\s+youtube",
            r"play\s+(.+?)\s+youtube",
            r"youtube\s+play\s+(.+)",
            r"play\s+(.+)",           # broad fallback
        ]

        song_name = None
        for pattern in patterns:
            match = re.search(pattern, command.lower())
            if match:
                song_name = match.group(1).strip()
                break

        if not song_name:
            response = "Please specify the song name. Say: play [song name] on YouTube"
            self.voice_engine.speak(response)
            return response

        try:
            youtube_url = (
                "https://www.youtube.com/results?search_query="
                + song_name.replace(" ", "+")
            )
            webbrowser.open(youtube_url)
            response = f"Playing {song_name} on YouTube"
            self.voice_engine.speak(response)
            return response
        except Exception as e:
            error_response = f"Failed to play {song_name}: {str(e)}"
            self.voice_engine.speak(error_response)
            return error_response

    def handle_google_search(self, command: str) -> str:
        """Handle Google search command."""
        # FIX 4: Added a broad fallback pattern so plain "search <query>" works
        patterns = [
            r"search\s+(?:for\s+)?(.+?)\s+on\s+google",
            r"search\s+(?:for\s+)?(.+?)\s+google",
            r"google\s+search\s+(.+)",
            r"search\s+(?:for\s+)?(.+)",   # broad fallback
        ]

        query = None
        for pattern in patterns:
            match = re.search(pattern, command.lower())
            if match:
                query = match.group(1).strip()
                break

        if not query:
            response = "Please specify the search query. Say: search [query] on Google"
            self.voice_engine.speak(response)
            return response

        try:
            google_url = (
                "https://www.google.com/search?q=" + query.replace(" ", "+")
            )
            webbrowser.open(google_url)
            response = f"Searching Google for {query}"
            self.voice_engine.speak(response)
            return response
        except Exception as e:
            error_response = f"Failed to search: {str(e)}"
            self.voice_engine.speak(error_response)
            return error_response

    def handle_open_website(self, command: str) -> str:
        """Handle website navigation command."""
        patterns = [
            r"open\s+(.+)",
            r"navigate\s+to\s+(.+)",
            r"go\s+to\s+(.+)"
        ]

        website = None
        for pattern in patterns:
            match = re.search(pattern, command.lower())
            if match:
                website = match.group(1).strip()
                break

        if not website:
            response = "Please specify the website. Say: open [website name]"
            self.voice_engine.speak(response)
            return response

        try:
            url = URLResolver.resolve(website)
            webbrowser.open(url)
            response = f"Opening {website}"
            self.voice_engine.speak(response)
            return response
        except Exception as e:
            error_response = f"Failed to open {website}: {str(e)}"
            self.voice_engine.speak(error_response)
            return error_response

    def handle_greeting(self, command: str) -> str:
        """Handle greeting commands."""
        response = "Hello! I'm JARVIS, your AI assistant. How can I help you today?"
        self.voice_engine.speak(response)
        return response

    def handle_help(self, command: str) -> str:
        """Handle help command."""
        help_text = """
        Here are the commands I can execute:

        🎵 Music & Video:
        - "Play [song name] on YouTube"
        - "Play [song name]"  ← short form also works

        🔍 Search:
        - "Search [query] on Google"
        - "Search [query]"  ← short form also works

        🌐 Website Navigation:
        - "Open [website name]"
        - "Navigate to [website]"
        - "Go to [website]"

        ℹ️  System:
        - "Help"    — show this help message
        - "Status"  — show system status
        - "History" — show recent command history
        - "Exit" or "Quit" — exit JARVIS
        """
        print(help_text)
        self.voice_engine.speak(
            "I can help you play music on YouTube, search Google, and open websites. "
            "Say help again to see the full list."
        )
        return help_text

    def handle_status(self, command: str) -> str:
        """Handle status command."""
        import platform
        status = (
            f"System: {platform.system()} {platform.release()}. "
            "Assistant is running normally."
        )
        self.voice_engine.speak(status)
        return status

    def handle_show_history(self, command: str) -> str:
        """Handle history command."""
        # FIX 2: Now actually reads from the injected command_history object
        recent = self.command_history.get_last(5)
        if not recent:
            response = "No command history yet."
            self.voice_engine.speak(response)
            return response

        lines = ["Recent commands:"]
        for entry in recent:
            lines.append(f"  [{entry['timestamp']}] {entry['command']}")
        output = "\n".join(lines)
        print(output)
        self.voice_engine.speak(f"Showing your last {len(recent)} commands.")
        return output

    def handle_exit(self, command: str) -> str:
        """Handle exit command."""
        # FIX 7: Signal the main loop to stop
        self._exit_requested = True
        response = "Goodbye! JARVIS is shutting down."
        self.voice_engine.speak(response)
        return response


class JARVIS:
    """
    Main JARVIS Assistant System.
    Orchestrates voice input, command processing, and action execution.
    """

    def __init__(self, enable_voice: bool = True, wake_word: str = "jarvis"):
        self.voice_engine = VoiceEngine()
        self.command_history = CommandHistory()
        # FIX 2: Pass command_history into CommandProcessor
        self.command_processor = CommandProcessor(self.voice_engine, self.command_history)
        self.enable_voice = enable_voice
        self.wake_word = wake_word.lower()
        self.running = False

        print("""
        ╔═══════════════════════════════════════════════════════════╗
        ║                                                           ║
        ║            🤖 JARVIS - AI Voice Assistant 🤖             ║
        ║                      Version 1.0.1                       ║
        ║                                                           ║
        ║  A smart desktop assistant for voice-controlled automation ║
        ║                                                           ║
        ╚═══════════════════════════════════════════════════════════╝
        """)

    def start(self):
        """Start the JARVIS assistant."""
        self.running = True

        if self.enable_voice:
            self.voice_engine.speak(
                f"JARVIS activated. Say {self.wake_word} followed by your command, "
                "or say help for options."
            )
            print(f"\n✓ JARVIS is running. Say '{self.wake_word}' to start.")
        else:
            # FIX 1: Text mode prints its own clear prompt instead of voice instructions
            print("\n✓ JARVIS text mode ready. Type your command (e.g. 'open google').")

        print("Type 'quit' or 'exit' to stop.\n")

        # If mic is broken, switch to text mode immediately rather than looping
        if self.enable_voice and not self.voice_engine.mic_available:
            print(
                "\n⚠️  Microphone unavailable — switching to text mode automatically.\n"
                "   Run:  pip install setuptools pyaudio   then restart for voice mode.\n"
            )
            self.enable_voice = False

        while self.running:
            try:
                if self.enable_voice:
                    user_input = self.voice_engine.listen()
                else:
                    user_input = input("You: ").strip()

                if not user_input:
                    continue

                # In text mode skip the wake-word gate entirely
                if self.enable_voice:
                    if self.wake_word not in user_input:
                        if "quit" in user_input or "exit" in user_input:
                            self.stop()
                            break
                        continue
                    # Strip wake word before passing to processor
                    command = user_input.replace(self.wake_word, "").strip()
                else:
                    command = user_input  # use input as-is in text mode

                if not command:
                    continue

                response = self.command_processor.process(command)

                if response:
                    self.command_history.add(command, response)

                # Respect the exit flag set by handle_exit
                if (
                    self.command_processor._exit_requested
                    or "exit" in command
                    or "quit" in command
                ):
                    self.stop()
                    break

            except RuntimeError as e:
                # Mic became unavailable mid-session — fall back gracefully
                print(f"\n⚠️  {e}")
                print("Switching to text mode.\n")
                self.enable_voice = False
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted by user")
                self.stop()
                break
            except Exception as e:
                print(f"✗ Error: {e}")
                if self.enable_voice:
                    self.voice_engine.speak(f"An error occurred: {str(e)}")

    def stop(self):
        """Stop the JARVIS assistant."""
        self.running = False
        self.command_history.save_to_file()
        response = "JARVIS shutting down. Goodbye!"
        self.voice_engine.speak(response, async_mode=False)  # wait for speech to finish
        print(f"\n{response}\n")

    def add_command(self, trigger: str, handler: Callable):
        """Add a custom command."""
        self.command_processor.register(trigger, handler)

    def add_website(self, name: str, url: str):
        """Add a custom website mapping."""
        URLResolver.add_website(name, url)


class TextModeJARVIS:
    """Text-based interface for JARVIS (useful for testing without voice)."""

    def __init__(self):
        self.jarvis = JARVIS(enable_voice=False)

    def start(self):
        """Start text mode."""
        print("\n" + "=" * 60)
        print("JARVIS - Text Mode")
        print("=" * 60)
        print("\nCommands:")
        print("  - Type your command (e.g., 'open google')")
        print("  - Type 'help' for available commands")
        print("  - Type 'quit' to exit\n")

        self.jarvis.start()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="JARVIS AI Voice Assistant")
    parser.add_argument(
        "--text-mode",
        action="store_true",
        help="Run in text mode instead of voice mode"
    )
    parser.add_argument(
        "--wake-word",
        default="jarvis",
        help="Custom wake word (default: jarvis)"
    )

    args = parser.parse_args()

    try:
        if args.text_mode:
            assistant = TextModeJARVIS()
            assistant.start()
        else:
            try:
                assistant = JARVIS(enable_voice=True, wake_word=args.wake_word)
                assistant.start()
            except Exception as e:
                print(f"\n⚠️  Voice mode failed: {e}")
                print("Falling back to text mode...\n")
                assistant = JARVIS(enable_voice=False, wake_word=args.wake_word)
                assistant.start()

    except KeyboardInterrupt:
        print("\n\nJARVIS terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
 