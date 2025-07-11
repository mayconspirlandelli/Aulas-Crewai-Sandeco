import streamlit as st
from crews.search_crew import CrewSearch

def render_search_page():

    # Configuração do Streamlit
    st.title('Sistema de Pesquisa com CrewAI')
    tema = st.text_input('Digite o tópico para pesquisar na internet', 'Oportunidades para Desenvolvedor de IA no Brasil')


    # Botão para iniciar o processo
    if st.button('Iniciar Processo'):
        
        #Quanto clicar no botão carrega um loader
        with st.spinner('Executando tarefas do Crew...'):
            crew_search = CrewSearch()
            result = crew_search.kickoff(inputs={'topic': tema})
            st.success('Processo concluído!')

        # Exibindo resultados
        st.subheader('Conteúdo Pesquisado')
        st.write(result)
