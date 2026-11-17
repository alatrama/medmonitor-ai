
import os
import tempfile

import pandas as pd
import streamlit as st

from modules.video_analysis import process_video
from modules.audio_analysis import transcribe_audio
from modules.text_analysis import analyze_text
from modules.clinical_alerts import detect_clinical_alerts, generate_alert_summary
from modules.vital_signs import analyze_vital_signs
from modules.prescription_analysis import analyze_prescriptions
from modules.multimodal_alerts import build_multimodal_alerts


# ==========================================
# CONFIGURAÇÕES
# ==========================================

st.set_page_config(
    page_title="MedMonitor AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

OUTPUT_DIR = "outputs/processed_videos"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# ESTILO
# ==========================================

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-title {
        font-size: 30px;
        font-weight: 700;
        color: #2563EB;
    }

    .subtitle {
        color: #64748b;
        font-size: 14px;
    }

    div[data-testid="stMetric"] {
        background-color: rgba(128,128,128,0.07);
        padding: 16px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.15);
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# MENU LATERAL
# ==========================================

with st.sidebar:

    st.title("🏥 MedMonitor AI")
    st.caption("Monitoramento inteligente de pacientes")

    st.divider()

    pagina = st.radio(
        "NAVEGAÇÃO",
        [
            "Visão Geral",
            "Análise de Vídeo",
            "Análise de Áudio",
            "Sinais Vitais",
            "Prescrições",
            "Alertas"
        ]
    )

    st.divider()

    st.caption("TECH CHALLENGE — FASE 4")
    st.caption("FIAP | IA para Devs")


# ==========================================
# CABEÇALHO
# ==========================================

st.markdown(
    '<div class="main-title">MedMonitor AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Plataforma de monitoramento multimodal e '
    'detecção inteligente de anomalias clínicas.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# ==========================================
# VISÃO GERAL
# ==========================================

if pagina == "Visão Geral":

    st.subheader("Painel de Monitoramento")

    st.info(
        "Ambiente de demonstração acadêmica. "
        "Os indicadores desta tela são ilustrativos."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Pacientes monitorados", "12")
    col2.metric("Anomalias detectadas", "03")
    col3.metric("Alertas prioritários", "01")
    col4.metric("Módulos ativos", "03/03")

    st.divider()

    st.subheader("Módulos de Inteligência Artificial")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### 🎥 Análise de Vídeo")
        st.write("Detecção de postura e padrões de movimentação.")
        st.caption("YOLOv8 Pose + OpenCV")
        st.success("Implementado")

    with c2:
        st.markdown("### 🎙️ Análise de Áudio")
        st.write("Transcrição e identificação de termos críticos.")
        st.caption("Azure Speech + Azure Language")
        st.success("Implementado — Azure Speech + Language")

    with c3:
        st.markdown("### ❤️ Sinais Vitais")
        st.write("Detecção de anomalias em indicadores clínicos.")
        st.caption("Isolation Forest")
        st.info("Próxima implementação")

    st.divider()

    st.subheader("Fluxo de Processamento")

    st.markdown("""
    1. Recebimento dos dados multimodais.
    2. Processamento individual de cada modalidade.
    3. Identificação de anomalias.
    4. Consolidação das evidências.
    5. Geração de alertas para avaliação humana.
    """)


# ==========================================
# ANÁLISE DE VÍDEO
# ==========================================

elif pagina == "Análise de Vídeo":

    st.subheader("🎥 Análise de Movimentação Corporal")

    st.write(
        "Envie um vídeo de fisioterapia para identificar "
        "articulações, analisar movimentos e detectar "
        "repetições de exercícios."
    )

    st.info(
        "Utilizamos YOLOv8 Pose para identificar pontos "
        "corporais e estimar ângulos articulares em 2D. "
        "Os resultados são experimentais e não representam "
        "uma avaliação clínica."
    )

    uploaded_video = st.file_uploader(
        "Selecione um vídeo",
        type=["mp4", "avi", "mov"],
        help="Prefira vídeos curtos, com uma pessoa visível e corpo inteiro."
    )

    rom_threshold = st.slider(
        "Limiar experimental de amplitude (graus)",
        min_value=10,
        max_value=90,
        value=30
    )

    if uploaded_video is not None:

        st.video(uploaded_video)

        st.caption(
            f"Arquivo selecionado: {uploaded_video.name}"
        )

        if st.button(
            "▶ Analisar vídeo",
            type="primary",
            use_container_width=True
        ):

            temp_path = None

            try:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=os.path.splitext(
                        uploaded_video.name
                    )[1]
                ) as temp_file:

                    temp_file.write(
                        uploaded_video.getvalue()
                    )

                    temp_path = temp_file.name

                with st.spinner(
                    "Processando vídeo com YOLOv8 Pose..."
                ):

                    result = process_video(
                        video_path=temp_path,
                        output_dir=OUTPUT_DIR,
                        confidence_threshold=0.4,
                        rom_threshold=float(rom_threshold)
                    )

                st.session_state["video_result"] = result
                st.session_state["video_filename"] = uploaded_video.name

                st.success(
                    "Análise de vídeo concluída!"
                )

            except Exception as error:

                st.error(
                    f"Erro durante o processamento: {error}"
                )

            finally:

                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

    # ======================================
    # EXIBIÇÃO DOS RESULTADOS
    # ======================================

    if "video_result" in st.session_state:

        result = st.session_state["video_result"]

        st.divider()

        st.subheader("📊 Resultado geral da análise")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Frames analisados",
            result["total_frames"]
        )

        col2.metric(
            "Frames com pessoa detectada",
            result["frames_with_person"]
        )

        col3.metric(
            "Limiar experimental",
            f'{result["rom_threshold"]:.0f}°'
        )

        # ==================================
        # IDENTIFICAÇÃO DE REPETIÇÕES
        # ==================================

        st.divider()

        st.subheader("🔄 Identificação de repetições")

        st.metric(
            "Repetições completas identificadas",
            result["total_repetitions"]
        )

        repetitions = result["repetitions"]

        if repetitions:

            repetition_df = pd.DataFrame(repetitions)

            display_df = repetition_df[
                [
                    "repetition",
                    "start_frame",
                    "end_frame",
                    "minimum_angle",
                    "range_of_motion",
                    "variation_percent",
                    "status"
                ]
            ].copy()

            display_df.columns = [
                "Repetição",
                "Frame inicial",
                "Frame final",
                "Ângulo mínimo",
                "Amplitude (°)",
                "Variação (%)",
                "Classificação"
            ]

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            st.markdown(
                "#### Comparação entre repetições"
            )

            chart_df = pd.DataFrame({
                "Repetição": [
                    f"Rep. {item['repetition']}"
                    for item in repetitions
                ],
                "Amplitude": [
                    item["range_of_motion"]
                    for item in repetitions
                ]
            })

            st.bar_chart(
                chart_df.set_index("Repetição")
            )

            discrepant = [
                item for item in repetitions
                if item["status"] == "AMPLITUDE DISCREPANTE"
            ]

            if discrepant:

                st.warning(
                    f"Foram identificadas {len(discrepant)} "
                    "repetições com amplitude discrepante "
                    "em relação à mediana."
                )

            else:

                st.success(
                    "Nenhuma discrepância de amplitude foi "
                    "identificada pelo critério experimental."
                )

            repetition_csv = result["repetition_csv"]

            if os.path.exists(repetition_csv):

                with open(repetition_csv, "rb") as file:

                    st.download_button(
                        "⬇ Baixar relatório de repetições",
                        data=file.read(),
                        file_name="relatorio_repeticoes.csv",
                        mime="text/csv"
                    )

        else:

            st.warning(
                "Nenhuma repetição completa foi identificada. "
                "Verifique o enquadramento e a visibilidade "
                "das articulações no vídeo."
            )

        # ==================================
        # ANÁLISE DOS JOELHOS
        # ==================================

        st.divider()

        st.subheader("🦵 Análise dos joelhos")

        left, right = st.columns(2)

        for side, column in [
            ("left", left),
            ("right", right)
        ]:

            data = result["sides"][side]

            with column:

                nome = (
                    "esquerdo"
                    if side == "left"
                    else "direito"
                )

                st.markdown(
                    f"#### Joelho {nome}"
                )

                if data["measurements"] > 0:

                    st.metric(
                        "Amplitude de movimento",
                        f'{data["range_of_motion"]:.1f}°'
                    )

                    st.write(
                        f'Ângulo mínimo: {data["min_angle"]:.1f}°'
                    )

                    st.write(
                        f'Ângulo máximo: {data["max_angle"]:.1f}°'
                    )

                    st.caption(
                        f'Medições válidas: {data["measurements"]}'
                    )

                    if "ABAIXO" in data["status"]:

                        st.warning(data["status"])

                    else:

                        st.success(data["status"])

                else:

                    st.warning(
                        "Dados insuficientes para avaliar esta articulação."
                    )

        # ==================================
        # VÍDEO PROCESSADO
        # ==================================

        st.divider()

        st.subheader(
            "🎬 Vídeo com detecção de articulações"
        )

        video_path = result["output_video"]

        if os.path.exists(video_path):

            with open(video_path, "rb") as video_file:

                video_bytes = video_file.read()

            st.video(video_bytes)

            st.download_button(
                "⬇ Baixar vídeo processado",
                data=video_bytes,
                file_name="video_analisado.mp4",
                mime="video/mp4"
            )

        # ==================================
        # GRÁFICO DOS ÂNGULOS
        # ==================================

        csv_path = result["output_csv"]

        if os.path.exists(csv_path):

            df = pd.read_csv(csv_path)

            if not df.empty:

                st.divider()

                st.subheader(
                    "📈 Evolução dos ângulos articulares"
                )

                chart_data = df.set_index("frame")[
                    [
                        "left_angle",
                        "right_angle"
                    ]
                ]

                chart_data.columns = [
                    "Joelho esquerdo",
                    "Joelho direito"
                ]

                st.line_chart(chart_data)

                st.subheader(
                    "Dados das medições"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

                st.download_button(
                    "⬇ Baixar relatório de movimentos",
                    data=df.to_csv(
                        index=False,
                        sep=";",
                        encoding="utf-8-sig"
                    ),
                    file_name="relatorio_movimentos.csv",
                    mime="text/csv"
                )

        st.caption(
            "A amplitude global corresponde à diferença entre "
            "o maior e o menor ângulo detectado. A amplitude "
            "por repetição é estimada a partir da posição elevada "
            "e do menor ângulo observado durante a descida. "
            "Os critérios são experimentais, não clínicos."
        )


# ==========================================
# ANÁLISE DE ÁUDIO
# ==========================================

elif pagina == "Análise de Áudio":

    st.subheader("🎙️ Análise de Áudio")
    st.write(
        "Envie uma gravação curta para transcrever a fala, analisar o texto "
        "com Azure AI Language e identificar expressões de atenção."
    )
    st.info(
        "Utilize áudio WAV PCM, preferencialmente mono, 16 kHz. "
        "Esta é uma demonstração acadêmica: não realiza diagnóstico e "
        "não substitui avaliação profissional. Evite dados pessoais identificáveis."
    )

    uploaded_audio = st.file_uploader(
        "Selecione uma gravação de áudio",
        type=["wav"],
        help="Recomendado: WAV PCM, mono, 16 kHz, com fala clara e curta."
    )

    if uploaded_audio is not None:
        st.audio(uploaded_audio, format="audio/wav")
        st.caption(f"Arquivo selecionado: {uploaded_audio.name}")

        if st.button("▶ Transcrever e analisar áudio", type="primary", use_container_width=True):
            temp_audio_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    temp_file.write(uploaded_audio.getvalue())
                    temp_audio_path = temp_file.name

                with st.spinner("Transcrevendo áudio com Azure Speech..."):
                    transcription_result = transcribe_audio(temp_audio_path)

                if not transcription_result.get("success"):
                    st.error(transcription_result.get("message", "Não foi possível transcrever o áudio."))
                else:
                    transcription = transcription_result.get("transcription", "").strip()
                    if not transcription:
                        st.warning("O Azure não retornou texto para este áudio.")
                    else:
                        with st.spinner("Analisando texto com Azure AI Language..."):
                            language_result = analyze_text(transcription)

                        clinical_alerts = detect_clinical_alerts(transcription)
                        alert_summary = generate_alert_summary(clinical_alerts)
                        st.session_state["audio_result"] = {
                            "filename": uploaded_audio.name,
                            "transcription": transcription,
                            "language": language_result,
                            "alert_summary": alert_summary
                        }
                        st.success("Transcrição e análise concluídas!")
            except Exception as error:
                st.error(f"Erro durante a análise do áudio: {error}")
            finally:
                if temp_audio_path and os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)

    if "audio_result" in st.session_state:
        audio_result = st.session_state["audio_result"]
        language_result = audio_result["language"]
        alert_summary = audio_result["alert_summary"]

        st.divider()
        st.subheader("📝 Transcrição")
        st.write(audio_result["transcription"])

        st.divider()
        st.subheader("🧠 Análise do Azure AI Language")
        sentiment = language_result.get("sentiment", "Não identificado")
        confidence = language_result.get("confidence", {})
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sentimento", str(sentiment).capitalize())
        col2.metric("Confiança positiva", f'{confidence.get("positive", 0):.0%}')
        col3.metric("Confiança neutra", f'{confidence.get("neutral", 0):.0%}')
        col4.metric("Confiança negativa", f'{confidence.get("negative", 0):.0%}')

        st.markdown("#### Frases-chave")
        key_phrases = language_result.get("key_phrases", [])
        if key_phrases:
            st.write(" · ".join(key_phrases))
        else:
            st.caption("Nenhuma frase-chave retornada.")

        st.markdown("#### Entidades identificadas")
        entities = language_result.get("entities", [])
        if entities:
            st.dataframe(pd.DataFrame(entities), use_container_width=True, hide_index=True)
        else:
            st.caption("Nenhuma entidade identificada.")

        st.divider()
        st.subheader("🚨 Regras experimentais de atenção")
        st.metric("Expressões identificadas", alert_summary.get("total", 0))
        if alert_summary.get("alerts"):
            for alert in alert_summary["alerts"]:
                message = (
                    f'**{alert["category"]} — {alert["term"]}**: '
                    f'{alert["message"]}. Prioridade experimental {alert["severity"].lower()}.'
                )
                if alert["severity"] == "Alta":
                    st.error(message)
                else:
                    st.warning(message)
        else:
            st.success("Nenhuma expressão prevista nas regras foi identificada.")

        st.caption(
            "As prioridades são definidas por regras demonstrativas. O sistema "
            "não interpreta negações, contexto clínico ou gravidade e não deve "
            "ser utilizado para decisões assistenciais."
        )


# ==========================================
# SINAIS VITAIS
# ==========================================
elif pagina == "Sinais Vitais":
    st.title("Monitoramento de Sinais Vitais")
    st.caption(
        "Análise experimental de séries temporais com "
        "detecção de anomalias usando Isolation Forest."
    )

    if st.button("Gerar e analisar sinais vitais", type="primary"):
        with st.spinner("Analisando sinais vitais..."):
            st.session_state["vital_result"] = analyze_vital_signs()

    if "vital_result" in st.session_state:
        result = st.session_state["vital_result"]
        df = result["data"]

        col1, col2, col3 = st.columns(3)

        col1.metric("Registros analisados", result["total_records"])
        col2.metric("Anomalias detectadas", result["total_anomalies"])
        col3.metric(
            "Percentual de anomalias",
            f"{result['anomaly_percentage']}%"
        )

        st.subheader("Evolução dos sinais vitais")

        metrics = {
            "fc": "Frequência cardíaca (bpm)",
            "pas": "Pressão sistólica (mmHg)",
            "pad": "Pressão diastólica (mmHg)",
            "spo2": "Saturação de oxigênio (%)"
        }

        for column, label in metrics.items():
            st.markdown(f"**{label}**")

            chart_data = df.set_index("timestamp")[[column]]
            st.line_chart(chart_data)

        st.subheader("Registros identificados como anomalia")

        anomalies = df[df["is_anomaly"]]

        if not anomalies.empty:
            st.warning(
                f"Foram identificados {len(anomalies)} registros "
                "atípicos pelo algoritmo."
            )

            st.dataframe(
                anomalies[
                    ["timestamp", "fc", "pas", "pad", "spo2", "status"]
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("Nenhuma anomalia foi identificada.")

        st.download_button(
            "Baixar relatório CSV",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="relatorio_sinais_vitais.csv",
            mime="text/csv"
        )

        st.info(
            "As anomalias representam padrões estatisticamente atípicos "
            "nos dados simulados. Não constituem diagnóstico ou "
            "classificação clínica."
        )
    else:
        st.info("Clique em 'Gerar e analisar sinais vitais' para iniciar.")

# ==========================================
# PRESCRIÇÕES
# ==========================================

elif pagina == "Prescrições":
    st.title("Análise de Prescrições")
    st.caption(
        "Comparação experimental entre medicamentos prescritos "
        "e registros de administração."
    )

    if st.button("Analisar prescrições", type="primary"):
        with st.spinner("Comparando prescrições e administrações..."):
            st.session_state["prescription_result"] = analyze_prescriptions()

    if "prescription_result" in st.session_state:
        result = st.session_state["prescription_result"]
        df = result["data"]

        col1, col2, col3 = st.columns(3)

        col1.metric("Registros analisados", result["total"])
        col2.metric("Situações de atenção", result["alerts"])
        col3.metric(
            "Registros conformes",
            int((df["status"] == "Conforme registro").sum())
        )

        st.subheader("Resultado da comparação")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Resumo das ocorrências")

        attention = df[df["status"] != "Conforme registro"]

        if not attention.empty:
            for _, item in attention.iterrows():
                st.warning(
                    f"**{item['medication']} — {item['status']}**\n\n"
                    f"{item['details']}"
                )
        else:
            st.success("Nenhuma divergência identificada.")

        st.download_button(
            "Baixar relatório de prescrições",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="relatorio_prescricoes.csv",
            mime="text/csv"
        )

        st.info(
            "Dados simulados. As divergências identificadas são "
            "sinalizações experimentais e precisam de validação humana."
        )

    else:
        st.info("Clique em 'Analisar prescrições' para iniciar.")

# ==========================================
# CENTRAL DE ALERTAS
# ==========================================

elif pagina == "Alertas":
    st.title("Central de Alertas Multimodais")
    st.caption(
        "Consolidação dos resultados de áudio, vídeo, "
        "sinais vitais e prescrições."
    )

    result = build_multimodal_alerts(
        audio_result=st.session_state.get("audio_result"),
        video_result=st.session_state.get("video_result"),
        vital_result=st.session_state.get("vital_result"),
        prescription_result=st.session_state.get("prescription_result")
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Módulos executados", result["total_modules"])
    col2.metric("Ocorrências identificadas", result["total_alerts"])
    col3.metric(
        "Módulos disponíveis",
        4 - result["total_modules"]
    )

    st.subheader("Status dos módulos")

    module_names = [
        "Áudio",
        "Vídeo",
        "Sinais vitais",
        "Prescrições"
    ]

    for name in module_names:
        if name in result["modules_analyzed"]:
            st.success(f"{name}: análise executada nesta sessão")
        else:
            st.info(f"{name}: aguardando análise")

    st.divider()
    st.subheader("Ocorrências consolidadas")

    if not result["alerts"].empty:
        st.dataframe(
            result["alerts"],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Baixar relatório consolidado",
            data=result["alerts"].to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name="relatorio_multimodal.csv",
            mime="text/csv"
        )
    else:
        st.info(
            "Nenhuma ocorrência foi consolidada. "
            "Execute os módulos para gerar resultados."
        )

    st.warning(
        "Os resultados são experimentais, baseados em dados "
        "simulados ou regras automatizadas. Não representam "
        "diagnóstico médico nem substituem avaliação profissional."
    )


    st.write("Consolidação dos resultados gerados pelos módulos nesta sessão.")

    audio_result = st.session_state.get("audio_result")
    video_result = st.session_state.get("video_result")

    if audio_result:
        summary = audio_result.get("alert_summary", {})
        st.markdown("### 🎙️ Alertas originados da análise de áudio")
        st.caption(f'Arquivo: {audio_result.get("filename", "áudio")}')
        st.write(f'Situação: **{summary.get("status", "Sem classificação")}**')
        for alert in summary.get("alerts", []):
            message = (
                f'{alert["category"]} — {alert["term"]} '
                f'(prioridade experimental: {alert["severity"]})'
            )
            if alert["severity"] == "Alta":
                st.error(message)
            else:
                st.warning(message)
    else:
        st.info("Ainda não há resultados de áudio nesta sessão.")

    if video_result:
        st.markdown("### 🎥 Indicadores originados da análise de vídeo")
        st.metric("Repetições identificadas", video_result.get("total_repetitions", 0))
        discrepant = [
            item for item in video_result.get("repetitions", [])
            if item.get("status") == "AMPLITUDE DISCREPANTE"
        ]
        if discrepant:
            st.warning(
                f"{len(discrepant)} repetição(ões) com amplitude discrepante "
                "segundo o critério experimental."
            )
        else:
            st.success("Nenhuma discrepância foi sinalizada pelo critério experimental.")
    else:
        st.info("Ainda não há resultados de vídeo nesta sessão.")

    st.caption(
        "Central demonstrativa. Alertas e indicadores não são diagnósticos "
        "nem recomendações clínicas."
    )


# ==========================================
# RODAPÉ
# ==========================================

st.divider()

st.caption(
    "MedMonitor AI | FIAP - Tech Challenge Fase 4 | "
    "Protótipo acadêmico"
)
