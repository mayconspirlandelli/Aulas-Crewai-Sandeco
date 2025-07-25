import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool
from dotenv import load_dotenv
from util.llm_helper import LLMHelper

class CrewPDFResumo:

    def __init__(self, pdf_path):
        self.llm = LLMHelper.get_llm()  # Obter instância da LLM com configuração padrão
        #self.pdf_tool = PDFSearchTool(pdf_path)  # Tool nativa do CrewAI para leitura de PDF

        # Para ler PDF usando Gemini.
        self.pdf_tool = PDFSearchTool(
            pdf_path,
            config=dict(
                llm=dict(
                    provider="google", # or google, openai, anthropic, llama2, ...
                    config=dict(
                        model="gemini/gemini-2.0-flash",
                        temperature=0.5,
                        api_key=os.environ.get("GOOGLE_API_KEY"),
                        # temperature=0.5,
                        # top_p=1,
                        # stream=true,
                    ),
                ),
                embedder=dict(
                    provider="google", # or openai, ollama, ...
                    config=dict(
                        model="models/embedding-001",
                        task_type="retrieval_document",
                        # title="Embeddings",
                    ),
                ),
            )
        )
        self.crew = self._criar_crew()

    def _criar_crew(self):
        # Definindo o agente resumidor
        resumidor = Agent(
            role='''Resumidor''',
            goal='''Criar um resumo do conteúdo de um PDF.''',
            verbose=True,
            llm=self.llm,
            memory=True,
            # backstory='''Você é um especialista em 
            #             sintetizar informações de documentos extensos. 
            #             Seu objetivo é identificar os pontos principais e 
            #             entregar um resumo conciso e útil.''',
            backstory="""
            Voce é especialista em resmuir atas de reunião. 
            Nesta ata voce deve identficar quais sao os projetos, eventos, extensão e pesquisa.
            """,         
            tools=[self.pdf_tool]  # Associando a tool de leitura de PDF ao agente
        )

        # Tarefa de resumo
        resumo_tarefa = Task(
            # description='''Leia o conteúdo do PDF fornecido 
            #                 usando a tool integrada. 
            #                 Produza um resumo objetivo, 
            #                 destacando os principais pontos 
            #                 e ideias essenciais.''',
            description="""
                Leia o conteduo do PDF fornecido usando a tool integrada. 
                Produza uma resumo objetivo destacando quais sao os projetos, eventos, extensão e pesquisa.
            """,
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
