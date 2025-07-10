import streamlit as st

def render_about_page():
    st.title("Sobre a Agentic Platform")

    st.write("""
    A **Agentic Platform** é uma solução inovadora criada para facilitar a criação, execução e gestão de agentes inteligentes,
    integrando modelos de linguagem (LLMs), ferramentas externas e automações complexas de forma intuitiva e escalável.

    Nosso objetivo é democratizar o uso da inteligência artificial baseada em agentes, permitindo que profissionais de diversas áreas
    – como educação, negócios, saúde, direito e tecnologia – possam construir fluxos de trabalho autônomos que combinam raciocínio,
    acesso à informação, e execução de tarefas com o mínimo de intervenção manual.

    A plataforma se apoia no conceito de agentes coordenados (multiagentes) com papéis definidos, atuando em colaboração para atingir
    objetivos claros, como análise de dados, geração de relatórios, atendimento a clientes, e muito mais.
    """)

    st.markdown("---")

    st.markdown("🔗 Acesse o site oficial: [www.agenticplatform.ai](https://www.agenticplatform.ai)")
