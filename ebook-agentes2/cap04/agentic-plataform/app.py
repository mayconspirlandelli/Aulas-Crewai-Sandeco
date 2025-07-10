import streamlit as st
from streamlit_option_menu import option_menu
from images._my_images import Image
from paginas.welcome import render_welcome
from paginas.post import render_post_page
from paginas.upload_pdf import render_upload_page
from paginas.about_page import render_about_page
from paginas.settings import render_settings_page
from paginas.translate import render_translate_page

st.sidebar.image(
    Image.LOGO,
    use_container_width=True,
    width=200
)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Agentic Platform",  # Título do menu
        options=["Home", "PostAgent", "SummaryPDF", "AboutPage", "Settings", "Translate"],  # Opções do menu
        icons=['house','file-earmark-text','cloud-upload', "info", "gear", "globe"],
        menu_icon='robot',
        default_index=0,
        orientation="vertical" #teste com "horizontal"
    )

st.sidebar.image(
    Image.POWERED,
    use_container_width=True,
    width=200
)

# Conteúdo baseado na opção selecionada
if selected == "Home":
    
    #render_welcome()
    render_translate_page()

elif selected == "PostAgent":
    render_post_page()

elif selected == "SummaryPDF":
    render_upload_page()

elif selected == "AboutPage":
    render_about_page()

elif selected == "Settings":
    render_settings_page()

elif selected == "Translate":
    render_translate_page()

