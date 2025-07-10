import streamlit as st

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
            # Aqui entraria a chamada para o agente CrewTranslate
            texto_traduzido = simular_traducao(texto_original, idiomas[idioma_destino])

            st.subheader("Texto Traduzido:")
            st.success(texto_traduzido)

# Simulador de tradução (temporário — substitua depois pelo agente CrewAI)
def simular_traducao(texto, idioma):
    return f"[Tradução simulada para {idioma.upper()}] {texto}"
