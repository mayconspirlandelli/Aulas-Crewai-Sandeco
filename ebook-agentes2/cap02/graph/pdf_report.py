import os
import markdown
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from bs4 import BeautifulSoup
from crewai.tools import BaseTool
from util.minhas_fontes import Fontes


pdfmetrics.registerFont(TTFont('Montserrat', Fontes.Montserrat))
pdfmetrics.registerFont(TTFont('Montserrat-Bold', Fontes.Montserrat_Bold))

class PDFReport(BaseTool):
    
    name: str = "PDF Creation Tool"

    description: str = """This tool generates a PDF file that includes a title, 
    a description, and an image. It is useful for creating report-like outputs 
    with visual elements embedded."""

    def markdown_to_paragraphs(self,markdown_content):
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content)
        
        # Prepare styles with justification
        styles = getSampleStyleSheet()
        
        # Custom justified style for normal text
        custom_style = ParagraphStyle(
            'JustifiedStyle',
            parent=styles['Normal'],
            fontName='Montserrat',
            fontSize=12,
            alignment=4  # 4 means fully justified
        )
        
        # Custom left-aligned heading styles
        heading1_style = ParagraphStyle(
            'LeftHeading1',
            parent=styles['Heading1'],
            fontName='Montserrat-Bold',
            alignment=0,  # 0 means left alignment
            fontSize=50
        )
        
        heading2_style = ParagraphStyle(
            'LeftHeading2',
            parent=styles['Heading2'],
            fontName='Montserrat-Bold',
            alignment=0,  # Left alignment
            fontSize=14
        )
        
        heading3_style = ParagraphStyle(
            'LeftHeading3',
            parent=styles['Heading3'],
            fontName='Montserrat-Bold',
            alignment=0,  # Left alignment
            fontSize=12
        )
        
        # Convert HTML to Reportlab Paragraphs
        soup = BeautifulSoup(html_content, 'html.parser')
        paragraphs = []
        
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'ul', 'ol']):
            if element.name == 'h1':
                paragraphs.append(Paragraph(element.get_text(), heading1_style))
            elif element.name == 'h2':
                paragraphs.append(Paragraph(element.get_text(), heading2_style))
            elif element.name == 'h3':
                paragraphs.append(Paragraph(element.get_text(), heading3_style))
            elif element.name in ['ul', 'ol']:
                # Handle lists with bullet points
                list_items = [f"• {li.get_text()}" for li in element.find_all('li')]
                for item in list_items:
                    paragraphs.append(Paragraph(item, custom_style))
            else:
                paragraphs.append(Paragraph(element.get_text(), custom_style))
        
        return paragraphs

    def _run(self, text: str, image_path: str, output_path: str = "output.pdf")-> str:
        # Unpack margins in order: top, left, right, bottom
        
        background_image = os.path.join('images', 'a4_fundo.png')
        
        custom_margins = (5*cm, 3*cm, 3*cm, 3*cm)
        
        top, left, right, bottom = custom_margins
        
        # Prepare PDF document with margins
        doc = SimpleDocTemplate(output_path, pagesize=A4, 
                                topMargin=top, 
                                leftMargin=left, 
                                rightMargin=right, 
                                bottomMargin=bottom)
        
        # Convert Markdown to paragraphs
        paragraphs = self.markdown_to_paragraphs(text)
        
        # Create a background canvas
        def add_background(canvas, doc):
            canvas.saveState()
            bg_image = ImageReader(background_image)
            canvas.drawImage(bg_image, 0, 0, width=A4[0], height=A4[1])
            canvas.restoreState()
        
        
        # Build PDF
        doc.build(paragraphs, onFirstPage=add_background, onLaterPages=add_background)
    
        return f"PDF '{output_path}' criado com sucesso!"
        
        