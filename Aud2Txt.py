import azure.cognitiveservices.speech as speechsdk
import threading
import time
import asyncio
from notify_emergency import notifyEmerg

class Transcription:
    def _init_(self):
        try:
            self.AZURE_SPEECH_KEY = "447qXmyKhJSXcdn4IWNmaMJ5zyyifVhiFrVgxafGMdbpY163ikL4JQQJ99BCACHYHv6XJ3w3AAAAACOGBIP4"
            self.AZURE_SERVICE_REGION = "eastus2"

            # Ensure speech config is initialized correctly
            self.speech_config = speechsdk.SpeechConfig(subscription=self.AZURE_SPEECH_KEY, region=self.AZURE_SERVICE_REGION)
            self.speech_config.speech_recognition_language = "en-US"

            self.notifier = notifyEmerg()
            self.stop_event = threading.Event()
        except Exception as e:
            print(f"Error initializing Transcription: {e}")
            raise  # Ensure the exception is raised for debugging

    def real_time_transcription(self):
        if not hasattr(self, "speech_config"):
            raise RuntimeError("speech_config was not initialized!")

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
                    print("Stopping transcription...")
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

        try:
            self.stop_event.wait()  # Use event-based waiting
        except KeyboardInterrupt:
            print("Stopping transcription due to KeyboardInterrupt...")
            self.stop_event.set()

        speech_recognizer.stop_continuous_recognition()
        return " ".join(transcribed_text)  # Return final transcription

# Fix for Streamlit asyncio issue
def run_transcription():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        trans = Transcription()
        return trans.real_time_transcription()
    except Exception as e:
        print(f"Error running transcription: {e}")
        return None
