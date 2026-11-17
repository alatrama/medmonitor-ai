
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def generate_vital_signs(n_samples=120, random_state=42):
    """Gera uma série temporal sintética de sinais vitais."""

    rng = np.random.default_rng(random_state)

    timestamps = pd.date_range(
        end=pd.Timestamp.now().floor("min"),
        periods=n_samples,
        freq="5min"
    )

    data = pd.DataFrame({
        "timestamp": timestamps,
        "fc": rng.normal(78, 5, n_samples).clip(55, 105),
        "pas": rng.normal(120, 7, n_samples).clip(95, 145),
        "pad": rng.normal(80, 5, n_samples).clip(60, 95),
        "spo2": rng.normal(97, 1, n_samples).clip(94, 100)
    })

    # Injeta alterações artificiais para testar a detecção.
    anomaly_indices = rng.choice(
        np.arange(10, n_samples),
        size=max(1, int(n_samples * 0.07)),
        replace=False
    )

    for index in anomaly_indices:
        scenario = rng.integers(0, 4)

        if scenario == 0:
            data.loc[index, "fc"] = rng.uniform(125, 150)
        elif scenario == 1:
            data.loc[index, "spo2"] = rng.uniform(85, 90)
        elif scenario == 2:
            data.loc[index, "pas"] = rng.uniform(165, 190)
        else:
            data.loc[index, "fc"] = rng.uniform(45, 52)
            data.loc[index, "spo2"] = rng.uniform(88, 92)

    return data


def detect_vital_anomalies(data):
    """Identifica medições atípicas com Isolation Forest."""

    result = data.copy()

    features = ["fc", "pas", "pad", "spo2"]

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("isolation_forest", IsolationForest(
            contamination=0.07,
            random_state=42,
            n_estimators=150
        ))
    ])

    predictions = model.fit_predict(result[features])

    result["is_anomaly"] = predictions == -1
    result["status"] = np.where(
        result["is_anomaly"],
        "Anomalia detectada",
        "Dentro do padrão"
    )

    return result


def analyze_vital_signs():
    """Executa a geração e a análise dos sinais vitais."""

    data = generate_vital_signs()
    analyzed = detect_vital_anomalies(data)

    return {
        "data": analyzed,
        "total_records": len(analyzed),
        "total_anomalies": int(analyzed["is_anomaly"].sum()),
        "anomaly_percentage": round(
            analyzed["is_anomaly"].mean() * 100, 1
        )
    }
