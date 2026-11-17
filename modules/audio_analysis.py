
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()


def transcribe_audio(audio_path):
    """
    Transcreve um arquivo de áudio usando Azure Speech.
    Idioma: Português brasileiro.
    """

    speech_key = os.getenv("AZURE_SPEECH_KEY", "").strip().strip('"').strip("'")
    speech_region = os.getenv("AZURE_SPEECH_REGION", "").strip().strip('"').strip("'")

    if not speech_key or not speech_region:
        raise ValueError(
            "Configure AZURE_SPEECH_KEY e AZURE_SPEECH_REGION no arquivo .env"
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=speech_region
    )

    speech_config.speech_recognition_language = "pt-BR"

    audio_config = speechsdk.audio.AudioConfig(
        filename=audio_path
    )

    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    result = recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return {
            "success": True,
            "transcription": result.text,
            "message": "Transcrição realizada com sucesso."
        }

    if result.reason == speechsdk.ResultReason.NoMatch:
        return {
            "success": False,
            "transcription": "",
            "message": "Nenhuma fala foi identificada no áudio."
        }

    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details

        return {
            "success": False,
            "transcription": "",
            "message": f"Transcrição cancelada: {cancellation.error_details}"
        }

    return {
        "success": False,
        "transcription": "",
        "message": "Não foi possível processar o áudio."
    }
