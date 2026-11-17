
import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()


def get_language_client():
    key = os.getenv("AZURE_LANGUAGE_KEY", "").strip()
    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT", "").strip()

    if not key or not endpoint:
        raise ValueError("Credenciais do Azure Language não encontradas no .env")

    return TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )


def analyze_text(text):
    """
    Analisa texto em português usando Azure AI Language.
    Retorna sentimento, frases-chave e entidades.
    """

    if not text or not text.strip():
        raise ValueError("O texto para análise está vazio.")

    client = get_language_client()

    documents = [text.strip()]

    # Análise de sentimento
    sentiment_result = client.analyze_sentiment(
        documents,
        language="pt"
    )[0]

    # Extração de frases-chave
    key_phrases_result = client.extract_key_phrases(
        documents,
        language="pt"
    )[0]

    # Reconhecimento de entidades
    entities_result = client.recognize_entities(
        documents,
        language="pt"
    )[0]

    if sentiment_result.is_error:
        sentiment = "Não identificado"
        confidence = {}
    else:
        sentiment = sentiment_result.sentiment
        confidence = sentiment_result.confidence_scores

    if key_phrases_result.is_error:
        key_phrases = []
    else:
        key_phrases = key_phrases_result.key_phrases

    if entities_result.is_error:
        entities = []
    else:
        entities = [
            {
                "text": entity.text,
                "category": entity.category,
                "subcategory": entity.subcategory
            }
            for entity in entities_result.entities
        ]

    return {
        "success": True,
        "sentiment": str(sentiment),
        "confidence": {
            "positive": confidence.positive,
            "neutral": confidence.neutral,
            "negative": confidence.negative
        } if confidence else {},
        "key_phrases": key_phrases,
        "entities": entities
    }
