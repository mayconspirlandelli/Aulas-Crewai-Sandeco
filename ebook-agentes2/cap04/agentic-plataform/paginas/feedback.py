import streamlit as st

def render_feedback_page():
    st.title("Página de Feedback 💬")
    st.write("Veja abaixo exemplos de mensagens de diferentes tipos de feedback no Streamlit.")

    # Mensagem de Sucesso
    st.subheader("✅ Mensagem de Sucesso")
    st.success("Sua operação foi concluída com sucesso! Tudo ocorreu como esperado.")

    # Mensagem de Erro
    st.subheader("❌ Mensagem de Erro")
    st.error("Ocorreu um erro ao tentar processar sua solicitação. Verifique os dados e tente novamente.")

    # Mensagem de Informação
    st.subheader("ℹ️ Mensagem Informativa")
    st.info("Esta é uma mensagem informativa para orientar o usuário durante o uso da plataforma.")
