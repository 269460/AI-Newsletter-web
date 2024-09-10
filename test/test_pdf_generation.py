from mining_summary.spiders.generatePDF import PDF

def test_pdf_generation():
    pdf_generator = PDF()
    pdf_generator.generate_pdfs(["AI", "IoT"])
    print("PDF generation completed. Check the output directory for the generated files.")

if __name__ == "__main__":
    test_pdf_generation()