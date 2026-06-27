import fitz  # PyMuPDF


def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF file.

    Parameters
    ----------
    pdf_path : str
        Path to the PDF.

    Returns
    -------
    dict
        {
            "filename": ...,
            "num_pages": ...,
            "pages": [
                {
                    "page": 1,
                    "text": "...",
                }
            ]
        }
    """

    document = fitz.open(pdf_path)

    pdf_data = {
        "filename": pdf_path.split("/")[-1],
        "num_pages": len(document),
        "pages": []
    }

    for page_number in range(len(document)):

        page = document.load_page(page_number)

        text = page.get_text("text")

        pdf_data["pages"].append(
            {
                "page": page_number + 1,
                "text": text
            }
        )

    document.close()

    return pdf_data