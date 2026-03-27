#!/usr/bin/env python3
"""
JARVIS - Usage Examples and Advanced Patterns

This file demonstrates various ways to use and extend JARVIS.
"""

from jarvis_assistant import (
    JARVIS, VoiceEngine, CommandProcessor, URLResolver,
    CommandHistory
)


# ============================================================================
# EXAMPLE 1: Basic Usage
# ============================================================================

def example_basic_usage():
    """Basic JARVIS setup and usage."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60 + "\n")
    
    # Initialize JARVIS
    jarvis = JARVIS(enable_voice=True, wake_word="jarvis")
    
    # Start the assistant
    jarvis.start()


# ============================================================================
# EXAMPLE 2: Text Mode (No Voice)
# ============================================================================

def example_text_mode():
    """Run JARVIS in text mode without voice."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Text Mode (No Voice)")
    print("="*60 + "\n")
    
    jarvis = JARVIS(enable_voice=False)
    jarvis.start()


# ============================================================================
# EXAMPLE 3: Custom Wake Word
# ============================================================================

def example_custom_wake_word():
    """Use a custom wake word."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Wake Word")
    print("="*60 + "\n")
    
    # Initialize with custom wake word
    jarvis = JARVIS(enable_voice=True, wake_word="hey assistant")
    
    print("Use 'hey assistant' as the wake word instead of 'jarvis'")
    jarvis.start()


# ============================================================================
# EXAMPLE 4: Custom Commands
# ============================================================================

def example_custom_commands():
    """Add custom command handlers."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Custom Commands")
    print("="*60 + "\n")
    
    jarvis = JARVIS(enable_voice=False)
    
    # Define custom command handlers
    def weather_command(command):
        jarvis.voice_engine.speak("Opening weather website")
        import webbrowser
        webbrowser.open("https://weather.com")
        return "Weather website opened"
    
    def time_command(command):
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {current_time}"
        jarvis.voice_engine.speak(response)
        return response
    
    def calculator_command(command):
        jarvis.voice_engine.speak("Opening calculator")
        import webbrowser
        webbrowser.open("https://www.calculator.net")
        return "Calculator opened"
    
    # Register commands
    jarvis.add_command("weather", weather_command)
    jarvis.add_command("time", time_command)
    jarvis.add_command("calculator", calculator_command)
    
    # Test commands
    print("\n📝 Testing custom commands:\n")
    
    commands = [
        "jarvis weather",
        "jarvis time",
        "jarvis calculator"
    ]
    
    for cmd in commands:
        print(f"Command: {cmd}")
        # Simulate processing
        if "weather" in cmd:
            print("→ Response: Weather website opened\n")
        elif "time" in cmd:
            print("→ Response: The current time is [current_time]\n")
        elif "calculator" in cmd:
            print("→ Response: Calculator opened\n")


# ============================================================================
# EXAMPLE 5: Custom Websites
# ============================================================================

def example_custom_websites():
    """Add custom website mappings."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Websites")
    print("="*60 + "\n")
    
    jarvis = JARVIS(enable_voice=False)
    
    # Add custom websites
    URLResolver.add_website("company", "https://mycompany.com")
    URLResolver.add_website("internal", "https://internal.company.com")
    URLResolver.add_website("docs", "https://docs.mycompany.com")
    
    print("✓ Added custom websites:")
    print("  - 'jarvis open company' → https://mycompany.com")
    print("  - 'jarvis open internal' → https://internal.company.com")
    print("  - 'jarvis open docs' → https://docs.mycompany.com")


# ============================================================================
# EXAMPLE 6: Command History
# ============================================================================

def example_command_history():
    """Work with command history."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Command History")
    print("="*60 + "\n")
    
    history = CommandHistory(max_history=100)
    
    # Add some sample commands
    sample_commands = [
        ("search python tutorial on google", "Searching Google for python tutorial"),
        ("play despacito on youtube", "Playing despacito on YouTube"),
        ("open facebook", "Opening facebook"),
    ]
    
    for command, response in sample_commands:
        history.add(command, response)
    
    print("✓ Added commands to history\n")
    
    # View last 5 commands
    print("📜 Last 5 commands:")
    for entry in history.get_last(5):
        print(f"  [{entry['timestamp']}] {entry['command']}")
        print(f"    → {entry['response']}\n")
    
    # Save history
    history.save_to_file("example_history.json")
    print("\n✓ History saved to 'example_history.json'")


# ============================================================================
# EXAMPLE 7: Programmatic Command Execution
# ============================================================================

def example_programmatic_execution():
    """Execute commands programmatically without voice."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Programmatic Command Execution")
    print("="*60 + "\n")
    
    jarvis = JARVIS(enable_voice=False)
    
    # Commands to execute
    commands = [
        "jarvis help",
        "jarvis status",
        "jarvis open github",
        "jarvis search machine learning on google",
        "jarvis play lofi beats on youtube",
    ]
    
    print("Executing commands programmatically:\n")
    
    for cmd in commands:
        print(f"Command: {cmd}")
        # In real scenario, you would process these
        response = jarvis.command_processor.process(cmd)
        print(f"Response: {response}\n")


# ============================================================================
# EXAMPLE 8: Advanced Command Handler with NLP
# ============================================================================

def example_advanced_nlp_handler():
    """Create advanced command handlers with NLP."""
    print("\n" + "="*60)
    print("EXAMPLE 8: Advanced NLP Command Handler")
    print("="*60 + "\n")
    
    jarvis = JARVIS(enable_voice=False)
    
    def advanced_search(command):
        """Advanced search that understands context."""
        import re
        
        # Extract different types of searches
        if re.search(r"wikipedia.*?", command.lower()):
            jarvis.voice_engine.speak("Searching Wikipedia")
            import webbrowser
            query = re.search(r"search.*?about\s+(.+?)$", command.lower())
            if query:
                webbrowser.open(f"https://wikipedia.org/search?search={query.group(1)}")
            return "Wikipedia search opened"
        
        elif re.search(r"stack.*?overflow", command.lower()):
            jarvis.voice_engine.speak("Searching Stack Overflow")
            import webbrowser
            query = re.search(r"search.*?about\s+(.+?)$", command.lower())
            if query:
                webbrowser.open(f"https://stackoverflow.com/search?q={query.group(1)}")
            return "Stack Overflow search opened"
        
        else:
            return "Unknown search type"
    
    jarvis.add_command("search", advanced_search)
    print("✓ Advanced NLP handler registered")
    print("  Examples:")
    print("  - 'jarvis search wikipedia about python'")
    print("  - 'jarvis search stack overflow about debugging'")


# ============================================================================
# EXAMPLE 9: Voice Configuration
# ============================================================================

def example_voice_configuration():
    """Configure voice properties."""
    print("\n" + "="*60)
    print("EXAMPLE 9: Voice Configuration")
    print("="*60 + "\n")
    
    jarvis = JARVIS(enable_voice=False)
    
    # Access voice engine
    voice = jarvis.voice_engine
    
    # Configure voice properties
    voice.engine.setProperty('rate', 200)  # Faster speech
    voice.engine.setProperty('volume', 0.8)  # Slightly lower volume
    
    # Get available voices
    voices = voice.engine.getProperty('voices')
    
    print(f"✓ Voice Configuration:")
    print(f"  Speech Rate: 200 wpm (default: 150)")
    print(f"  Volume: 0.8 (default: 0.9)")
    print(f"  Available voices: {len(voices)}")
    
    if len(voices) > 0:
        print(f"  Current voice: {voices[0].name}")
    if len(voices) > 1:
        print(f"  Alternative voice: {voices[1].name}")


# ============================================================================
# EXAMPLE 10: Multi-threading and Async Operations
# ============================================================================

def example_async_operations():
    """Handle long-running operations asynchronously."""
    print("\n" + "="*60)
    print("EXAMPLE 10: Asynchronous Operations")
    print("="*60 + "\n")
    
    import threading
    import time
    
    jarvis = JARVIS(enable_voice=False)
    
    def long_running_command(command):
        """Simulate a long-running operation."""
        def background_task():
            print("  [Background] Starting long operation...")
            time.sleep(2)
            print("  [Background] Operation completed!")
        
        # Run in background thread
        thread = threading.Thread(target=background_task, daemon=True)
        thread.start()
        
        return "Operation started in background"
    
    jarvis.add_command("long", long_running_command)
    
    print("✓ Async command handler registered")
    print("  Long-running operations won't block the interface")
    print("  Example: 'jarvis long task'")


# ============================================================================
# EXAMPLE 11: Error Handling and Recovery
# ============================================================================

def example_error_handling():
    """Demonstrate robust error handling."""
    print("\n" + "="*60)
    print("EXAMPLE 11: Error Handling and Recovery")
    print("="*60 + "\n")
    
    jarvis = JARVIS(enable_voice=False)
    
    def robust_command(command):
        """Command with comprehensive error handling."""
        try:
            import webbrowser
            
            # Parse command
            url = "https://example.com"
            
            # Open browser with error handling
            try:
                webbrowser.open(url)
                return "Website opened successfully"
            except Exception as browser_error:
                return f"Browser error: {browser_error}. Trying alternative method..."
        
        except Exception as e:
            return f"Command failed: {str(e)}"
    
    jarvis.add_command("robust", robust_command)
    
    print("✓ Robust command handler with:")
    print("  - Try-except blocks")
    print("  - Nested error handling")
    print("  - User-friendly error messages")


# ============================================================================
# EXAMPLE 12: Integration with External APIs
# ============================================================================

def example_api_integration():
    """Example of integrating external APIs."""
    print("\n" + "="*60)
    print("EXAMPLE 12: API Integration")
    print("="*60 + "\n")
    
    def weather_from_api(command):
        """Get weather from external API."""
        try:
            import requests
            
            # Example: Using Open-Meteo (free, no API key needed)
            url = "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current=temperature_2m"
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                temp = data['current']['temperature_2m']
                return f"Current temperature: {temp} degrees Celsius"
            else:
                return "Could not fetch weather data"
        
        except ImportError:
            return "Please install requests library: pip install requests"
        except Exception as e:
            return f"Error fetching weather: {e}"
    
    jarvis = JARVIS(enable_voice=False)
    jarvis.add_command("weather", weather_from_api)
    
    print("✓ API integration example:")
    print("  - Using Open-Meteo weather API (no key required)")
    print("  - Demonstrates error handling for API calls")
    print("  - Example: 'jarvis weather'")


# ============================================================================
# EXAMPLE 13: Configuration Management
# ============================================================================

def example_configuration():
    """Work with JARVIS configuration."""
    print("\n" + "="*60)
    print("EXAMPLE 13: Configuration Management")
    print("="*60 + "\n")
    
    from jarvis_config import JARVISConfig
    
    print("Current Configuration:")
    config = JARVISConfig.get_config_dict()
    
    for key, value in config.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in list(value.items())[:3]:
                print(f"    - {k}: {v}")
            if len(value) > 3:
                print(f"    ... and {len(value)-3} more")
        else:
            print(f"  {key}: {value}")
    
    print("\n✓ Save configuration:")
    print("  JARVISConfig.save_to_file('jarvis_config.json')")


# ============================================================================
# EXAMPLE 14: Creating a JARVIS Module
# ============================================================================

def example_jarvis_module():
    """Create a reusable JARVIS module."""
    print("\n" + "="*60)
    print("EXAMPLE 14: Creating JARVIS Modules")
    print("="*60 + "\n")
    
    class UtilityModule:
        """A reusable module for JARVIS."""
        
        def __init__(self, jarvis):
            self.jarvis = jarvis
            self.register()
        
        def register(self):
            """Register all commands in this module."""
            self.jarvis.add_command("flip", self.flip_coin)
            self.jarvis.add_command("dice", self.roll_dice)
        
        def flip_coin(self, command):
            """Flip a coin."""
            import random
            result = random.choice(["Heads", "Tails"])
            response = f"Coin flip result: {result}"
            self.jarvis.voice_engine.speak(response)
            return response
        
        def roll_dice(self, command):
            """Roll a dice."""
            import random
            result = random.randint(1, 6)
            response = f"Dice roll result: {result}"
            self.jarvis.voice_engine.speak(response)
            return response
    
    jarvis = JARVIS(enable_voice=False)
    utility = UtilityModule(jarvis)
    
    print("✓ Created utility module with commands:")
    print("  - 'jarvis flip' → flip a coin")
    print("  - 'jarvis dice' → roll a dice")


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """Run examples from menu."""
    examples = {
        "1": ("Basic Usage", example_basic_usage),
        "2": ("Text Mode (No Voice)", example_text_mode),
        "3": ("Custom Wake Word", example_custom_wake_word),
        "4": ("Custom Commands", example_custom_commands),
        "5": ("Custom Websites", example_custom_websites),
        "6": ("Command History", example_command_history),
        "7": ("Programmatic Execution", example_programmatic_execution),
        "8": ("Advanced NLP Handler", example_advanced_nlp_handler),
        "9": ("Voice Configuration", example_voice_configuration),
        "10": ("Async Operations", example_async_operations),
        "11": ("Error Handling", example_error_handling),
        "12": ("API Integration", example_api_integration),
        "13": ("Configuration Management", example_configuration),
        "14": ("Create Modules", example_jarvis_module),
    }
    
    print("\n" + "="*60)
    print("JARVIS - Usage Examples")
    print("="*60)
    print("\nAvailable Examples:")
    
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    
    print("\n  0. Exit")
    
    choice = input("\nSelect an example (0-14): ").strip()
    
    if choice in examples:
        name, func = examples[choice]
        print(f"\n▶ Running: {name}\n")
        try:
            func()
        except KeyboardInterrupt:
            print("\n\n⏹️  Example interrupted by user")
        except Exception as e:
            print(f"\n✗ Error running example: {e}")
    elif choice == "0":
        print("\nGoodbye!")
    else:
        print("\n✗ Invalid choice")
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExamples terminated.")