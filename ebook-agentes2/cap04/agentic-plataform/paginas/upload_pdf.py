import os
import time  # Adicionado para simular um tempo de processamento
import streamlit as st
from crews.pdf_resumo_crew import CrewPDFResumo

# Configuração do diretório temporário
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


def render_upload_page():

    # Título da aplicação
    st.title("Resumidor de PDF")

    # Instruções para o usuário
    st.write("Faça upload de um arquivo PDF para resumir seu conteúdo.")

    # Controle deslizante para limitar caracteres
    max_chars = st.slider(
        "Limite de caracteres do resumo",
        min_value=100,
        max_value=2000,
        value=600,
        step=50
    )

    # Elemento de upload de arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

    if uploaded_file is not None:
        try:
            
            # Salvando o arquivo no diretório temporário
            temp_file_path = os.path.join(TEMP_DIR, uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"Upload Realizado com sucesso: {uploaded_file.name}")
                
            st.info("Resumindo PDF com agentes")

            # Loader durante a execução da tarefa
            with st.spinner('Executando tarefas do Crew...'):
                
                crew = CrewPDFResumo(temp_file_path)
                time.sleep(1)  # Simulando um pequeno atraso (remova na produção)
                resumo_completo = crew.kickoff() # Certifique-se de que esta é a tarefa demorada
                #resultado = crew.kickoff()  

                # Ajustar o texto com base no limite
                resumo_cortado = resumo_completo[:max_chars] + "..." if len(resumo_completo) > max_chars else resumo_completo

            st.text_area("Resumo via agentes:", resumo_cortado, height=300)

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")


