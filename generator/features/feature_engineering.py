import os
import pandas as pd
import pandera.pandas as pa

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica transformações e cria novas features.
    """
    df_processed = df.copy()
    
    # Exemplo: Criando uma feature de interação se as colunas existirem
    if "feature_1" in df.columns and "feature_2" in df.columns:
        df_processed["feature_1_x_feature_2"] = df_processed["feature_1"] * df_processed["feature_2"]
        
    return df_processed

if __name__ == "__main__":
    # 1. Definir caminhos baseados na estrutura BUILD
    raw_path = "build/data/raw"
    output_dir = "build/data/processed"
    output_path = os.path.join(output_dir, "features_ready.csv")
    
    # 2. Ler e unir os dados (Accepted + Rejected)
    try:
        print("Lendo dados brutos de build/data/raw/...")
        df_acc = pd.read_excel(os.path.join(raw_path, "accepted.xlsx"), nrows=10000)
        df_rej = pd.read_excel(os.path.join(raw_path, "rejected.xlsx"), nrows=10000)
        
        # Unindo os datasets para análise (ajuste a lógica de união conforme seu critério)
        df = pd.concat([df_acc, df_rej], axis=0, ignore_index=True)
        print(f"Datasets carregados. Total de linhas: {len(df)}")
        
    except FileNotFoundError:
        print("Arquivos Excel não encontrados em build/data/raw. Usando dados sintéticos...")
        df = pd.DataFrame({
            "feature_1": [0.1, 0.5, 0.9, 0.3],
            "feature_2": [1.0, 2.0, 3.0, 4.0],
            "target": [0, 1, 1, 0]
        })

    # 3. Processar
    df_processed = compute_features(df)
    
    # 4. Garantir que a pasta build/data/processed existe
    os.makedirs(output_dir, exist_ok=True)
    
    # 5. Salvar
    df_processed.to_csv(output_path, index=False)
    print(f"Sucesso! Features salvas em: {output_path}")