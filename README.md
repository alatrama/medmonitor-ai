# MedMonitor AI

### Plataforma de monitoramento multimodal e detecção inteligente de anomalias clínicas

Projeto desenvolvido para o **FIAP Tech Challenge – Fase 4**, com o objetivo de demonstrar a aplicação de inteligência artificial no monitoramento de pacientes por meio da análise integrada de áudio, vídeo, sinais vitais e prescrições.

---

## 1. Sobre o projeto

O MedMonitor AI é um protótipo acadêmico de monitoramento multimodal que utiliza diferentes técnicas de inteligência artificial e processamento de dados para identificar padrões atípicos e possíveis situações que merecem atenção durante o acompanhamento de pacientes.

A solução integra quatro fontes de informação:

- **Vídeo:** análise de movimentos corporais utilizando visão computacional.
- **Áudio:** transcrição de gravações e identificação de expressões relevantes.
- **Sinais vitais:** identificação de padrões estatisticamente atípicos em séries temporais.
- **Prescrições:** comparação entre medicamentos prescritos e registros de administração.

Os resultados são consolidados em uma Central de Alertas Multimodais, permitindo visualizar ocorrências provenientes das diferentes análises em uma única interface.

## 2. Objetivos

- Demonstrar o uso de inteligência artificial no monitoramento multimodal.
- Identificar movimentos e variações de amplitude em vídeos.
- Transcrever gravações utilizando serviços de inteligência artificial em nuvem.
- Identificar termos e expressões relevantes em transcrições.
- Detectar anomalias em séries temporais de sinais vitais.
- Identificar divergências entre prescrições e administrações.
- Consolidar os resultados em uma interface interativa.

## 3. Arquitetura da solução

O sistema foi desenvolvido em Python, utilizando Streamlit como camada de apresentação e módulos independentes para processamento das diferentes fontes de dados.

### Fluxo de processamento

1. Entrada de dados por upload de arquivos ou geração de dados simulados.
2. Processamento individual por cada módulo.
3. Extração de informações e identificação de padrões atípicos.
4. Geração de ocorrências e alertas experimentais.
5. Consolidação dos resultados na Central de Alertas Multimodais.
6. Disponibilização de relatórios para consulta e exportação.

### Módulos implementados

**Análise de vídeo**

Utiliza YOLOv8 Pose e OpenCV para identificar pessoas, estimar posições corporais e analisar ângulos articulares durante movimentos.

O protótipo calcula a amplitude de movimento das repetições e identifica possíveis discrepâncias entre elas.

**Análise de áudio**

Utiliza Azure Speech Services para transcrever gravações em português brasileiro.

O texto transcrito é processado pelo Azure AI Language para análise de sentimento, extração de frases-chave e identificação de entidades.

Um mecanismo complementar de regras identifica expressões associadas a possíveis situações de atenção.

**Monitoramento de sinais vitais**

Utiliza Scikit-learn e o algoritmo Isolation Forest para identificar medições estatisticamente atípicas.

São considerados os seguintes indicadores:

- Frequência cardíaca (FC).
- Pressão arterial sistólica (PAS).
- Pressão arterial diastólica (PAD).
- Saturação de oxigênio (SpO₂).

**Análise de prescrições**

Compara prescrições simuladas com registros de administração de medicamentos.

Identifica situações como:

- Medicamento não administrado.
- Dose divergente.
- Administração atrasada.
- Administração sem prescrição correspondente.

**Central de Alertas Multimodais**

Consolida as ocorrências produzidas pelos módulos de áudio, vídeo, sinais vitais e prescrições.

Apresenta a origem, categoria, prioridade experimental e descrição das ocorrências, permitindo também exportar os resultados em CSV.

## 4. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Streamlit | Interface web |
| YOLOv8 Pose | Detecção e estimativa de poses |
| OpenCV | Processamento de vídeo |
| Azure Speech Services | Transcrição de áudio |
| Azure AI Language | Análise de texto |
| Scikit-learn | Detecção de anomalias |
| Isolation Forest | Identificação de padrões atípicos |
| Pandas | Manipulação de dados |
| NumPy | Operações numéricas |
| Matplotlib | Visualização de dados |

## 5. Estrutura do projeto

```text
medmonitor-ai/
│
├── app.py
├── requirements.txt
├── requirements-lock.txt
├── .gitignore
├── README.md
├── yolov8n-pose.pt
│
├── modules/
│   ├── __init__.py
│   ├── video_analysis.py
│   ├── audio_analysis.py
│   ├── text_analysis.py
│   ├── clinical_alerts.py
│   ├── vital_signs.py
│   ├── prescription_analysis.py
│   └── multimodal_alerts.py
│
└── docs/
    ├── resultados_experimentais.md
    │
    └── evidencias/
        ├── 02-video.png
        ├── 03-audio.png
        ├── 04-texto.png
        ├── 05-sinais-vitais.png
        ├── 06-prescricoes.png
        └── 07-central-alertas.png
```

## 6. Documentação e evidências

A pasta `docs/` reúne os materiais complementares do projeto, permitindo consultar os resultados dos testes e visualizar as funcionalidades implementadas.

### Resultados experimentais

O arquivo [resultados_experimentais.md](docs/resultados_experimentais.md) apresenta os testes realizados, os resultados observados e as métricas obtidas durante a execução dos módulos.

Entre os pontos documentados estão:

- Resultados da análise de vídeo e identificação de movimentos.
- Testes de transcrição e análise de áudio.
- Detecção de anomalias em sinais vitais.
- Comparação entre prescrições e administrações.
- Consolidação das ocorrências na Central de Alertas Multimodais.

### Evidências da aplicação

A pasta [docs/evidencias](docs/evidencias/) contém capturas de tela da aplicação em funcionamento, demonstrando as principais funcionalidades desenvolvidas.

| Evidência | Funcionalidade |
|---|---|
| 02-video.png | Análise de vídeo, repetições e amplitude de movimento |
| 03-audio.png | Transcrição realizada pelo Azure Speech |
| 04-texto.png | Análise de sentimento, frases-chave e alertas |
| 05-sinais-vitais.png | Gráficos e anomalias identificadas pelo Isolation Forest |
| 06-prescricoes.png | Comparação entre medicamentos prescritos e administrados |
| 07-central-alertas.png | Consolidação multimodal dos resultados |

## 7. Configuração do ambiente

### Pré-requisitos

- Python 3.12.
- Visual Studio Code ou outro editor Python.
- Conta e recursos configurados no Microsoft Azure.
- Conexão com a internet para utilização dos serviços Azure e download de dependências.

### Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
cd medmonitor-ai
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente no Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### Configuração do Azure

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
AZURE_SPEECH_KEY=sua_chave_speech
AZURE_SPEECH_REGION=brazilsouth
AZURE_SPEECH_ENDPOINT=https://brazilsouth.api.cognitive.microsoft.com/

AZURE_LANGUAGE_KEY=sua_chave_language
AZURE_LANGUAGE_ENDPOINT=seu_endpoint_language
```

Substitua os valores pelas credenciais dos recursos Azure criados para o projeto.

**Importante:** nunca publique o arquivo `.env` ou suas chaves no GitHub. As credenciais devem permanecer apenas no ambiente local.

### Execução

Inicie a aplicação:

```bash
streamlit run app.py
```

A interface estará disponível localmente em:

```text
http://localhost:8501
```

## 8. Resultados experimentais

O protótipo permite executar análises independentes e consolidar os resultados em uma única interface.

Entre os cenários demonstrados estão:

- Identificação de repetições e discrepâncias de amplitude em vídeos.
- Transcrição de gravações em português brasileiro.
- Identificação de expressões relevantes em relatos de pacientes.
- Detecção de anomalias em séries temporais de sinais vitais.
- Identificação de divergências em registros de administração de medicamentos.
- Consolidação de ocorrências em relatórios multimodais.

Os testes e resultados observados estão detalhados no arquivo [Resultados Experimentais](docs/resultados_experimentais.md).

Os dados utilizados nas demonstrações incluem cenários sintéticos e gravações de teste. Os resultados dependem dos arquivos e parâmetros utilizados em cada execução.

## 9. Limitações e considerações

O MedMonitor AI é um protótipo acadêmico desenvolvido para demonstrar conceitos de inteligência artificial e processamento multimodal.

As ocorrências identificadas não representam diagnósticos médicos, prognósticos ou recomendações de tratamento.

As classificações de prioridade são experimentais e baseadas em regras definidas para a demonstração.

O algoritmo Isolation Forest identifica padrões estatisticamente atípicos, mas não determina isoladamente a gravidade clínica de uma alteração.

A análise de movimentos utiliza estimativas de pose e critérios experimentais de amplitude, não substituindo avaliações profissionais.

A análise de prescrições utiliza dados simulados e não contempla todas as regras e exceções de um ambiente hospitalar real.

O protótipo não realiza integração com sistemas hospitalares nem envia notificações automáticas para equipes médicas.

Qualquer utilização em ambiente clínico exigiria validação especializada, avaliação de segurança, privacidade, desempenho e conformidade regulatória.

## 10. Trabalhos futuros

- Aprimorar a fusão de informações entre os diferentes módulos.
- Implementar histórico persistente de pacientes e ocorrências.
- Desenvolver mecanismos de reconhecimento de contexto e negações em transcrições.
- Aprimorar a classificação e contextualização dos alertas.
- Implementar integração com sistemas hospitalares.
- Avaliar os modelos com conjuntos de dados reais e devidamente autorizados.
- Desenvolver mecanismos de auditoria e rastreabilidade.

## 11. Contexto acadêmico

Projeto desenvolvido como parte do **Tech Challenge – Fase 4**, da pós-graduação em Inteligência Artificial para Desenvolvedores da FIAP.

**Projeto:** MedMonitor AI  
**Área:** Inteligência Artificial e Saúde  
**Abordagem:** Monitoramento multimodal e detecção de anomalias  
**Instituição:** FIAP

---

*MedMonitor AI — Inteligência artificial aplicada ao monitoramento multimodal de pacientes.*
