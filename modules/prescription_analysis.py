
import pandas as pd


def generate_prescription_data():
    """Gera prescrições e registros simulados de administração."""

    prescriptions = pd.DataFrame([
        {
            "medication": "Paracetamol",
            "prescribed_dose": "750 mg",
            "prescribed_time": "08:00",
            "frequency": "8/8 horas"
        },
        {
            "medication": "Dipirona",
            "prescribed_dose": "500 mg",
            "prescribed_time": "09:00",
            "frequency": "6/6 horas"
        },
        {
            "medication": "Omeprazol",
            "prescribed_dose": "20 mg",
            "prescribed_time": "10:00",
            "frequency": "1 vez ao dia"
        },
        {
            "medication": "Amoxicilina",
            "prescribed_dose": "500 mg",
            "prescribed_time": "11:00",
            "frequency": "8/8 horas"
        },
        {
            "medication": "Losartana",
            "prescribed_dose": "50 mg",
            "prescribed_time": "12:00",
            "frequency": "1 vez ao dia"
        }
    ])

    administrations = pd.DataFrame([
        {
            "medication": "Paracetamol",
            "administered_dose": "750 mg",
            "administered_time": "08:05",
            "status": "Administrado"
        },
        {
            "medication": "Dipirona",
            "administered_dose": "500 mg",
            "administered_time": "09:45",
            "status": "Administrado"
        },
        {
            "medication": "Omeprazol",
            "administered_dose": "-",
            "administered_time": "-",
            "status": "Não administrado"
        },
        {
            "medication": "Amoxicilina",
            "administered_dose": "250 mg",
            "administered_time": "11:05",
            "status": "Administrado"
        },
        {
            "medication": "Losartana",
            "administered_dose": "50 mg",
            "administered_time": "12:10",
            "status": "Administrado"
        },
        {
            "medication": "Ibuprofeno",
            "administered_dose": "400 mg",
            "administered_time": "13:00",
            "status": "Administrado"
        }
    ])

    return prescriptions, administrations


def analyze_prescriptions():
    """Compara prescrições com registros de administração."""

    prescriptions, administrations = generate_prescription_data()

    results = []

    for _, prescription in prescriptions.iterrows():
        medication = prescription["medication"]

        records = administrations[
            administrations["medication"] == medication
        ]

        if records.empty:
            status = "Sem registro de administração"
            details = "Não foi encontrado registro para o medicamento."
        else:
            administration = records.iloc[0]

            if administration["status"] == "Não administrado":
                status = "Não administrado"
                details = "Medicamento prescrito sem registro de administração."

            elif administration["administered_dose"] != prescription["prescribed_dose"]:
                status = "Dose divergente"
                details = (
                    f"Prescrito: {prescription['prescribed_dose']} | "
                    f"Administrado: {administration['administered_dose']}"
                )

            else:
                prescribed_minutes = (
                    int(prescription["prescribed_time"][:2]) * 60
                    + int(prescription["prescribed_time"][3:])
                )

                administered_minutes = (
                    int(administration["administered_time"][:2]) * 60
                    + int(administration["administered_time"][3:])
                )

                delay = administered_minutes - prescribed_minutes

                if delay > 30:
                    status = "Administração atrasada"
                    details = f"Atraso de {delay} minutos."
                else:
                    status = "Conforme registro"
                    details = "Dose e horário dentro dos critérios definidos."

        results.append({
            "medication": medication,
            "prescribed_dose": prescription["prescribed_dose"],
            "prescribed_time": prescription["prescribed_time"],
            "status": status,
            "details": details
        })

    # Identifica medicamentos administrados sem prescrição correspondente.
    prescribed_names = set(prescriptions["medication"])

    for _, administration in administrations.iterrows():
        if administration["medication"] not in prescribed_names:
            results.append({
                "medication": administration["medication"],
                "prescribed_dose": "-",
                "prescribed_time": "-",
                "status": "Sem prescrição",
                "details": "Administração registrada sem prescrição correspondente."
            })

    result_df = pd.DataFrame(results)

    return {
        "data": result_df,
        "total": len(result_df),
        "alerts": int(
            (result_df["status"] != "Conforme registro").sum()
        )
    }
