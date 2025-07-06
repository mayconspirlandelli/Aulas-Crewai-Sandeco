from crewai.tools import BaseTool

# Definindo a classe MultiplicationTool sem o uso de decoradores
class MultiplicationTool(BaseTool):
    name: str = "Ferramenta de Multiplicação"
    description: str = "Útil para quando você precisa multiplicar dois números."

    def _run(self, primeiro_numero: int, segundo_numero: int) -> str:
        resultado = primeiro_numero * segundo_numero
        return f"O resultado da multiplicação de {primeiro_numero} e {segundo_numero} é {resultado}."