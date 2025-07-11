from crewai import Agent, Task, Crew, Process
from util.llm_helper import LLMHelper
from langchain.tools import DuckDuckGoSearchRun
import MyCustomDuckDuckGoTool


# @tool('DuckDuckGoSearch')
# def search_tool(search_query: str):
#     """Search the web for information on a given topic"""
#     return DuckDuckGoSearchRun().run(search_query)


class CrewSearch:

    def __init__(self):
        
        #self.search_tool = DuckDuckGoSearchRun()
        self.search_tool = MyCustomDuckDuckGoTool()
        # Obter instância da LLM com configuração padrão
        self.llm = LLMHelper.get_llm()
        self.crew = self._criar_crew()

    def _criar_crew(self):
        
        # Definindo os agentes
        buscador = Agent(
            role='Buscador de Conteúdo',
            goal='Buscar conteúdo on line sobre {tema}',
            verbose=True,
            llm=self.llm,
            memory=True,
            backstory="""
                Você está trabalhando na criação de artigos em português para o LinkedIn sobre o {tema}.
                Você vai fazer uma busca sobre informações na internet, coletá-las e agrupá-las e se necessário, traduzi-las para português.
                Seu trabalho servirá como base para o Escritor de Conteúdo.
                """,
            tools=[self.search_tool]
        )

        escritor = Agent(
            role = 'Escritor de conteúdo',
            goal = 'Escrever um texto para o Linkedin sobre {tema}',
            backstory = ''''
                        Você está trabalhando na redação de um artigo para o LinkedIn sobre {tema}.
                        Você vai utilizar os dados coletados pelo Buscador de Conteúdo para escrever um texto em português.
                        O artigo deve ter um tom divertido mas factualmente correto.
                        ''',
            tools = [search_tool],
            verbose=True,
            memory=True,
            llm=self.llm
        )

        revisor = Agent(
            role = 'Editor de Conteúdo',
            goal = 'Editar um texto de LinkedIn para que o mesmo seja factualmente correto e tenha um tom informal e divertido.',
            backstory = ''''
                        Você está trabalhando na edição e correção de um artigo para o LinkedIn.
                        Você vai receber um texto do Escritor de Conteúdo e vai revisá-lo e editá-lo.
                        Seu texto para a publicação deve ser em português.
                        ''',
            tools = [search_tool],
            verbose=True,
            memory=True,
            llm=self.llm
        )

        # Tarefas
        buscar_tarefa = Task(
            description=
                '''
                1. Priorize as últimas tendências, os principais atores e as notícias mais relevantes sobre o {tema}.\n
                2. Identifique o público-alvo, considerando seus interesses e pontos de dor.\n
                3. Inclua palavras-chave de SEO e o dados de fontes relevantes.
                ''',
            agent=buscador,
            tools=[self.search_tool],
            llm=self.llm,
            expected_output='Um plano de tendências sobre {tema} com as palavras mais relevantes de SEO e as últimas notícias.'
        )

        escrever_tarefa = Task(
            description='''
                1. Use os dados coletados de conteúdo para criar um post de LinkedIn atraente sobre o {tema}.\n
                2. Incorpore palavras-chave de SEO de forma natural. \n
                3. Certifique-se de que o post esteja estruturado de forma cativante, com uma conclusão que faça o leitor refletir. \n
                ''',
            agent=escritor,
            tools=[self.search_tool],
            llm=self.llm,
            context=[buscar_tarefa],
            expected_output='Um texto sobre {tema} para o Linkedin.'
        )
        
        revisar_tarefa = Task(
            description=("Revisar a postagem de LinkedIn em questão quanto a erros gramaticais"
            ),
            agent=revisor,
            tools=[self.search_tool],
            llm=self.llm,
            context=[escrever_tarefa],
            expected_output='Um texto de Linkedin pronto para a publicação. O texto está separado em parágrafos e não utiliza bullet point'
        )

        # Criando o Crew
        return Crew(
            agents=[buscador, escritor, revisor],
            tasks=[buscar_tarefa, escrever_tarefa, revisar_tarefa],
            process=Process.sequential
        )

    def kickoff(self, inputs):
        # Executa o Crew com o tópico fornecido
        resposta = self.crew.kickoff(inputs=inputs)     
        return resposta.raw
