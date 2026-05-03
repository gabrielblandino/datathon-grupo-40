# Model Card - Classificador de Risco de Crédito (Datathon Fase 05)
- **Model Name:** `credit_risk_classifier_v1`
- **Version:** 1.0.0
- **Model Type:** Random Forest Classifier / Scikit-Learn
- **Training Data:** `data/processed/accepted_clean.csv` (Versão do DVC tracking).
- **Intended Use:** Aprovação automatizada e análise de risco para submissões de crédito em plataformas financeiras.
- **Metrics:** F1-Score e AUC ROC avaliadas rigorosamente com holdout set.
- **Fairness & Bias:** O modelo foi validado via feature importance para garantir que `zip_code` (CEP) ou inferências discriminatórias não possuam peso primário sobre o score de aceitação de crédito, assegurando justiça social na avaliação algorítmica.