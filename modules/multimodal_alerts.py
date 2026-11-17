
import pandas as pd


def build_multimodal_alerts(
    audio_result=None,
    video_result=None,
    vital_result=None,
    prescription_result=None
):
    alerts = []
    modules = []

    def add_alert(source, category, severity, description):
        alerts.append({
            "Origem": source,
            "Categoria": category,
            "Prioridade": severity,
            "Descrição": description
        })

    # 1. Áudio
    if audio_result:
        modules.append("Áudio")

        audio_alerts = audio_result.get("alerts", [])

        for item in audio_alerts:
            if isinstance(item, dict):
                add_alert(
                    "Áudio",
                    item.get("category", "Termo crítico"),
                    item.get("severity", "Atenção"),
                    item.get(
                        "message",
                        f"Expressão identificada: {item.get('term', 'Não especificada')}"
                    )
                )

    # 2. Vídeo

    # 2. Vídeo
    if video_result:
        modules.append("Vídeo")

        summary = video_result.get("summary", video_result)

        if isinstance(summary, dict):
            repetitions = summary.get("repetitions", [])

            for repetition in repetitions:
                status = str(repetition.get("status", "")).lower()

                is_discrepant = (
                    repetition.get("is_discrepant", False)
                    or repetition.get("discrepant", False)
                    or "discrep" in status
                    or "inconsist" in status
                )

                if is_discrepant:
                    repetition_number = repetition.get(
                        "repetition",
                        repetition.get("number", "?")
                    )

                    rom = repetition.get("rom")
                    variation = repetition.get("variation")

                    details = (
                        f"Repetição {repetition_number} apresentou "
                        "amplitude discrepante."
                    )

                    if rom is not None:
                        details += f" Amplitude (ROM): {rom:.1f}°."

                    if variation is not None:
                        details += f" Variação: {variation:.1f}%."

                    add_alert(
                        "Vídeo",
                        "Discrepância de movimento",
                        "Atenção",
                        details
                    )


    # 3. Sinais vitais
    if vital_result:
        modules.append("Sinais vitais")

        vital_data = vital_result.get("data")

        if isinstance(vital_data, pd.DataFrame):
            anomalies = vital_data[
                vital_data["is_anomaly"] == True
            ]

            for _, row in anomalies.iterrows():
                add_alert(
                    "Sinais vitais",
                    "Anomalia estatística",
                    "Atenção",
                    (
                        f"FC: {row['fc']:.1f} bpm | "
                        f"Pressão: {row['pas']:.1f}/{row['pad']:.1f} mmHg | "
                        f"SpO₂: {row['spo2']:.1f}%"
                    )
                )

    # 4. Prescrições
    if prescription_result:
        modules.append("Prescrições")

        prescription_data = prescription_result.get("data")

        if isinstance(prescription_data, pd.DataFrame):
            attention = prescription_data[
                prescription_data["status"] != "Conforme registro"
            ]

            for _, row in attention.iterrows():
                add_alert(
                    "Prescrições",
                    row["status"],
                    "Atenção",
                    f"{row['medication']}: {row['details']}"
                )

    return {
        "modules_analyzed": modules,
        "total_modules": len(modules),
        "alerts": pd.DataFrame(alerts),
        "total_alerts": len(alerts)
    }
