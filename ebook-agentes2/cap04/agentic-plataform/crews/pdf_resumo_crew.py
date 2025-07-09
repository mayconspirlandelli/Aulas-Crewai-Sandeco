import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool
from dotenv import load_dotenv
from util.llm_helper import LLMHelper

#load_dotenv()

class CrewPDFResumo:

    def __init__(self, pdf_path):
        self.llm = LLMHelper.get_llm()  # Obter instância da LLM com configuração padrão
        self.pdf_tool = PDFSearchTool(pdf_path)  # Tool nativa do CrewAI para leitura de PDF
        
        
        self.llm = "gpt-4o-mini"  # Configuração do modelo LLM        
        self.crew = self._criar_crew()

    def _criar_crew(self):
        # Definindo o agente resumidor
        resumidor = Agent(
            role='''Resumidor''',
            goal='''Criar um resumo do conteúdo de um PDF.''',
            verbose=True,
            llm=self.llm,
            memory=True,
            backstory='''Você é um especialista em 
                        sintetizar informações de documentos extensos. 
                        Seu objetivo é identificar os pontos principais e 
                        entregar um resumo conciso e útil.''',
            tools=[self.pdf_tool]  # Associando a tool de leitura de PDF ao agente
        )

        # Tarefa de resumo
        resumo_tarefa = Task(
            description='''Leia o conteúdo do PDF fornecido 
                            usando a tool integrada. 
                            Produza um resumo objetivo, 
                            destacando os principais pontos 
                            e ideias essenciais.''',
            expected_output='''Um resumo claro e objetivo 
                        do conteúdo do PDF.''',
            llm=self.llm,
            agent=resumidor
        )

        # Criando o Crew
        return Crew(
            agents=[resumidor],
            tasks=[resumo_tarefa],
            process=Process.sequential
        )

    def kickoff(self):
        # Executa o Crew com o caminho do PDF como entrada
        resposta = self.crew.kickoff()
        return resposta.raw
