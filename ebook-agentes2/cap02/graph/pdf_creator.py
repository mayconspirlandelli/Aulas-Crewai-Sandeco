from crewai.tools import BaseTool
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os

class PDFCreationTool(BaseTool):
    name: str = "PDF Creation Tool"
    description: str = """This tool generates a PDF file that includes a title, 
    a description, and an image. It is useful for creating report-like outputs 
    with visual elements embedded."""

    def _run(self, title: str, text: str, image_path: str, output_path: str = "output.pdf") -> str:
        """
        Gera um PDF contendo o título, texto e uma imagem especificada.

        Args:
            title (str): O título a ser exibido no PDF.
            text (str): O texto a ser incluído como descrição do gráfico.
            image_path (str): O caminho para a imagem a ser incluída no PDF.
            output_path (str): O caminho onde o PDF será salvo. O padrão é "output.pdf".

        Returns:
            str: Uma mensagem indicando o sucesso da operação e o caminho do arquivo PDF gerado.
        """
        # Verifica se o arquivo de imagem existe
        if not os.path.exists(image_path):
            return f"Erro: o arquivo de imagem em '{image_path}' não foi encontrado."

        # Criação do PDF usando ReportLab
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        margin = 50  # margem para evitar cortes nas bordas

        # Função para dividir o texto em linhas de acordo com a largura do PDF
        def draw_wrapped_text(c, text, x, y, max_width):
            lines = []
            words = text.split()
            current_line = ""
            for word in words:
                # Testa se adicionar a próxima palavra ultrapassará o limite
                if c.stringWidth(current_line + " " + word, "Helvetica", 12) < max_width:
                    current_line += " " + word if current_line else word
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)  # Adiciona a última linha

            # Desenha cada linha no PDF
            for line in lines:
                c.drawString(x, y, line)
                y -= 15  # Espaço entre as linhas
            return y

        # Adiciona o título ao PDF
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin, height - 50, title)

        # Adiciona o texto como descrição no PDF com quebra de linha automática
        c.setFont("Helvetica", 12)
        y_position = height - 80
        y_position = draw_wrapped_text(c, text, margin, y_position, width - 2 * margin)

        # Adiciona a imagem no PDF
        try:
            image = ImageReader(image_path)
            c.drawImage(image, margin, y_position - 300, width=width - 2 * margin, height=250, preserveAspectRatio=True)
        except Exception as e:
            return f"Erro ao inserir a imagem no PDF: {e}"

        # Finaliza o PDF
        c.showPage()
        c.save()

        return f"output_path"
