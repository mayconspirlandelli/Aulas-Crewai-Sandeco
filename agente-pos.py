from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool
from crewai import LLM
import json
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from crewai_tools import FirecrawlSearchTool

# Página de exemplo (troque pela URL que desejar)
url = "https://escoladepos.ufg.br/cursos/atendimento-de-criancas-e-adolescentes-vitimas-ou-testemunhas-de-violencia/"
#url = "https://escoladepos.ufg.br/cursos/banco-de-dados-com-big-data/"

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()  # Isso carrega as variáveis do .env para os.environ

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")


llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0,
    api_key=GOOGLE_API_KEY,
)


# Ferramenta para raspagem de site
scraper_tool = ScrapeWebsiteTool()


# Agente que usa a ferramenta de scraping
agente_extracao = Agent(
    role="Agente de Coleta de Informações de Sites",
    goal="Extrair informacoes dos curso de pós-graduação da UFG. Voce deve caputra informaçoes sobre o curso, como nome, descrição, data de início e valor.",
    backstory="Especialista em web scraping de lojas online e coleta de informações relevantes.",
    verbose=True,
    memory=True,
    llm=llm,
    tools=[scraper_tool]
)


# Tarefa que instrui o agente a usar a ferramenta
extrair_informacoes_site = Task(
    description=f"""
    Acesse o site {url} e extraia informaçoes relativas ao curso de pós-graduação da UFG.
    Para cada curso, colete:
    - Nome do curso
    - Descrição resumida
    - Carga horário do curso
    - Curso é on-line, presencial ou híbrido
    - Informações sobre o curso
    - Edital está diponível ou não.
    - Data de início do curso
    - Qual valor da mensalidade do curso.

    Formate a saída como uma lista em JSON.
    """,
    expected_output="Uma lista JSON contendo nome, descrição e preço de cada produto.",
    tools=[scraper_tool],
    agent=agente_extracao
)

agente_formatador_json = Agent(
    role="Agente Responsavel por Formatação JSON",
    goal="Extrair lista de produtos, descrições e preços de um site de e-commerce",
    backstory="Especialista em web scraping de lojas online e coleta de informações relevantes.",
    verbose=True,
    memory=True,
    llm=llm,
    tools=[scraper_tool]
)

formatar_json = Task(
    description=f"""
    Formate a saída como uma lista em JSON com os seguintes campos para cada produto coletado:
    - Nome do curso,
    - Descrição resumida,
    - Carga horário do curso,
    - Curso é on-line, presencial ou híbrido,
    - Informações sobre o curso,
    - Edital está diponível ou não,
    - Data de início do curso,
    - Qual valor da mensalidade do curso.
    """,
    expected_output="Uma lista JSON contendo todos as informações coletadas do site.",
    tools=[scraper_tool],
    agent=agente_formatador_json
)

# Criar a equipe e processar
equipe = Crew(
    agents=[agente_extracao, agente_formatador_json],
    tasks=[extrair_informacoes_site, formatar_json],
    process=Process.sequential,
    llm=llm,
    verbose=True
)




# Executar
resultado = equipe.kickoff(inputs={'url': url})

print(resultado)

# with open("resultado_scraping.json", "w", encoding="utf-8") as f:
#     json.dump(saida_json, f, ensure_ascii=False, indent=2)

print("✅ Resultado salvo em 'resultado_scraping.json'")
