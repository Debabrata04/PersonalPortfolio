import pdfplumber
from pprint import pprint  # For clean debugging

def extract_resume_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]  # Single-page resume
        
        # Method 1: Standard text extraction
        text = page.extract_text()
        print("=== Standard Extraction ===")
        print(text)
        
        # Method 2: Extract text with layout preservation
        text_with_layout = page.extract_text(x_tolerance=2, y_tolerance=2)
        print("\n=== Layout-Aware Extraction ===")
        print(text_with_layout)
        
        # Method 3: Extract from tables (if any)
        tables = page.extract_tables()
        if tables:
            print("\n=== Extracted Tables ===")
            pprint(tables)
        
        # Method 4: Visual debug (what PDFplumber "sees")
        im = page.to_image()
        # im.show()  # Opens an image showing detected elements
        
        return text_with_layout or text  # Return the best result

# Execute
extracted_text = extract_resume_text("resume.pdf")
with open("resume_text.txt", "w", encoding="utf-8") as f:
    f.write(extracted_text)