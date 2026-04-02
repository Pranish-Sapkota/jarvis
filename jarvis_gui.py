#!/usr/bin/env python3
"""
JARVIS GUI - Modern Interface for AI Voice Assistant
A modern, visually appealing GUI for the JARVIS voice assistant.

Features:
- Real-time voice command processing
- Visual feedback for listening/processing states
- Command history display
- Command suggestions
- Settings panel
- Dark theme with modern design

Author: Pranish Sapkota
Version: 1.0.0
"""

import sys
import threading
import json
from datetime import datetime
from pathlib import Path

try:
    import customtkinter as ctk
except ImportError:
    print("Installing customtkinter...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk

# Import JARVIS core modules
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis_assistant import JARVIS, VoiceEngine, CommandProcessor, URLResolver


class JARVISGUIApp(ctk.CTk):
    """Modern GUI application for JARVIS."""

    def __init__(self):
        super().__init__()

        # Configure window
        self.title("JARVIS - AI Voice Assistant")
        self.geometry("1200x800")
        self.iconbitmap(default="")  # Use default icon

        # Configure color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize JARVIS backend
        self.jarvis = JARVIS(enable_voice=True)
        self.voice_engine = self.jarvis.voice_engine
        self.command_processor = self.jarvis.command_processor
        self.command_history = self.jarvis.command_history

        # State variables
        self.is_recording = False
        self.is_processing = False
        self.recording_time = 0

        # Build UI
        self._build_ui()
        self._setup_styles()

        # Load previous history
        self.command_history.load_from_file("command_history.json")
        self._refresh_history_display()

    def _setup_styles(self):
        """Configure visual styles."""
        self.primary_color = "#1f6aa5"
        self.secondary_color = "#0d47a1"
        self.accent_color = "#00bcd4"
        self.success_color = "#4caf50"
        self.error_color = "#f44336"

    def _build_ui(self):
        """Build the user interface."""
        # Main container
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        self._build_header(main_container)

        # Main content area
        content_container = ctk.CTkFrame(main_container)
        content_container.pack(fill="both", expand=True, pady=20)

        # Split into left and right panels
        left_panel = ctk.CTkFrame(content_container)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_panel = ctk.CTkFrame(content_container)
        right_panel.pack(side="right", fill="both", expand=False, padx=(10, 0), ipadx=10)

        # Build left panel (voice control and display)
        self._build_voice_control(left_panel)
        self._build_output_display(left_panel)

        # Build right panel (history and suggestions)
        self._build_command_history(right_panel)
        self._build_suggestions(right_panel)

        # Footer
        self._build_footer(main_container)

    def _build_header(self, parent):
        """Build the header section."""
        header = ctk.CTkFrame(parent, height=80)
        header.pack(fill="x", pady=(0, 20))

        # Title
        title = ctk.CTkLabel(
            header,
            text="🤖 JARVIS",
            font=("Helvetica", 48, "bold"),
            text_color=self.primary_color
        )
        title.pack(side="left", padx=20)

        # Subtitle
        subtitle = ctk.CTkLabel(
            header,
            text="AI Voice Assistant | Voice-Controlled Automation",
            font=("Helvetica", 14),
            text_color="#888888"
        )
        subtitle.pack(side="left", padx=20, pady=(40, 0))

        # Status indicator
        self.status_indicator = ctk.CTkLabel(
            header,
            text="● READY",
            font=("Helvetica", 12, "bold"),
            text_color=self.success_color
        )
        self.status_indicator.pack(side="right", padx=20, pady=10)

    def _build_voice_control(self, parent):
        """Build voice control section."""
        control_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=15)
        control_frame.pack(fill="x", pady=(0, 20))

        # Title
        title = ctk.CTkLabel(
            control_frame,
            text="🎤 Voice Control",
            font=("Helvetica", 16, "bold"),
            text_color=self.accent_color
        )
        title.pack(pady=(15, 10), padx=15)

        # Waveform visualization (simulated)
        self.waveform_frame = ctk.CTkFrame(control_frame, fg_color="#0a0a0a", height=60)
        self.waveform_frame.pack(fill="x", padx=15, pady=10)

        self.waveform_label = ctk.CTkLabel(
            self.waveform_frame,
            text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            font=("Courier", 12),
            text_color="#444444"
        )
        self.waveform_label.pack(pady=15)

        # Recording time display
        self.recording_time_label = ctk.CTkLabel(
            control_frame,
            text="00:00",
            font=("Courier", 14, "bold"),
            text_color=self.primary_color
        )
        self.recording_time_label.pack(pady=5)

        # Button container
        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.pack(pady=15)

        # Record button
        self.record_button = ctk.CTkButton(
            button_frame,
            text="🎙️ START RECORDING",
            command=self.toggle_recording,
            font=("Helvetica", 13, "bold"),
            fg_color=self.success_color,
            hover_color="#66bb6a",
            text_color="white",
            width=200,
            height=50
        )
        self.record_button.pack(side="left", padx=5)

        # Text input alternative
        self.text_input = ctk.CTkEntry(
            button_frame,
            placeholder_text="Or type a command here...",
            font=("Helvetica", 12),
            height=50,
            width=350
        )
        self.text_input.pack(side="left", padx=5)
        self.text_input.bind("<Return>", lambda e: self.process_text_command())

        # Submit button
        self.submit_button = ctk.CTkButton(
            button_frame,
            text="SUBMIT",
            command=self.process_text_command,
            font=("Helvetica", 12, "bold"),
            fg_color=self.primary_color,
            hover_color=self.secondary_color,
            text_color="white",
            width=100,
            height=50
        )
        self.submit_button.pack(side="left", padx=5)

    def _build_output_display(self, parent):
        """Build output display section."""
        display_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=15)
        display_frame.pack(fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            display_frame,
            text="📊 Command Output",
            font=("Helvetica", 16, "bold"),
            text_color=self.accent_color
        )
        title.pack(pady=(15, 10), padx=15, anchor="w")

        # Output text area
        self.output_display = ctk.CTkTextbox(
            display_frame,
            font=("Courier", 11),
            fg_color="#0a0a0a",
            text_color="#00ff00",
            border_color="#333333",
            corner_radius=10
        )
        self.output_display.pack(fill="both", expand=True, padx=15, pady=15)

        # Add initial text
        self.output_display.insert("0.0", "JARVIS Ready for Commands\n")
        self.output_display.configure(state="disabled")

    def _build_command_history(self, parent):
        """Build command history section."""
        history_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=15)
        history_frame.pack(fill="both", expand=True, pady=(0, 15))

        # Title
        title = ctk.CTkLabel(
            history_frame,
            text="📜 Command History",
            font=("Helvetica", 14, "bold"),
            text_color=self.accent_color
        )
        title.pack(pady=(10, 5), padx=10, anchor="w")

        # History listbox with scrollbar
        scrollbar_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
        scrollbar_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.history_listbox = ctk.CTkTextbox(
            scrollbar_frame,
            font=("Courier", 9),
            fg_color="#0a0a0a",
            text_color="#bbdefb",
            border_color="#333333",
            corner_radius=8,
            height=250
        )
        self.history_listbox.pack(fill="both", expand=True)
        self.history_listbox.configure(state="disabled")

        # Clear history button
        clear_button = ctk.CTkButton(
            history_frame,
            text="Clear History",
            command=self.clear_history,
            font=("Helvetica", 10),
            fg_color="#666666",
            hover_color="#777777",
            text_color="white",
            height=30
        )
        clear_button.pack(fill="x", padx=10, pady=(0, 10))

    def _build_suggestions(self, parent):
        """Build command suggestions section."""
        suggestions_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=15)
        suggestions_frame.pack(fill="x")

        # Title
        title = ctk.CTkLabel(
            suggestions_frame,
            text="💡 Quick Commands",
            font=("Helvetica", 14, "bold"),
            text_color=self.accent_color
        )
        title.pack(pady=(10, 5), padx=10, anchor="w")

        # Suggestion buttons
        suggestions = [
            ("🎵 Play Music", "Play despacito on YouTube"),
            ("🔍 Google Search", "Search python programming on Google"),
            ("📘 Open Facebook", "Open facebook"),
            ("💬 Open Discord", "Open discord"),
            ("❓ Get Help", "Help"),
        ]

        button_frame = ctk.CTkFrame(suggestions_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=10)

        for emoji, command in suggestions:
            btn = ctk.CTkButton(
                button_frame,
                text=emoji,
                command=lambda cmd=command: self.execute_suggestion(cmd),
                font=("Helvetica", 9),
                fg_color="#333333",
                hover_color="#444444",
                text_color="white",
                height=35,
                corner_radius=8
            )
            btn.pack(fill="x", pady=3)

    def _build_footer(self, parent):
        """Build the footer section."""
        footer = ctk.CTkFrame(parent, fg_color="#0a0a0a", height=40)
        footer.pack(fill="x", pady=(20, 0))

        # Status text
        self.footer_label = ctk.CTkLabel(
            footer,
            text="Ready to assist",
            font=("Helvetica", 10),
            text_color="#666666"
        )
        self.footer_label.pack(side="left", padx=20, pady=10)

        # Exit button
        exit_button = ctk.CTkButton(
            footer,
            text="⏻ Exit",
            command=self.quit,
            font=("Helvetica", 10, "bold"),
            fg_color=self.error_color,
            hover_color="#e53935",
            text_color="white",
            width=80,
            height=30
        )
        exit_button.pack(side="right", padx=20, pady=10)

    # Event Handlers

    def toggle_recording(self):
        """Toggle voice recording."""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        """Start voice recording in a separate thread."""
        self.is_recording = True
        self.record_button.configure(
            text="🛑 STOP RECORDING",
            fg_color=self.error_color,
            hover_color="#e53935"
        )
        self.status_indicator.configure(text="● LISTENING", text_color="#ffeb3b")

        # Run recording in background thread
        thread = threading.Thread(target=self._record_voice, daemon=True)
        thread.start()

    def _record_voice(self):
        """Record voice input in background."""
        try:
            command = self.voice_engine.listen(timeout=10, phrase_time_limit=10)
            self.is_recording = False

            if command:
                self.process_command(command)
        except Exception as e:
            self.append_output(f"Recording error: {e}")
        finally:
            self.is_recording = False
            self.record_button.configure(
                text="🎙️ START RECORDING",
                fg_color=self.success_color,
                hover_color="#66bb6a"
            )
            self.status_indicator.configure(text="● READY", text_color=self.success_color)

    def stop_recording(self):
        """Stop voice recording."""
        self.is_recording = False

    def process_text_command(self):
        """Process text command from input field."""
        command = self.text_input.get().strip()
        if command:
            self.process_command(command)
            self.text_input.delete(0, "end")

    def process_command(self, command: str):
        """Process a command and display results."""
        self.append_output(f"\n👤 You: {command}\n")

        # Process in background thread
        thread = threading.Thread(
            target=self._process_command_async,
            args=(command,),
            daemon=True
        )
        thread.start()

    def _process_command_async(self, command: str):
        """Process command asynchronously."""
        try:
            self.is_processing = True
            self.status_indicator.configure(text="● PROCESSING", text_color="#ff9800")

            response = self.command_processor.process(command)

            self.command_history.add(command, response or "")
            self.append_output(f"🤖 JARVIS: {response}\n")

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.append_output(f"🤖 JARVIS: {error_msg}\n")
        finally:
            self.is_processing = False
            self.status_indicator.configure(text="● READY", text_color=self.success_color)
            self._refresh_history_display()

    def execute_suggestion(self, command: str):
        """Execute a suggested command."""
        self.process_command(command)

    def append_output(self, text: str):
        """Append text to output display."""
        self.output_display.configure(state="normal")
        self.output_display.insert("end", text)
        self.output_display.see("end")
        self.output_display.configure(state="disabled")

    def _refresh_history_display(self):
        """Refresh the history display."""
        self.history_listbox.configure(state="normal")
        self.history_listbox.delete("0.0", "end")

        for item in reversed(self.command_history.get_last(20)):
            timestamp = item.get("timestamp", "")
            command = item.get("command", "")
            self.history_listbox.insert("end", f"[{timestamp}]\n{command}\n\n")

        self.history_listbox.configure(state="disabled")

    def clear_history(self):
        """Clear command history."""
        self.command_history.history.clear()
        self._refresh_history_display()
        self.append_output("\n🗑️  History cleared.\n")

    def on_closing(self):
        """Handle window closing."""
        self.command_history.save_to_file()
        self.quit()


def main():
    """Main entry point for GUI application."""
    app = JARVISGUIApp()
    app.mainloop()


if __name__ == "__main__":
    main()
