# Relatório de Experimentos e Resultados — MedMonitor AI

**Projeto:** MedMonitor AI  
**Instituição:** FIAP  
**Desafio:** Tech Challenge — Fase 4  
**Área:** Inteligência Artificial aplicada ao monitoramento multimodal

---

## 1. Objetivo dos experimentos

Os experimentos tiveram como objetivo validar o funcionamento dos módulos desenvolvidos no MedMonitor AI, avaliando a capacidade de processamento de diferentes fontes de informação e a identificação de padrões atípicos.

Foram avaliados quatro módulos principais:

1. Análise de vídeo por visão computacional.
2. Análise de áudio e processamento de linguagem natural.
3. Detecção de anomalias em sinais vitais.
4. Comparação de prescrições e registros de administração.

Também foi testada a integração dos resultados por meio da Central de Alertas Multimodais.

## 2. Ambiente experimental

O protótipo foi executado em ambiente local, utilizando Python 3.12 e Streamlit.

As principais tecnologias utilizadas nos experimentos foram:

- YOLOv8 Pose e OpenCV para análise de vídeo.
- Azure Speech Services para transcrição de áudio.
- Azure AI Language para análise textual.
- Scikit-learn e Isolation Forest para detecção de anomalias.
- Pandas e NumPy para manipulação dos dados.
- Streamlit para apresentação dos resultados.

Parte dos dados utilizados foi gerada artificialmente para permitir a validação controlada dos módulos.

## 3. Experimento 1 — Análise de vídeo

### Objetivo

Avaliar a capacidade de identificação de movimentos corporais e comparação da amplitude de movimento entre repetições.

### Metodologia

Foi utilizado o modelo YOLOv8 Pose para estimar pontos-chave corporais em vídeos.

Com base nas posições identificadas, o módulo calcula ângulos articulares, acompanha as variações durante a execução dos movimentos e identifica repetições.

Posteriormente, as amplitudes das repetições são comparadas utilizando critérios experimentais de consistência.

### Resultados observados

| Indicador | Resultado |
|---|---:|
| Repetições identificadas | 5 |
| Repetições com amplitude discrepante | 1 |

O sistema também gerou um vídeo anotado e relatórios CSV com informações dos movimentos identificados.

### Análise

O experimento demonstrou a aplicação de visão computacional para estimativa de poses e análise de movimentos.

A identificação de uma repetição com amplitude discrepante demonstra a possibilidade de utilizar informações extraídas de vídeos para sinalizar variações durante a execução de exercícios.

A análise depende da qualidade do vídeo, visibilidade das articulações e confiabilidade da estimativa de pose.

## 4. Experimento 2 — Análise de áudio

### Objetivo

Validar a transcrição automática de gravações e a identificação de expressões relevantes em relatos de pacientes.

### Metodologia

Foi utilizado o Azure Speech Services para converter gravações em texto, com configuração de idioma português brasileiro (`pt-BR`).

Na sequência, o texto foi processado pelo Azure AI Language para extração de sentimento, frases-chave e entidades.

Um mecanismo complementar de regras foi utilizado para identificar expressões associadas a categorias experimentais de atenção.

### Resultados observados

Em um dos testes, foi utilizada a seguinte fala simulada:

"Boa tarde, médico. Eu tô muito mal. Tô com dor de cabeça, dor de barriga e não enxergo nada."

A transcrição foi realizada corretamente e o processamento textual retornou:

| Indicador | Resultado |
|---|---|
| Sentimento | Mixed |
| Confiança positiva | 31% |
| Confiança neutra | 2% |
| Confiança negativa | 67% |

Foram identificadas expressões relevantes relacionadas a dor e desconforto.

O mecanismo de regras identificou duas ocorrências na demonstração apresentada:

- Visual — "não enxergo nada" — prioridade experimental alta.
- Gastrointestinal — "dor de barriga" — prioridade experimental moderada.

### Análise

O experimento demonstrou a integração entre reconhecimento automático de fala, processamento de linguagem natural e identificação complementar de expressões por regras.

A utilização conjunta dessas técnicas permite transformar gravações em informações estruturadas para posterior consolidação.

Entretanto, a análise textual depende do contexto da fala e pode apresentar limitações na interpretação de negações, ambiguidades e expressões informais.

## 5. Experimento 3 — Detecção de anomalias em sinais vitais

### Objetivo

Avaliar a aplicação do algoritmo Isolation Forest na identificação de medições estatisticamente atípicas em séries temporais de sinais vitais.

### Metodologia

Foi desenvolvido um gerador de dados sintéticos para simular medições de:

- Frequência cardíaca.
- Pressão arterial sistólica.
- Pressão arterial diastólica.
- Saturação de oxigênio.

Foram gerados 120 registros, com alterações artificiais inseridas para permitir a avaliação do algoritmo.

O modelo Isolation Forest foi configurado com contaminação estimada de 7% e 150 estimadores.

### Resultados observados

| Indicador | Resultado |
|---|---:|
| Registros analisados | 120 |
| Anomalias identificadas | 9 |
| Percentual de anomalias | 7,5% |

O dashboard apresentou gráficos temporais para os quatro indicadores e uma tabela contendo os registros identificados como atípicos.

### Análise

O experimento demonstrou a utilização de aprendizado de máquina não supervisionado para identificação de padrões estatisticamente incomuns.

A técnica permite analisar múltiplas variáveis simultaneamente e identificar combinações de valores que diferem do comportamento predominante dos dados.

Como os dados são sintéticos, o resultado demonstra o funcionamento técnico do algoritmo, mas não permite concluir sobre sua eficácia em pacientes reais.

## 6. Experimento 4 — Análise de prescrições

### Objetivo

Validar a comparação automatizada entre medicamentos prescritos e registros de administração.

### Metodologia

Foram criados dados simulados contendo prescrições e registros de administração de medicamentos.

O módulo compara os dados e identifica divergências utilizando regras implementadas em Python.

Foram considerados os seguintes cenários:

- Medicamento administrado conforme registro.
- Administração atrasada.
- Medicamento não administrado.
- Dose divergente.
- Administração sem prescrição correspondente.

### Resultados observados

| Indicador | Resultado |
|---|---:|
| Registros analisados | 6 |
| Situações de atenção | 4 |
| Registros conformes | 2 |

As quatro situações identificadas foram:

| Medicamento | Ocorrência |
|---|---|
| Paracetamol | Conforme registro |
| Dipirona | Atraso de 45 minutos |
| Omeprazol | Não administrado |
| Amoxicilina | Dose divergente |
| Losartana | Conforme registro |
| Ibuprofeno | Sem prescrição |

### Análise

O experimento demonstrou a aplicação de regras automatizadas para comparação entre informações de prescrição e administração.

A abordagem permite identificar inconsistências nos registros simulados e gerar ocorrências para análise posterior.

O protótipo não contempla regras completas de administração hospitalar, alterações autorizadas, cancelamentos ou justificativas clínicas.

## 7. Experimento 5 — Central de Alertas Multimodais

### Objetivo

Validar a consolidação das informações produzidas pelos diferentes módulos em uma interface única.

### Metodologia

Foi desenvolvido um módulo de consolidação responsável por consultar os resultados armazenados na sessão do Streamlit e organizar as ocorrências por origem, categoria, prioridade experimental e descrição.

A central reúne informações de:

- Áudio.
- Vídeo.
- Sinais vitais.
- Prescrições.

Também disponibiliza a exportação dos resultados consolidados em formato CSV.

### Resultado observado

Durante uma execução integrada, o dashboard apresentou:

| Indicador | Resultado |
|---|---:|
| Módulos executados | 4 |
| Ocorrências consolidadas exibidas | 18 |
| Módulos disponíveis | 0 |

O resultado representa uma execução observada da aplicação e não uma métrica de desempenho clínico.

### Análise

A central demonstrou a possibilidade de reunir informações heterogêneas em uma única interface.

A integração permite consultar diferentes tipos de ocorrências sem acessar individualmente cada módulo.

O resultado também demonstra a importância de manter uma estrutura padronizada para os dados produzidos por diferentes componentes.

## 8. Considerações sobre os resultados

Os experimentos demonstraram o funcionamento dos principais componentes técnicos do MedMonitor AI.

Foram exploradas diferentes abordagens:

- Visão computacional para estimativa de poses.
- Reconhecimento automático de fala.
- Processamento de linguagem natural.
- Aprendizado de máquina não supervisionado.
- Comparação automatizada de registros.
- Consolidação de informações multimodais.

Os resultados apresentados são experimentais e estão associados aos dados e cenários utilizados durante os testes.

Não foram realizados estudos clínicos, validação diagnóstica ou avaliação de desempenho com população hospitalar.

## 9. Limitações dos experimentos

As principais limitações identificadas foram:

1. Utilização de dados sintéticos em sinais vitais e prescrições.
2. Dependência da qualidade dos arquivos de áudio e vídeo.
3. Possibilidade de erros na estimativa de poses.
4. Limitações das regras textuais na interpretação de contexto e negações.
5. Ausência de validação clínica dos critérios de prioridade.
6. Ausência de persistência histórica em banco de dados.
7. Necessidade de validação dos resultados por profissionais especializados antes de qualquer aplicação real.

## 10. Conclusão

Os experimentos realizados demonstraram a viabilidade técnica de desenvolver uma aplicação acadêmica que integra diferentes tecnologias de inteligência artificial para análise multimodal.

A arquitetura modular permitiu desenvolver e testar componentes independentes, enquanto a Central de Alertas Multimodais possibilitou consolidar os resultados em uma interface única.

O projeto evidencia possibilidades de aplicação de visão computacional, processamento de linguagem natural e aprendizado de máquina em cenários de monitoramento.

Como evolução, destaca-se a necessidade de aprimorar a integração entre modalidades, utilizar conjuntos de dados representativos e desenvolver mecanismos de validação mais robustos.

**MedMonitor AI — FIAP Tech Challenge Fase 4.**