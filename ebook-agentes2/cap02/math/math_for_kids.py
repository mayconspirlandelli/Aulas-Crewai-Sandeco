from crewai import Agent, Task, Crew, Process, LLM
from math_tool import MultiplicationTool
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Definir o modelo de linguagem
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0,
    api_key=GOOGLE_API_KEY,
)

# Criando a instância da ferramenta
multiplication_tool = MultiplicationTool()

# Definindo o agente que gera números aleatórios solicitando à LLM
generator_agent = Agent(
    role="Gerador de Números",
    goal="Você cria dois números aleatórios para serem multiplicados.",
    backstory="Você é especialista em gerar números aleatórios.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

# Definindo o agente que realiza a multiplicação
writer_agent = Agent(
    role="Escritor",
    goal="Você escreve lições de matemática para crianças.",
    backstory="""Você é um especialista em redação e adora ensinar crianças, mas não sabe nada de matemática.""",
    tools=[multiplication_tool],  # Integrando a ferramenta ao agente
    allow_delegation=False,
    llm=llm, 
    verbose=True
)

# Task para o agente Gerador de Números solicitar à LLM dois números aleatórios
generate_numbers_task = Task(
    description="Peça à LLM para gerar dois números aleatórios entre 1 e 10.",
    expected_output="Dois números aleatórios para serem multiplicados.",
    agent=generator_agent  # Associando o agente de geração de números à tarefa
)

# Task para o agente Multiplicador multiplicar os números fornecidos
multiplication_task = Task(
    description="""
    Ensine a multiplicação para crianças.     
    Multiplique os dois números fornecidos pelo agente Gerador de Números.
    Quando você for ensinar use maçãs (emojs) para explicar em um texto como funciona a multiplicação na linguagem 
    para crianças""",
    expected_output="""Uma explicação para crianças sobre multilicação.  
    O primeiro número aleatório representa a quantidade de sacolas 
    e o segundo número aleatório representa a quantidade de maçãs
    como mostra o exemplo delimitado por <exemplo>

    <exemplo>
    sacolas de maçãs:
    sacola 1: 🍎🍎🍎🍎
    sacola 2: 🍎🍎🍎🍎
    sacola 3: 🍎🍎🍎🍎

    Portanto: 3 x 4 = 12 maçãs
    
    </exemplo>
    """,
    tools=[multiplication_tool],  # Ferramenta usada na tarefa
    agent=writer_agent, # Associando o agente de multiplicação à tarefa
    context=[generate_numbers_task]
)

# Criando a crew que organiza o processo com os dois agentes e suas tasks
math_crew = Crew(
    agents=[generator_agent, writer_agent],
    tasks=[generate_numbers_task, multiplication_task],
    process=Process.sequential  # Processo sequencial de execução
)

# Iniciando a crew para realizar a tarefa completa
result = math_crew.kickoff(inputs={})
print(f"Resultado final da Crew: {result}")
