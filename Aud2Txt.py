import azure.cognitiveservices.speech as speechsdk
import os
from notify_emergency import notifyEmerg

# Azure Speech Config
AZURE_SPEECH_KEY = "447qXmyKhJSXcdn4IWNmaMJ5zyyifVhiFrVgxafGMdbpY163ikL4JQQJ99BCACHYHv6XJ3w3AAAAACOGBIP4"
AZURE_SERVICE_REGION = "eastus2"

# Initialize Speech SDK
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SERVICE_REGION)
speech_config.speech_recognition_language = "en-US"  # Change if needed

class Transcription:
    def _init_(self):
        self.notifier = notifyEmerg()
        self.stop_transcription = False

    def real_time_transcription(self):
        # Use the default system microphone
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        def recognized_callback(evt):
            """Callback for recognized speech"""
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                recognized_text = evt.result.text.strip()
                print(f"Transcription: {recognized_text}")

                if 'stop transcription' in recognized_text.lower():
                    self.stop_transcription = True
                    print("Stopping transcription...")
                    speech_recognizer.stop_continuous_recognition()

                if 'notify emergency' in recognized_text.lower():
                    self.notifier.notify_emergency()

        # Event handlers for live speech recognition
        speech_recognizer.recognized.connect(recognized_callback)
        
        print("Listening... (Say 'stop transcription' to stop)")
        speech_recognizer.start_continuous_recognition()

        try:
            while not self.stop_transcription:
                pass  # Keep running indefinitely
        except KeyboardInterrupt:
            print("Stopping transcription manually...")
            speech_recognizer.stop_continuous_recognition()

# Run real-time transcription
if _name_ == "_main_":
    t = Transcription()
    t.real_time_transcription()
