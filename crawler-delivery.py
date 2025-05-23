from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool
from crewai import LLM
import json
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from crewai_tools import FirecrawlSearchTool

# Página de exemplo (troque pela URL que desejar)
url = "https://anaformigadoces.goomer.app/menu"

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()  # Isso carrega as variáveis do .env para os.environ

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# class Produtos(BaseModel):
#     nome: str
#     descricao: str
#     preco: str

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0,
    api_key=GOOGLE_API_KEY,
)


# Ferramenta para raspagem de site
scraper_tool = ScrapeWebsiteTool()
# text = scraper_tool.run()
# print(text)


# firecraw_tool = FirecrawlSearchTool(api_key=FIRECRAWL_API_KEY,
#                                      query='Quais são os produtos?')

# Agente que usa a ferramenta de scraping
agente_extracao = Agent(
    role="Agente de Coleta de Produtos de Sites",
    goal="Extrair lista de produtos, descrições e preços de um site de e-commerce",
    backstory="Especialista em web scraping de lojas online e coleta de informações relevantes.",
    verbose=True,
    memory=True,
    llm=llm,
    tools=[scraper_tool]
)


# Tarefa que instrui o agente a usar a ferramenta
extrair_informacoes_site = Task(
    description=f"""
    Acesse o site {url} e extraia uma lista estruturada de produtos disponíveis.
    Para cada produto, colete:
    - Nome do produto
    - Descrição resumida
    - Preço

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
    - Nome do produto
    - Descrição resumida
    - Preço
    """,
    expected_output="Uma lista JSON contendo nome, descrição e preço de cada produto.",
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
