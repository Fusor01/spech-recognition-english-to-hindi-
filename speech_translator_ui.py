import azure.cognitiveservices.speech as speechsdk
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from datetime import datetime

class SpeechTranslatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 English to Hindi Speech Translator")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")
        
        # Translation state
        self.is_translating = False
        self.translator = None
        
        # Azure Credentials
        self.speech_key = "key_here"
        self.service_region = "region_here"
        
        self.setup_ui()
        self.setup_translator()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(
            main_frame,
            text="🎤 English → Hindi Speech Translator",
            font=("Segoe UI", 24, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        title.pack(pady=(0, 20))
        
        # Status indicator
        status_frame = tk.Frame(main_frame, bg="#1e1e1e")
        status_frame.pack(pady=(0, 10))
        
        self.status_indicator = tk.Canvas(
            status_frame,
            width=20,
            height=20,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 10))
        self.status_circle = self.status_indicator.create_oval(
            2, 2, 18, 18,
            fill="#666666",
            outline=""
        )
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to start",
            font=("Segoe UI", 12),
            bg="#1e1e1e",
            fg="#cccccc"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg="#1e1e1e")
        button_frame.pack(pady=(0, 20))
        
        self.start_button = tk.Button(
            button_frame,
            text="▶ Start Translation",
            font=("Segoe UI", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.start_translation
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="⏹ Stop Translation",
            font=("Segoe UI", 14, "bold"),
            bg="#f44336",
            fg="white",
            activebackground="#da190b",
            activeforeground="white",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.stop_translation,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(
            button_frame,
            text="🗑 Clear",
            font=("Segoe UI", 14),
            bg="#555555",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.clear_text
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Translation display
        display_frame = tk.Frame(main_frame, bg="#1e1e1e")
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # English input section
        english_label = tk.Label(
            display_frame,
            text="English (Recognized)",
            font=("Segoe UI", 12, "bold"),
            bg="#1e1e1e",
            fg="#64B5F6",
            anchor="w"
        )
        english_label.pack(fill=tk.X, pady=(0, 5))
        
        self.english_text = scrolledtext.ScrolledText(
            display_frame,
            font=("Consolas", 11),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="white",
            relief=tk.FLAT,
            wrap=tk.WORD,
            height=8
        )
        self.english_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Hindi output section
        hindi_label = tk.Label(
            display_frame,
            text="हिंदी (Translation)",
            font=("Segoe UI", 12, "bold"),
            bg="#1e1e1e",
            fg="#81C784",
            anchor="w"
        )
        hindi_label.pack(fill=tk.X, pady=(0, 5))
        
        self.hindi_text = scrolledtext.ScrolledText(
            display_frame,
            font=("Nirmala UI", 12),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="white",
            relief=tk.FLAT,
            wrap=tk.WORD,
            height=8
        )
        self.hindi_text.pack(fill=tk.BOTH, expand=True)
        
        # Footer info
        footer = tk.Label(
            main_frame,
            text="💡 Speak English into your microphone • Hindi translation plays through speaker",
            font=("Segoe UI", 9),
            bg="#1e1e1e",
            fg="#888888"
        )
        footer.pack(pady=(15, 0))
        
    def setup_translator(self):
        """Initialize Azure Speech Translator"""
        try:
            # Translation Config
            translation_config = speechsdk.translation.SpeechTranslationConfig(
                subscription=self.speech_key,
                region=self.service_region
            )
            
            translation_config.speech_recognition_language = "en-IN"
            translation_config.add_target_language("hi")
            translation_config.voice_name = "hi-IN-SwaraNeural"
            
            # Audio Config
            audio_input = speechsdk.audio.AudioConfig(use_default_microphone=True)
            
            # Create Translator
            self.translator = speechsdk.translation.TranslationRecognizer(
                translation_config=translation_config,
                audio_config=audio_input
            )
            
            # Connect event handlers
            self.translator.recognized.connect(self.recognized_handler)
            self.translator.recognizing.connect(self.recognizing_handler)
            self.translator.canceled.connect(self.canceled_handler)
            
        except Exception as e:
            self.append_to_display("english", f"Error initializing translator: {str(e)}\n", "red")
    
    def recognized_handler(self, evt):
        """Handle recognized speech events"""
        if evt.result.reason == speechsdk.ResultReason.TranslatedSpeech:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Display English
            english_text = evt.result.text
            if english_text:
                self.append_to_display(
                    "english",
                    f"[{timestamp}] {english_text}\n",
                    "#64B5F6"
                )
            
            # Display Hindi
            hindi_translation = evt.result.translations.get("hi", "")
            if hindi_translation:
                self.append_to_display(
                    "hindi",
                    f"[{timestamp}] {hindi_translation}\n",
                    "#81C784"
                )
                
                # Synthesize Hindi speech
                self.synthesize_hindi_speech(hindi_translation)
    
    def recognizing_handler(self, evt):
        """Handle interim recognition results"""
        pass  # Optionally show real-time recognition
    
    def canceled_handler(self, evt):
        """Handle cancellation events"""
        if evt.reason == speechsdk.CancellationReason.Error:
            error_msg = f"Error: {evt.error_details}\n"
            self.append_to_display("english", error_msg, "#f44336")
            self.root.after(0, self.stop_translation)
    
    def synthesize_hindi_speech(self, text):
        """Synthesize and play Hindi speech"""
        def synthesize():
            try:
                speech_config = speechsdk.SpeechConfig(
                    subscription=self.speech_key,
                    region=self.service_region
                )
                speech_config.speech_synthesis_voice_name = "hi-IN-SwaraNeural"
                
                audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
                synthesizer = speechsdk.SpeechSynthesizer(
                    speech_config=speech_config,
                    audio_config=audio_config
                )
                
                synthesizer.speak_text_async(text)
            except Exception as e:
                print(f"Synthesis error: {e}")
        
        # Run synthesis in separate thread
        threading.Thread(target=synthesize, daemon=True).start()
    
    def append_to_display(self, field, text, color=None):
        """Append text to specified display field"""
        def update():
            text_widget = self.english_text if field == "english" else self.hindi_text
            text_widget.config(state=tk.NORMAL)
            
            if color:
                # Create tag for color
                tag_name = f"color_{color}"
                text_widget.tag_config(tag_name, foreground=color)
                text_widget.insert(tk.END, text, tag_name)
            else:
                text_widget.insert(tk.END, text)
            
            text_widget.see(tk.END)
            text_widget.config(state=tk.DISABLED)
        
        self.root.after(0, update)
    
    def update_status(self, status, color):
        """Update status indicator"""
        self.status_indicator.itemconfig(self.status_circle, fill=color)
        self.status_label.config(text=status)
    
    def start_translation(self):
        """Start continuous translation"""
        if not self.is_translating:
            try:
                self.translator.start_continuous_recognition()
                self.is_translating = True
                
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.update_status("🎤 Listening...", "#4CAF50")
                
                self.append_to_display("english", "═" * 50 + "\n", "#888888")
                self.append_to_display("english", "Translation started - Speak now!\n", "#4CAF50")
                self.append_to_display("english", "═" * 50 + "\n", "#888888")
                
            except Exception as e:
                self.append_to_display("english", f"Error starting translation: {str(e)}\n", "#f44336")
    
    def stop_translation(self):
        """Stop continuous translation"""
        if self.is_translating:
            try:
                self.translator.stop_continuous_recognition()
                self.is_translating = False
                
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                self.update_status("Stopped", "#666666")
                
                self.append_to_display("english", "═" * 50 + "\n", "#888888")
                self.append_to_display("english", "Translation stopped.\n", "#f44336")
                self.append_to_display("english", "═" * 50 + "\n", "#888888")
                
            except Exception as e:
                self.append_to_display("english", f"Error stopping translation: {str(e)}\n", "#f44336")
    
    def clear_text(self):
        """Clear all text displays"""
        self.english_text.config(state=tk.NORMAL)
        self.english_text.delete(1.0, tk.END)
        self.english_text.config(state=tk.DISABLED)
        
        self.hindi_text.config(state=tk.NORMAL)
        self.hindi_text.delete(1.0, tk.END)
        self.hindi_text.config(state=tk.DISABLED)
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_translating:
            self.stop_translation()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = SpeechTranslatorUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
