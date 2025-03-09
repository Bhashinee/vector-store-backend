from pypdf import PdfReader

# Simple Implementation
def parse_content(file):
    reader = PdfReader(file)
    content = ""
    for page in reader.pages:
        content += page.extract_text()

    return content

    