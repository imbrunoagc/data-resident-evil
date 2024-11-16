import pandas as pd

def explode_dataframe(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return df.explode(col, ignore_index=True)

def top_10_most_popular_characters(df_exploded: pd.DataFrame) -> pd.DataFrame:
    """
    Ordenar por número de aparições e selecionar os top 10
    """
    top_popular = df_exploded.sort_values(by="aparicoes", ascending=False).head(10)
    print("Top 3 Personagens Mais Populares:")
    print(top_popular[["name", "aparicoes"]])
    return top_popular

def blood_type_distribution(data: pd.DataFrame) -> pd.DataFrame: 
    """
    Contagem de personagens por tipo sanguíneo
    """
    blood_type_count = data["tipo_sanguineo"].value_counts().reset_index()
    print("Distribuição por Tipo Sanguíneo:")
    print(blood_type_count)
    return blood_type_count

def average_height_and_weight_by_blood_type(df: pd.DataFrame) -> pd.DataFrame:
    """
        Obter Média de Altura por Tipo Sanguíneo
    """
    mean_physics = df.groupby("tipo_sanguineo")[["altura", "peso"]].mean().reset_index()
    print("Média de Altura e Peso por Tipo Sanguíneo:")
    print(mean_physics)
    return mean_physics