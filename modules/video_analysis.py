
import os
import csv
import cv2
import numpy as np

from ultralytics import YOLO


# ==========================================
# CONFIGURAÇÕES
# ==========================================

MODEL_NAME = "yolov8n-pose.pt"

KEYPOINTS = {
    "left": {
        "hip": 11,
        "knee": 13,
        "ankle": 15
    },
    "right": {
        "hip": 12,
        "knee": 14,
        "ankle": 16
    }
}

# Parâmetros experimentais para identificação
# de repetições de agachamento.
STANDING_THRESHOLD = 150
BOTTOM_THRESHOLD = 120

# Diferença mínima considerada para sinalizar
# uma repetição discrepante em relação à mediana.
VARIATION_THRESHOLD = 0.20


# ==========================================
# CÁLCULO DO ÂNGULO ARTICULAR
# ==========================================

def calculate_angle(a, b, c):

    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    ba = a - b
    bc = c - b

    denominator = (
        np.linalg.norm(ba) *
        np.linalg.norm(bc)
    )

    if denominator == 0:
        return None

    cosine = np.dot(ba, bc) / denominator
    cosine = np.clip(cosine, -1.0, 1.0)

    return float(np.degrees(np.arccos(cosine)))


# ==========================================
# IDENTIFICAÇÃO DOS ÂNGULOS
# ==========================================

def get_joint_angle(
    keypoints,
    confidences,
    side,
    min_confidence
):

    indices = KEYPOINTS[side]

    hip_idx = indices["hip"]
    knee_idx = indices["knee"]
    ankle_idx = indices["ankle"]

    required = [
        hip_idx,
        knee_idx,
        ankle_idx
    ]

    for idx in required:

        if confidences[idx] < min_confidence:
            return None

    hip = keypoints[hip_idx]
    knee = keypoints[knee_idx]
    ankle = keypoints[ankle_idx]

    return calculate_angle(
        hip,
        knee,
        ankle
    )


# ==========================================
# SUAVIZAÇÃO DOS ÂNGULOS
# ==========================================

def smooth_angles(values, window=5):

    values = np.array(values, dtype=float)

    if len(values) < window:
        return values.tolist()

    kernel = np.ones(window) / window

    smoothed = np.convolve(
        values,
        kernel,
        mode="same"
    )

    return smoothed.tolist()


# ==========================================
# IDENTIFICAÇÃO DAS REPETIÇÕES
# ==========================================

def detect_repetitions(
    frame_records,
    standing_threshold=STANDING_THRESHOLD,
    bottom_threshold=BOTTOM_THRESHOLD
):

    valid_records = [
        item for item in frame_records
        if item["mean_knee_angle"] is not None
    ]

    if not valid_records:
        return []

    raw_angles = [
        item["mean_knee_angle"]
        for item in valid_records
    ]

    smoothed = smooth_angles(raw_angles)

    repetitions = []

    in_squat = False

    current_rep = None

    max_angle_since_last_rep = None

    for index, angle in enumerate(smoothed):

        frame = valid_records[index]["frame"]

        if not in_squat:

            if max_angle_since_last_rep is None:
                max_angle_since_last_rep = angle
            else:
                max_angle_since_last_rep = max(
                    max_angle_since_last_rep,
                    angle
                )

            # Identifica a descida do agachamento.
            if angle <= bottom_threshold:

                in_squat = True

                baseline = max_angle_since_last_rep

                current_rep = {
                    "repetition": len(repetitions) + 1,
                    "start_frame": frame,
                    "end_frame": None,
                    "baseline_angle": baseline,
                    "minimum_angle": angle
                }

        else:

            current_rep["minimum_angle"] = min(
                current_rep["minimum_angle"],
                angle
            )

            # Identifica o retorno à posição elevada.
            if angle >= standing_threshold:

                current_rep["end_frame"] = frame

                current_rep["range_of_motion"] = (
                    current_rep["baseline_angle"] -
                    current_rep["minimum_angle"]
                )

                current_rep["range_of_motion"] = max(
                    0,
                    current_rep["range_of_motion"]
                )

                repetitions.append(current_rep)

                in_squat = False
                current_rep = None
                max_angle_since_last_rep = angle

    return repetitions


# ==========================================
# ANÁLISE DA CONSISTÊNCIA
# ==========================================

def analyze_consistency(repetitions):

    if not repetitions:
        return []

    amplitudes = [
        item["range_of_motion"]
        for item in repetitions
    ]

    median_rom = float(np.median(amplitudes))

    results = []

    for repetition in repetitions:

        rom = repetition["range_of_motion"]

        if median_rom > 0:

            variation = abs(
                rom - median_rom
            ) / median_rom

        else:

            variation = 0

        if (
            len(repetitions) >= 3
            and variation > VARIATION_THRESHOLD
        ):

            status = "AMPLITUDE DISCREPANTE"

        else:

            status = "SEM DISCREPÂNCIA IDENTIFICADA"

        results.append({
            **repetition,
            "median_amplitude": round(median_rom, 2),
            "variation_percent": round(
                variation * 100, 2
            ),
            "status": status
        })

    return results


# ==========================================
# PROCESSAMENTO DO VÍDEO
# ==========================================

def process_video(
    video_path,
    output_dir="outputs/processed_videos",
    confidence_threshold=0.4,
    rom_threshold=30.0
):

    os.makedirs(output_dir, exist_ok=True)

    output_video = os.path.join(
        output_dir,
        "video_analisado.mp4"
    )

    output_csv = os.path.join(
        output_dir,
        "relatorio_movimentos.csv"
    )

    model = YOLO(MODEL_NAME)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(
            "Não foi possível abrir o vídeo."
        )

    fps = cap.get(cv2.CAP_PROP_FPS)

    if not fps or not np.isfinite(fps) or fps <= 0:
        fps = 25.0

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    if width <= 0 or height <= 0:

        cap.release()

        raise ValueError(
            "Dimensões do vídeo inválidas."
        )

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    writer = cv2.VideoWriter(
        output_video,
        fourcc,
        fps,
        (width, height)
    )

    if not writer.isOpened():

        cap.release()

        raise ValueError(
            "Não foi possível criar o vídeo de saída."
        )

    angles_history = {
        "left": [],
        "right": []
    }

    frame_records = []

    frame_number = 0
    detected_frames = 0

    try:

        while True:

            success, frame = cap.read()

            if not success:
                break

            frame_number += 1

            result = model.predict(
                frame,
                verbose=False,
                conf=confidence_threshold
            )[0]

            annotated_frame = result.plot()

            left_angle = None
            right_angle = None

            if (
                result.keypoints is not None
                and len(result.keypoints) > 0
            ):

                detected_frames += 1

                # Seleciona a pessoa com maior confiança
                # média nas articulações detectadas.
                person_scores = []

                for person_idx in range(
                    len(result.keypoints)
                ):

                    person_conf = (
                        result.keypoints.conf[person_idx]
                        .cpu()
                        .numpy()
                    )

                    person_scores.append(
                        float(np.mean(person_conf))
                    )

                best_person = int(
                    np.argmax(person_scores)
                )

                keypoints = (
                    result.keypoints.xy[best_person]
                    .cpu()
                    .numpy()
                )

                confidences = (
                    result.keypoints.conf[best_person]
                    .cpu()
                    .numpy()
                )

                left_angle = get_joint_angle(
                    keypoints,
                    confidences,
                    "left",
                    confidence_threshold
                )

                right_angle = get_joint_angle(
                    keypoints,
                    confidences,
                    "right",
                    confidence_threshold
                )

                if left_angle is not None:

                    angles_history["left"].append({
                        "frame": frame_number,
                        "angle": left_angle
                    })

                if right_angle is not None:

                    angles_history["right"].append({
                        "frame": frame_number,
                        "angle": right_angle
                    })

            valid_angles = [
                value
                for value in [
                    left_angle,
                    right_angle
                ]
                if value is not None
            ]

            mean_angle = (
                float(np.mean(valid_angles))
                if valid_angles
                else None
            )

            frame_records.append({
                "frame": frame_number,
                "left_angle": left_angle,
                "right_angle": right_angle,
                "mean_knee_angle": mean_angle
            })

            cv2.putText(
                annotated_frame,
                f"Frame: {frame_number}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            if mean_angle is not None:

                cv2.putText(
                    annotated_frame,
                    f"Knee angle: {mean_angle:.1f}",
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            writer.write(annotated_frame)

    finally:

        cap.release()
        writer.release()

    # ======================================
    # DETECÇÃO DE REPETIÇÕES
    # ======================================

    repetitions = detect_repetitions(
        frame_records
    )

    repetitions = analyze_consistency(
        repetitions
    )

    # ======================================
    # RESUMO DOS JOELHOS
    # ======================================

    summary = {
        "video": os.path.basename(video_path),
        "total_frames": frame_number,
        "frames_with_person": detected_frames,
        "sides": {},
        "repetitions": repetitions,
        "total_repetitions": len(repetitions),
        "output_video": output_video,
        "output_csv": output_csv,
        "rom_threshold": rom_threshold
    }

    csv_rows = []

    for record in frame_records:

        csv_rows.append({
            "frame": record["frame"],
            "left_angle": (
                round(record["left_angle"], 2)
                if record["left_angle"] is not None
                else None
            ),
            "right_angle": (
                round(record["right_angle"], 2)
                if record["right_angle"] is not None
                else None
            ),
            "mean_knee_angle": (
                round(record["mean_knee_angle"], 2)
                if record["mean_knee_angle"] is not None
                else None
            )
        })

    for side, measurements in angles_history.items():

        if measurements:

            values = [
                item["angle"]
                for item in measurements
            ]

            minimum = float(np.min(values))
            maximum = float(np.max(values))
            rom = maximum - minimum

            status = (
                "AMPLITUDE ABAIXO DO LIMIAR DEMONSTRATIVO"
                if rom < rom_threshold
                else "AMPLITUDE ACIMA DO LIMIAR DEMONSTRATIVO"
            )

            summary["sides"][side] = {
                "measurements": len(values),
                "min_angle": round(minimum, 2),
                "max_angle": round(maximum, 2),
                "range_of_motion": round(rom, 2),
                "status": status
            }

        else:

            summary["sides"][side] = {
                "measurements": 0,
                "status": "DADOS INSUFICIENTES"
            }

    # ======================================
    # RELATÓRIO CSV
    # ======================================

    with open(
        output_csv,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        fieldnames = [
            "frame",
            "left_angle",
            "right_angle",
            "mean_knee_angle"
        ]

        csv_writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        csv_writer.writeheader()
        csv_writer.writerows(csv_rows)

    # ======================================
    # RELATÓRIO DE REPETIÇÕES
    # ======================================

    repetition_csv = os.path.join(
        output_dir,
        "relatorio_repeticoes.csv"
    )

    repetition_fields = [
        "repetition",
        "start_frame",
        "end_frame",
        "baseline_angle",
        "minimum_angle",
        "range_of_motion",
        "variation_percent",
        "status"
    ]

    with open(
        repetition_csv,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        csv_writer = csv.DictWriter(
            file,
            fieldnames=repetition_fields
        )

        csv_writer.writeheader()

        for repetition in repetitions:

            csv_writer.writerow({
                key: repetition.get(key)
                for key in repetition_fields
            })

    summary["repetition_csv"] = repetition_csv

    return summary
