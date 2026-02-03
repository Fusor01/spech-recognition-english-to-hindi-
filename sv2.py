

import azure.cognitiveservices.speech as speechsdk

# ===== Azure Credentials =====
speech_key = "key_here"   # replace with your Azure Speech service key
service_region = "region_here"   # e.g. centralindia, eastus

# ===== Translation Config =====
translation_config = speechsdk.translation.SpeechTranslationConfig(
    subscription=speech_key,
    region=service_region
)

translation_config.speech_recognition_language = "en-IN"
translation_config.add_target_language("hi")

# Hindi neural voice (speaker output)
translation_config.voice_name = "hi-IN-SwaraNeural"

# ===== Audio Input & Output =====
audio_input = speechsdk.audio.AudioConfig(use_default_microphone=True)
audio_output = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# ===== Translator =====
translator = speechsdk.translation.TranslationRecognizer(
    translation_config=translation_config,
    audio_config=audio_input
)

print("🎤 Speak English — Hindi voice will play on speaker 🔊")

def recognized_handler(evt):
    if evt.result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("Hindi:", evt.result.translations["hi"])

translator.recognized.connect(recognized_handler)

translator.start_continuous_recognition()

try:
    while True:
        pass
except KeyboardInterrupt:
    translator.stop_continuous_recognition()
    print("\nStopped.")
