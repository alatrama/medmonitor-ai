
import re
import unicodedata


# Regras experimentais para identificação de termos

CLINICAL_RULES = {
    "Respiratório": {
        "severity": "Alta",
        "terms": [
            "falta de ar",
            "dificuldade para respirar",
            "dificuldade respiratória",
            "respiração acelerada",
            "respiração rápida",
            "não consigo respirar",
            "fôlego curto"
        ]
    },
    "Cardíaco": {
        "severity": "Alta",
        "terms": [
            "dor no peito",
            "dor torácica",
            "aperto no peito",
            "pressão no peito",
            "palpitação"
        ]
    },
    "Neurológico": {
        "severity": "Moderada",
        "terms": [
            "tontura",
            "desmaio",
            "confusão mental",
            "perda de consciência",
            "dificuldade para falar",
            "dor de cabeça",
            "cefaleia"
        ]
    },
    "Visual": {
        "severity": "Alta",
        "terms": [
            "não enxergo nada",
            "não consigo enxergar",
            "perda de visão",
            "perda da visão",
            "visão turva",
            "visão embaçada",
            "dificuldade para enxergar"
        ]
    },
    "Gastrointestinal": {
        "severity": "Moderada",
        "terms": [
            "dor de barriga",
            "dor abdominal",
            "dor no abdômen",
            "náusea",
            "vômito"
        ]
    },
    "Geral": {
        "severity": "Moderada",
        "terms": [
            "febre",
            "cansaço intenso",
            "fraqueza",
            "calafrios",
            "dor intensa"
        ]
    }
}



def normalize_text(text):
    text = text.lower().strip()

    text = unicodedata.normalize("NFD", text)
    text = "".join(
        char for char in text
        if unicodedata.category(char) != "Mn"
    )

    return re.sub(r"\s+", " ", text)


def detect_clinical_alerts(text):
    """
    Identifica expressões clínicas predefinidas.
    Não realiza diagnóstico médico.
    """

    normalized = normalize_text(text)

    alerts = []

    for category, config in CLINICAL_RULES.items():

        for term in config["terms"]:

            normalized_term = normalize_text(term)

            pattern = (
                r"(?<!\w)"
                + re.escape(normalized_term)
                + r"(?!\w)"
            )

            if re.search(pattern, normalized):

                alerts.append({
                    "category": category,
                    "term": term,
                    "severity": config["severity"],
                    "message": (
                        f"Expressão identificada: {term}"
                    )
                })

    # Evita duplicidade
    unique_alerts = []
    seen = set()

    for alert in alerts:
        key = (alert["category"], alert["term"])

        if key not in seen:
            unique_alerts.append(alert)
            seen.add(key)

    return unique_alerts


def generate_alert_summary(alerts):

    if not alerts:
        return {
            "status": "Sem termos identificados",
            "total": 0,
            "alerts": []
        }

    high = sum(
        1 for alert in alerts
        if alert["severity"] == "Alta"
    )

    moderate = sum(
        1 for alert in alerts
        if alert["severity"] == "Moderada"
    )

    if high:
        status = "Requer atenção prioritária"
    else:
        status = "Termos de atenção identificados"

    return {
        "status": status,
        "total": len(alerts),
        "high": high,
        "moderate": moderate,
        "alerts": alerts
    }
