# 🎤 English to Hindi Speech Translator

A modern GUI application for real-time speech translation from English to Hindi using Azure Cognitive Services.

## Features

- 🎙️ **Real-time Speech Recognition** - Continuous English speech recognition
- 🔊 **Audio Output** - Hindi translation plays through speakers
- 📝 **Live Display** - Shows both English input and Hindi translation
- 🎨 **Modern Dark UI** - Clean, professional interface
- ⏯️ **Easy Controls** - Start/Stop/Clear buttons
- 📍 **Timestamps** - Track when each translation occurred

## Prerequisites

- Python 3.7+
- Microphone access
- Speaker/headphones for audio output
- Active Azure Cognitive Services subscription

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Update Azure credentials (if needed):**
   - Open `speech_translator_ui.py`
   - Update `speech_key` and `service_region` variables with your Azure credentials

## Usage

1. **Run the application:**
```bash
python speech_translator_ui.py
```

2. **Using the translator:**
   - Click **"▶ Start Translation"** to begin
   - Speak in English into your microphone
   - Watch the English text appear in the top panel
   - See the Hindi translation in the bottom panel
   - Hear the Hindi translation through your speakers
   - Click **"⏹ Stop Translation"** when done
   - Use **"🗑 Clear"** to clear all text

## Interface Components

### Status Indicator
- 🔴 Red: Error state
- 🟢 Green: Actively listening
- ⚪ Gray: Stopped/Ready

### Text Panels
- **Top Panel (Blue)**: Recognized English speech
- **Bottom Panel (Green)**: Hindi translation

### Controls
- **Start Translation**: Begin listening and translating
- **Stop Translation**: Stop the translation service
- **Clear**: Remove all text from displays

## Configuration

### Supported Languages
- **Source**: English (India) - `en-IN`
- **Target**: Hindi - `hi`

### Voice
- Hindi Neural Voice: `hi-IN-SwaraNeural`

### To Change Languages/Voice:
Edit these lines in the code:
```python
translation_config.speech_recognition_language = "en-IN"  # Source language
translation_config.add_target_language("hi")              # Target language
translation_config.voice_name = "hi-IN-SwaraNeural"       # Voice for output
```

## Troubleshooting

### No microphone input
- Check microphone permissions
- Ensure microphone is set as default input device
- Test microphone in system settings

### No audio output
- Check speaker/headphone connection
- Verify default audio output device
- Check system volume settings

### Translation errors
- Verify Azure credentials are valid
- Check internet connection
- Ensure subscription has available quota

### Recognition issues
- Speak clearly and at normal pace
- Reduce background noise
- Ensure microphone is close enough

## Azure Service Regions

Common regions:
- `southeastasia` - Southeast Asia
- `centralindia` - Central India
- `eastus` - East US
- `westeurope` - West Europe

## Notes

- The app requires continuous internet connection
- Translation and synthesis happen in real-time
- Each session is independent (no conversation history)
- Press Ctrl+C or close window to exit

## Credits

Built with:
- Azure Cognitive Services Speech SDK
- Python tkinter for GUI
- Threading for async operations

---
**Note**: Remember to keep your Azure credentials secure and never commit them to public repositories!
