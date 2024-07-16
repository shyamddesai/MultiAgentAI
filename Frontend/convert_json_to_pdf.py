import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def create_articles_pdf(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    custom_styles = {
        'title': ParagraphStyle('title', parent=styles['Title'], fontSize=18, textColor='blue'),
        'source': ParagraphStyle('source', parent=styles['Normal'], fontSize=12, textColor='green'),
        'date': ParagraphStyle('date', parent=styles['Normal'], fontSize=10, textColor='gray'),
        'content': ParagraphStyle('content', parent=styles['Normal'], fontSize=12),
        'default': styles['Normal']
    }
    story = []

    for item in data:
        story.append(Paragraph(item['Title'], custom_styles['title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Source: {item['Source']}", custom_styles['source']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Published: {item['Date']}", custom_styles['date']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(item['Content'], custom_styles['content']))
        story.append(PageBreak())

    doc.build(story)

def create_sources_pdf(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    custom_styles = {
        'source': ParagraphStyle('source', parent=styles['Title'], fontSize=14, textColor='blue'),
        'address': ParagraphStyle('address', parent=styles['Normal'], fontSize=12, textColor='green'),
        'default': styles['Normal']
    }
    story = []

    for item in data:
        story.append(Paragraph(item['Source'], custom_styles['source']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(item['Address'], custom_styles['address']))
        story.append(Spacer(1, 24))

    doc.build(story)

def main():
    # Load JSON data for articles
    articles_json_filename = '1.json'
    articles_data = load_json(articles_json_filename)

    # Load JSON data for sources
    sources_json_filename = '2.json'
    sources_data = load_json(sources_json_filename)

    # Create Articles PDF
    articles_pdf_filename = '1.pdf'
    create_articles_pdf(articles_data, articles_pdf_filename)
    print(f"Created PDF: {articles_pdf_filename}")

    # Create Sources PDF
    sources_pdf_filename = '2.pdf'
    create_sources_pdf(sources_data, sources_pdf_filename)
    print(f"Created PDF: {sources_pdf_filename}")

if __name__ == '__main__':
    main()