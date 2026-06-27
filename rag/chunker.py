"""
chunker.py

Splits extracted PDF text into overlapping chunks
ready for embedding.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_pdf(pdf_data):
    """
    Split each page into chunks.

    Parameters
    ----------
    pdf_data : dict
        Output from extract_pdf_text()

    Returns
    -------
    list
        List of chunk dictionaries.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = []

    chunk_id = 0

    for page in pdf_data["pages"]:

        page_number = page["page"]

        page_text = page["text"]

        page_chunks = splitter.split_text(page_text)

        for text in page_chunks:

            chunk = {

                "chunk_id": chunk_id,

                "page": page_number,

                "text": text,

                "source": pdf_data["filename"]

            }

            chunks.append(chunk)

            chunk_id += 1

    return chunks