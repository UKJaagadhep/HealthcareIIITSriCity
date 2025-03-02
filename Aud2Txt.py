print("Azure Speech SDK is installed and working!")
import azure.cognitiveservices.speech as speechsdk
import time
import threading
from notify_emergency import notifyEmerg

class Transcription():
    def __init__(self):
        AZURE_SPEECH_KEY = "447qXmyKhJSXcdn4IWNmaMJ5zyyifVhiFrVgxafGMdbpY163ikL4JQQJ99BCACHYHv6XJ3w3AAAAACOGBIP4"
        AZURE_SERVICE_REGION = "eastus2"

        self.speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SERVICE_REGION)
        self.speech_config.speech_recognition_language = "en-US"  

        self.notifier = notifyEmerg()

    def real_time_transcription(self):
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        transcribed_text = ""  
        last_recognition_time = time.time() 
        pause_threshold = 3  
        stop_transcription = False  

        def recognized_callback(evt):
            nonlocal transcribed_text, last_recognition_time, stop_transcription
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                last_recognition_time = time.time()
                recognized_text = evt.result.text.strip()

                if 'stop transcription' not in recognized_text.lower():
                    transcribed_text += recognized_text + " " 
                    print(f"Transcription: {recognized_text}")

                if 'stop transcription' in recognized_text.lower():
                    stop_transcription = True
                    print("Detected 'stop transcription', stopping transcription.")

                if 'notify emergency' in recognized_text.lower():
                    self.notifier.notify_emergency()
        speech_recognizer.recognized.connect(recognized_callback)

        def stop_callback(evt):
            nonlocal transcribed_text
            if evt.result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized.")
            elif evt.result.reason == speechsdk.ResultReason.Canceled:
                print(f"Recognition canceled: {evt.result.cancellation_details.error_details}")

        speech_recognizer.session_stopped.connect(stop_callback)

        print("Listening... (Say 'stop transcription' to stop)")

        speech_recognizer.start_continuous_recognition()

        try:
            while not stop_transcription:
                if time.time() - last_recognition_time > pause_threshold:
                    time.sleep(0.5)  
        except KeyboardInterrupt:
            print("Stopping transcription due to KeyboardInterrupt...")
            stop_transcription = True

        speech_recognizer.stop_continuous_recognition()

        return transcribed_text.strip() 


