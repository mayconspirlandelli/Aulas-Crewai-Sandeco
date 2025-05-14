from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process, LLM


# Carregar variáveis de ambiente do arquivo .env
load_dotenv()  # Isso carrega as variáveis do .env para os.environ

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=GOOGLE_API_KEY,
)
# response = llm.call(
#     "Analyze the following messages and return the name, age, and breed. "
#     "Meet Kona! She is 3 years old and is a black german shepherd."
# )
# print(response)


# llm = "gemini/gemini-2.0-flash"

#Teste de conexão com o Google Generative AI
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     temperature=0.2
# )
# resposta = llm.invoke("Explique o que é aprendizado de máquina em uma frase simples.")
# print(resposta.content)


# Agente Pesquisador
pesquisador = Agent(
    role='Pesquisador de mercado',
    goal='Encontrar dados relevantes sobre o mercado de IA no Brasil',
    backstory='Especialista em análise de mercado com foco em tecnologia emergente.',
    llm=llm,
)

# Agente Escritor
escritor = Agent(
    role='Redator',
    goal='Escrever um artigo com base nas descobertas do pesquisador',
    backstory='Jornalista experiente que transforma informações complexas em conteúdo acessível.',
    llm=llm,
)

# Tarefas
tarefa_pesquisa = Task(
    description='Pesquisar sobre o mercado de IA no Brasil em 2024',
    agent=pesquisador,
    expected_output="Dados relevantes sobre o mercado de IA no Brasil em 2024",
)

tarefa_redacao = Task(
    description='Escrever um artigo com base nos dados de mercado encontrados',
    agent=escritor,
    expected_output="Um artigo sobre o mercado de IA no Brasil em 2024" # Added expected_output,
)


# Equipe
equipe = Crew(
    agents=[pesquisador, escritor],
    tasks=[tarefa_pesquisa, tarefa_redacao],
    #process=Process.hierarchical,
    process=Process.sequential,
    manager_llm=llm,
    llm=llm,
    memory=True,
    llm_provider="google",
    verbose=True,
)

# Execução
resultado = equipe.kickoff()
print(resultado)
