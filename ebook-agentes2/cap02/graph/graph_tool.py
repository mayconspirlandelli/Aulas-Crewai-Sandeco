from crewai.tools import BaseTool
import matplotlib.pyplot as plt

class CustomGraphTool(BaseTool):
    name: str = "Ferramenta de Criação de Gráficos"
    description: str = (
        """Gera um gráfico com base em uma lista de 
        valores e um tipo de gráfico especificado 
        (linha, barras ou pizza) e salva o gráfico 
        como um arquivo PNG."""
    )

    def _run(self, values: list, labels: list = None, chart_type: str = "linha", title: str = "Gráfico") -> str:
        # Escolhe o tipo de gráfico com base no parâmetro 'chart_type'
        plt.figure()
        
        if chart_type == "linha":
            plt.plot(values)
            plt.title(title)
        elif chart_type == "barras":
            plt.bar(range(len(values)), values, tick_label=labels)
            plt.title(title)
        elif chart_type == "pizza":
            if not labels:
                labels = [f"Item {i+1}" for i in range(len(values))]
            plt.pie(values, labels=labels, autopct='%1.1f%%')
            plt.title(title)
        else:
            return """Tipo de gráfico inválido. 
                      Escolha entre 'linha', 'barras' ou 'pizza'."""

        # Salva o gráfico como PNG
        file_name = f"{title.lower().replace(' ', '_')}.png"
        plt.savefig(file_name)
        plt.close()
        
        return f"Gráfico salvo como {file_name}"
