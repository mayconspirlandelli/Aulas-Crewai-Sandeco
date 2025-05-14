from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool
from crewai import LLM
import json
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from crewai_tools import FirecrawlSearchTool



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

# Página de exemplo (troque pela URL que desejar)
url = "https://anaformigadoces.goomer.app/menu"


# Ferramenta para raspagem de site
scraper_tool = ScrapeWebsiteTool(website_url=url)
text = scraper_tool.run()
print(text)


firecraw_tool = FirecrawlSearchTool(api_key=FIRECRAWL_API_KEY,
                                     query='Quais são os produtos?')

# Agente que usa a ferramenta de scraping
agente_scraper = Agent(
    role="Agente de Coleta de Produtos",
    goal="Extrair lista de produtos, descrições e preços de um site de e-commerce",
    backstory="Especialista em web scraping de lojas online.",
    tools=[firecraw_tool],
    llm=llm
)


# Tarefa que instrui o agente a usar a ferramenta
tarefa_scraping = Task(
    description=f"""
    Acesse o site {url} e extraia uma lista estruturada de produtos disponíveis.
    Para cada produto, colete:
    - Nome do produto
    - Descrição resumida
    - Preço

    Formate a saída como uma lista em JSON.
    """,
    expected_output="Uma lista JSON contendo nome, descrição e preço de cada produto.",
    agent=agente_scraper


    # description=f"Use a ferramenta para extrair o conteúdo da página {url}. Extraia os produtos, suas descrições e preços.",
    # expected_output="Texto extraído da página em formato limpo.",
    # agent=agente_scraper
)

# Criar a equipe e processar
equipe = Crew(
    agents=[agente_scraper],
    tasks=[tarefa_scraping],
    process=Process.sequential,
    llm=llm,
    verbose=True
)

# Executar
resultado = equipe.kickoff()

# Salvar o resultado em JSON
saida_json = {
    "url": url,
    "conteudo_extraido": resultado
}

print(resultado)

# with open("resultado_scraping.json", "w", encoding="utf-8") as f:
#     json.dump(saida_json, f, ensure_ascii=False, indent=2)

print("✅ Resultado salvo em 'resultado_scraping.json'")
