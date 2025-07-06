from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from graph_tool import CustomGraphTool
from pdf_creator import PDFCreationTool  # Supondo que a ferramenta foi implementada como descrito
from util.MyLLM import MyLLM
from util.llm_helper import LLMHelper

# Obter instância da LLM com configuração padrão
llm = LLMHelper.get_llm()

# Ferramenta para pesquisar informações sobre matriz energética usando o SerperDevTool
serper_tool = SerperDevTool()
serper_tool.n_results = 50

# Agente responsável por pesquisar dados sobre matriz energética mundial usando o SerperDevTool
research_agent = Agent(
    role="Pesquisador de Matriz Energética",
    goal="""Pesquisar a previsão de consumo energético global por tipo de fonte para o ano de 2025, incluindo porcentagens 
    de uso para as seguintes fontes: Petróleo e derivados, Carvão, Gás natural, Hidráulica, Nuclear, Biomassa e Outras renováveis.""",
    backstory="Especialista em pesquisa de dados energéticos e fontes de energia sustentáveis.",
    tools=[serper_tool],
    allow_delegation=False,
    verbose=True
)

# Agente responsável por criar o gráfico com base nos dados fornecidos
graph_agent = Agent(
    role="Criador de Gráficos",
    goal="Gerar um gráfico de pizza visual com base nos dados de matriz energética fornecidos.",
    backstory="""Você é especialista em visualização de dados e transforma dados 
    numéricos em gráficos claros e informativos.""",
    tools=[CustomGraphTool()],  # Integrando a ferramenta de criação de gráficos
    allow_delegation=False,
    verbose=True
)

# Novo agente escritor que utiliza a ferramenta PDFCreationTool
writer_agent = Agent(
    role="Escritor de Relatórios",
    goal="Escrever um relatório explicativo sobre os dados energéticos e criar um PDF com as informações e o gráfico.",
    backstory="Você é um especialista em redação de relatórios sobre temas complexos, especialmente relacionados a dados energéticos.",
    tools=[PDFCreationTool()],
    allow_delegation=False,
    verbose=True
)

# Task para o agente Pesquisador de Matriz Energética usar o SerperDevTool para buscar dados de consumo de energia
energy_research_task = Task(
    description="""Use o SerperDevTool para pesquisar a previsão de consumo energético global por tipo de fonte 
    para o ano de 2025. As fontes de energia devem incluir: Petróleo e derivados, Carvão, Gás natural, Hidráulica, 
    Nuclear, Biomassa e Outras renováveis (incluindo solar, eólica e geotérmica). As pesquisas na web devem ser feitas 
    em fontes renomadas e retornar porcentagens para cada tipo de fonte.""",
    expected_output="""Um dicionário com as porcentagens de consumo energético previstas para cada fonte em 2025:
    {
        "Petróleo e Derivados": <valor>%, 
        "Carvão": <valor>%, 
        "Gás Natural": <valor>%, 
        "Hidráulica": <valor>%, 
        "Nuclear": <valor>%, 
        "Biomassa": <valor>%, 
        "Outras Renováveis": <valor>%
    }""",
    tools=[serper_tool],  # Ferramenta de pesquisa usada na tarefa
    agent=research_agent  # Associando o agente de pesquisa de matriz energética à tarefa
)

# Task para o agente Criador de Gráficos usar a CustomGraphTool e gerar um gráfico de pizza
graph_creation_task = Task(
    description="""Utilize os dados de consumo energético previstos para 2025 para criar um gráfico de pizza 
    que ilustre a distribuição percentual de cada tipo de fonte de energia: Petróleo e derivados, Carvão, Gás natural, 
    Hidráulica, Nuclear, Biomassa e Outras renováveis.""",
    expected_output="Um gráfico de pizza salvo como arquivo PNG que mostra a distribuição percentual da matriz energética em 2025.",
    tools=[CustomGraphTool()],  # Ferramenta usada na tarefa para gerar o gráfico
    context=[energy_research_task],
    agent=graph_agent  # Associando o agente de criação de gráficos à tarefa
)

# Task para o agente escritor criar um relatório em PDF com o gráfico e uma análise textual
report_creation_task = Task(
    description="""Escreva um relatório explicativo de cinco parágrafos sobre os dados energéticos fornecidos, abordando a 
    importância de cada fonte de energia e as previsões de consumo para 2025. Em seguida, utilize a ferramenta PDFCreationTool 
    para criar um PDF com o título 'Relatório de Consumo Energético 2025', incluindo o texto explicativo e o gráfico gerado.""",
    expected_output="Um arquivo PDF contendo o relatório explicativo e o gráfico da matriz energética, salvo com o nome 'Relatorio_Consumo_Energetico_2025.pdf'.",
    tools=[PDFCreationTool()],
    context=[energy_research_task, graph_creation_task],
    agent=writer_agent  # Associando o agente escritor à tarefa de criação do relatório
)

# Criando a crew que organiza o processo com os três agentes e suas tarefas
energy_report_crew = Crew(
    agents=[research_agent, graph_agent, writer_agent],  # Agentes: pesquisador, criador de gráficos e escritor de relatórios
    tasks=[energy_research_task, graph_creation_task, report_creation_task],  # Tarefas: pesquisa, criação de gráfico e criação de relatório
    process=Process.sequential  # Processo sequencial para que a pesquisa e o gráfico ocorram antes da criação do relatório
)

# Iniciando a crew para realizar a tarefa completa de pesquisa, visualização e relatório
result = energy_report_crew.kickoff(inputs={})
print(f"Resultado final da Crew: {result}")
