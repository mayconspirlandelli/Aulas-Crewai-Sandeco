import streamlit as st
from crews.translate_crew import CrewTranslate

def render_translate_page():
    st.title("CrewTranslate: Tradução de Textos")

    st.write("Insira o texto que deseja traduzir e escolha o idioma de destino:")

    # Entrada de texto
    texto_original = st.text_area("Texto original", height=200)

    # Idiomas disponíveis para tradução
    idiomas = {
        "Inglês": "en",
        "Espanhol": "es",
        "Francês": "fr",
        "Alemão": "de",
        "Português": "pt",
        "Italiano": "it"
    }

    idioma_destino = st.selectbox("Idioma de destino", list(idiomas.keys()))

    # Botão para acionar a tradução
    if st.button("Traduzir"):
        if texto_original.strip() == "":
            st.warning("Por favor, insira um texto para traduzir.")
        else:
            
            crew_translate = CrewTranslate()
            traducao = crew_translate.kickoff(inputs={
                    'texto_original': texto_original,
                    'idioma_destino': idioma_destino
            })
        st.subheader("Texto Traduzido:")
        st.success(traducao)