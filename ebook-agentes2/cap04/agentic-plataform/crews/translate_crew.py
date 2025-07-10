import os
from crewai import Agent, Task, Crew, Process
from util.llm_helper import LLMHelper

class CrewTranslate:

    def __init__(self):
        # Obter instância da LLM com configuração padrão
        self.llm = LLMHelper.get_llm()
        self.crew = self._criar_crew()
    

    def _criar_crew(self):
      
        # Agente Tradutor
        tradutor = Agent(
            role="Tradutor de idiomas",
            goal="Traduzir {texto_original} de forma precisa para o idioma {idioma_destino}",
            backstory="Você é um tradutor profissional com domínio de vários idiomas. Seu objetivo é realizar traduções precisas e naturais de textos enviados por usuários.",
            verbose=True,
            memory=True,
            llm=self.llm
        )

        # Tarefa de tradução
        traducao_tarefa = Task(
            description="Traduzir o seguinte {texto_original} para {idioma_destino}: ",
            expected_output="Texto traduzido de forma precisa e natural",
            agent=tradutor,
            llm=self.llm
        )

        # Criação do Crew com a tarefa
        self.crew = Crew(
            agents=[tradutor],
            tasks=[traducao_tarefa],
            process=Process.sequential,
            verbose=True,
            llm=self.llm
        )

    # def kickoff(self, inputs):
    #     # Cria o crew com base nas entradas
    #     resposta = self.crew.kickoff(inputs=inputs)     
    #     return resposta.raw

    def kickoff(self, inputs: dict):
        texto_original = inputs.get('texto_original')
        idioma_destino = inputs.get('idioma_destino')

        if not texto_original or not idioma_destino:
            raise ValueError("As chaves 'texto_original' e 'idioma_destino' são obrigatórias em inputs.")

        #self._criar_crew(texto_original, idioma_destino)
        self._criar_crew()
        resultado = self.crew.kickoff(inputs=inputs)  # permite uso de inputs em Tasks, se necessário
        return resultado.raw

