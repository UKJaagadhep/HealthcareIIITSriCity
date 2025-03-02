import azure.cognitiveservices.speech as speechsdk
import threading
import time
from notify_emergency import notifyEmerg

class Transcription:
    def _init_(self):
        # Ensure API keys are set correctly
        self.AZURE_SPEECH_KEY = "447qXmyKhJSXcdn4IWNmaMJ5zyyifVhiFrVgxafGMdbpY163ikL4JQQJ99BCACHYHv6XJ3w3AAAAACOGBIP4"
        self.AZURE_SERVICE_REGION = "eastus2"

        # Initialize speech configuration
        self.speech_config = speechsdk.SpeechConfig(subscription=self.AZURE_SPEECH_KEY, region=self.AZURE_SERVICE_REGION)
        self.speech_config.speech_recognition_language = "en-US"

        self.notifier = notifyEmerg()
        self.stop_event = threading.Event()

    def real_time_transcription(self):
        if not hasattr(self, "speech_config"):
            raise RuntimeError("speech_config was not initialized!")

        # Initialize audio configuration
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        transcribed_text = []

        def recognized_callback(evt):
            """Handle recognized speech."""
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                recognized_text = evt.result.text.strip()
                print(f"Transcription: {recognized_text}")
                transcribed_text.append(recognized_text)

                if "stop transcription" in recognized_text.lower():
                    print("Detected 'stop transcription', stopping...")
                    self.stop_event.set()

                if "notify emergency" in recognized_text.lower():
                    self.notifier.notify_emergency()

        def stop_callback(evt):
            """Handle session stop events."""
            print("Recognition session stopped.")
            self.stop_event.set()

        # Connect event handlers
        speech_recognizer.recognized.connect(recognized_callback)
        speech_recognizer.session_stopped.connect(stop_callback)

        print("Listening... (Say 'stop transcription' to stop)")
        speech_recognizer.start_continuous_recognition()

        self.stop_event.wait()  # Wait for stop event

        speech_recognizer.stop_continuous_recognition()

        return " ".join(transcribed_text)  # Return final transcription
