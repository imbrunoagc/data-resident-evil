import streamlit as st

from frontend.configs.settings_page import setup_page
from frontend.components.footer import footer
from frontend.components.input_css import styling
from frontend.resources.readFile import readFile


setup_page() # Page configuration

st.markdown(styling, unsafe_allow_html=True) # CSS styling

df = readFile('characters_exploded') # Readed data

col1, col2 = st.columns([0.5, 3]) # Set 2 columns

# Defined divider for column
col1.header('Metricas', divider="gray")
col2.header('Gráficos', divider=True)

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
    
    abt_1, abt_2 = st.columns(2)
    abt_1.write(f'**Ano de Nacimento**: {ano_nasc}')
    abt_1.write(f'**Tipo sanguíneo**: {tipo_sague}')
    abt_2.write(f'**Peso**: {peso}')
    abt_2.write(f'**Altura**: {altura}')


with col1:
    
    number_characters_unique = df['name'].nunique()
    st.metric("Numero de personagens", number_characters_unique)
    
    number_appearances = df['aparicoes'].nunique()
    st.metric("Numero de aparicoes", number_appearances)
    
with col2:
    pass

footer()