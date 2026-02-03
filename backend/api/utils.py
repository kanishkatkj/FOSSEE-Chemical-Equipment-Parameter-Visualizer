from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse

def generate_pdf(dataset, equipment_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, f"Analysis Report: {dataset.file.name}")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 80, f"Uploaded At: {dataset.uploaded_at}")
    
    # Summary
    y = height - 120
    p.drawString(100, y, f"Total Equipment Count: {equipment_data.count()}")
    y -= 20
    
    # Simple table-like listing
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, "Equipment Name")
    p.drawString(300, y, "Type")
    p.drawString(450, y, "Flowrate")
    
    p.setFont("Helvetica", 10)
    y -= 20
    for item in equipment_data[:20]: # Limit to 20 for one page demo
        if y < 50:
             p.showPage()
             y = height - 50
        p.drawString(100, y, str(item.equipment_name))
        p.drawString(300, y, str(item.equipment_type))
        p.drawString(450, y, str(item.flowrate))
        y -= 15
        
    p.save()
    buffer.seek(0)
    return buffer
