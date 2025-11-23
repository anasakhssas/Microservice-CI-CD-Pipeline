"""
Convert Markdown documentation to PDF
"""
import markdown_pdf

def convert_to_pdf():
    input_file = "PROJECT_DOCUMENTATION.md"
    output_file = "Microservice_CI_CD_Pipeline_Documentation.pdf"
    
    print(f"Converting {input_file} to PDF...")
    
    # Create PDF converter
    pdf = markdown_pdf.MarkdownPdf()
    
    # Convert markdown to PDF
    pdf.add_section(markdown_pdf.Section(input_file))
    pdf.save(output_file)
    
    print(f"✓ PDF created successfully: {output_file}")

if __name__ == "__main__":
    convert_to_pdf()
