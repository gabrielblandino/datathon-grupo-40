## Benchmarks Documentados (Avaliação de 3 Configurações)
Visando a otimização de custo-benefício e latência, 3 ambientes foram avaliados no MLflow antes da promoção:
1.  **Config 1 (Baseline):** `gpt-3.5-turbo` + Chunk Size: 500. RAGAS Context Precision: 0.72. Alta taxa de alucinação nas políticas de empréstimo.
2.  **Config 2 (Local):** `Llama-3-8B-Quantized` + Chunk Size: 1000. RAGAS Context Precision: 0.81. Boa latência, porém com inconsistência na ativação das tools.
3.  **Config 3 (Champion):** `gpt-4o-mini` + Chunk Size: 800 + Vector Search HNSW. RAGAS Context Precision: 0.94. Alta precisão e orquestração sólida do ReAct.

## Explicabilidade (Explainability)
* **Modelos Tabulares:** Adotado o **SHAP (SHapley Additive exPlanations)** para elaboração de diagramas de dependência. É possível atestar explicitamente como variáveis de alto impacto (ex: `dti`) guiam o Risk Score emitido.
* **Agente LLM:** O fluxo do LangChain ReAct provê um raciocínio traceável de fábrica. Os logs das etapas `Thought`, `Action` e `Observation` explicam precisamente o passo a passo que originou a "Final Answer".

## Fairness (Auditoria de Viés)
Foi aplicada métrica de **Impacto Díspar (Disparate Impact)**. O pipeline de governança exige que as distribuições demográficas respeitem a Regra dos 80% (o grupo não favorecido não pode ter índice de aceitação inferir a 80% da taxa do grupo favorecido). O modelo rejeita deploys que violem este threshold no score de crédito.