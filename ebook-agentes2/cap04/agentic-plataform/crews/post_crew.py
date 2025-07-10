from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from util.llm_helper import LLMHelper

class CrewPostagem:

    def __init__(self):
        
        self.search_tool = SerperDevTool()
        # Obter instância da LLM com configuração padrão
        self.llm = LLMHelper.get_llm()
        #self.llm = "gpt-4o-mini"
        
        self.crew = self._criar_crew()

    def _criar_crew(self):
        
        # Definindo os agentes
        pesquisador = Agent(
            role='Pesquisador',
            goal='Encontrar informações relevantes sobre {topic}',
            verbose=True,
            llm=self.llm,
            memory=True,
            backstory=(
                'Você é um pesquisador especializado em descobrir informações'
                ' úteis e relevantes para escrever sobre {topic}.'
            ),
            tools=[self.search_tool]
        )

        escritor = Agent(
            role='Escritor',
            goal='Criar uma postagem convincente sobre {topic}',
            verbose=True,
            memory=True,
            llm=self.llm,
            backstory=(
                'Você é um redator experiente que transforma informações em'
                ' conteúdos interessantes e informativos.'
            )
        )

        revisor = Agent(
            role='Revisor',
            goal='Revisar e melhorar a postagem sobre {topic}',
            verbose=True,
            memory=True,
            llm=self.llm,
            backstory=(
                'Você é um revisor detalhista, especializado em ajustar o tom,'
                ' a clareza e a gramática de textos.'
            )
        )

        # Tarefas
        pesquisa_tarefa = Task(
            description=(
                'Pesquise informações detalhadas sobre {topic}.'
                ' Foque em identificar pontos importantes e um resumo geral.'
            ),
            expected_output='Um resumo detalhado sobre {topic}.',
            tools=[self.search_tool],
            llm=self.llm,
            agent=pesquisador,
        )

        escrita_tarefa = Task(
            description=(
                'Escreva uma postagem com base no conteúdo pesquisado.'
                ' A postagem deve ser clara, interessante e envolvente.'
            ),
            expected_output='Uma postagem completa sobre {topic} com 3 parágrafos.',
            agent=escritor,
            llm=self.llm,
            context=[pesquisa_tarefa]
        )

        revisao_tarefa = Task(
            description=(
                'Reveja a postagem criada, ajustando a clareza e corrigindo possíveis erros.'
            ),
            expected_output='Uma postagem revisada e otimizada.',
            agent=revisor,
            llm=self.llm,
            context=[escrita_tarefa]
        )

        # Criando o Crew
        return Crew(
            agents=[pesquisador, escritor, revisor],
            tasks=[pesquisa_tarefa, escrita_tarefa, revisao_tarefa],
            process=Process.sequential
        )

    def kickoff(self, inputs):
        # Executa o Crew com o tópico fornecido
        resposta = self.crew.kickoff(inputs=inputs)     
        return resposta.raw
