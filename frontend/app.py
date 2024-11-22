import os
import streamlit as st
import pandas as pd
from configs.settings_page import setup_page
from components.footer import footer
from components.input_css import styling

dir_current = os.path.abspath(os.path.dirname(__file__))
path_raiz = os.path.join(dir_current, "..")
path_data = os.path.join(path_raiz, "data")

setup_page() # Page configuration

st.markdown(styling, unsafe_allow_html=True) # CSS styling in metrics

LOCAL = True

if LOCAL: # Local
    df = pd.read_parquet(
        f'{path_data}/characters_exploded.parquet',
        engine='pyarrow'
        )
    
    df_top_10_characters_with_most_appearances = pd.read_parquet(
        f'{path_data}/top_10_characters_with_most_appearances.parquet',
        engine='pyarrow'
        )
    
    df_top_10_appearances = pd.read_parquet(
        f'{path_data}/top_10_appearances.parquet',
        engine='pyarrow'
    )
    
    df_average_by_blood_type = pd.read_parquet(
        f'{path_data}/average_by_blood_type.parquet',
        engine='pyarrow'
    )
    
    df_blood_type_distribution = pd.read_parquet(
        f'{path_data}/blood_type_distribution.parquet',
        engine='pyarrow'
    )   

col1, col2, col3 = st.columns([1, 3, 1]) # Set 3 columns

# Sidebar
with st.sidebar:
    st.title(':skull: Character Profiles')
    name_characters_list = df['name'].unique()
    character_picked = st.selectbox("Escolha o personagem: ", name_characters_list)
    
    # Preview Image
    imagem_url = df.loc[df['name'] == character_picked, 'pathimage'].values[0]
    st.image(imagem_url)
    
    ano_nasc = df.loc[df['name'] == character_picked, 'ano_de_nascimento'].values[0]
    tipo_sague = df.loc[df['name'] == character_picked, 'tipo_sanguineo'].values[0]
    peso = df.loc[df['name'] == character_picked, 'peso'].values[0]
    altura = df.loc[df['name'] == character_picked, 'altura'].values[0]
    aparicoes = df.loc[df['name'] == character_picked, 'aparicoes'].values
    
    abt_1, abt_2 = st.columns(2)
    abt_1.write(f'**Ano de Nacimento**: {ano_nasc}')
    abt_1.write(f'**Tipo sanguíneo**: {tipo_sague}')
    abt_2.write(f'**Peso**: {peso}')
    abt_2.write(f'**Altura**: {altura}')
    abt_1.write(f'**Aparicoes**: {len(aparicoes)}')

# Metrics
with col1:
    st.markdown("### Métricas")
    number_characters_unique = df['name'].nunique()
    st.metric("Numero de personagens", number_characters_unique)
    
    number_appearances = df['aparicoes'].nunique()
    st.metric("Numero de aparicoes", number_appearances)


# Graphics
with col2:
    st.markdown("### Informações")
    st.table(df_top_10_appearances.rename(columns={'count': 'qtd_aparicoes'}))
    
    col2_1, col2_2 = st.columns(2)
    
    col2_1.table(df_average_by_blood_type.rename(columns={'altura':'avg_altura', 'peso':'avg_peso'}))
    col2_2.table(df_blood_type_distribution)

# Top Ranking
with col3:
    st.markdown("### Top Ranking")
    st.dataframe(df_top_10_characters_with_most_appearances\
        .rename(columns={'count': 'qtd_aparicoes'}), hide_index=True) # Top Ranking

footer()