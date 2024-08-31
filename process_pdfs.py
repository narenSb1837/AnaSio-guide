def process_pdf(file):
    def extract_text(elements):
        text_content = ""
        count = 0
        for element in elements:
            if "unstructured.documents.elements.Header" in str(type(element)):
                if count > 0:
                    continue
                else:
                    count += 1
                text_content += "\n \n"
            if "unstructured.documents.elements.Title" in str(type(element)):
                text_content += "\n \n"

            text_content += str(element) + "\n"
        return text_content

    filename, _ = file.split(".")
    print(f"Processing - {file}")
    raw_pdf_elements = partition_pdf(
        filename=file,
        strategy="auto",
        extract_images_in_pdf=True,
        extract_image_block_types=["Image", "Table"],
        extract_image_block_to_payload=False,
        extract_image_block_output_dir=f"input_images_vol_{filename[-1]}",
        infer_table_structure=True,
    )
    text_content = extract_text(raw_pdf_elements)
    output_file = filename + ".txt"
    with open(output_file, "w") as f:
        f.write(text_content)
    print(f"Successfully processed - {file}")


if __name__ == "__main__":
    import sys

    # Get filenames from command line arguments
    files = sys.argv[1:]

    # Check if help is requested
    if "-h" in files or "--help" in files:
        print("Usage: python process_pdfs.py [-h] [--help] <pdf_file1> <pdf_file2> ...")
        print("\nProcess one or more PDF files and extract their content.")
        print("\nArguments:")
        print("  -h, --help    Show this help message and exit")
        print("  <pdf_file>    Path to a PDF file to process")
        sys.exit(0)

    # Remove help flags if present
    files = [f for f in files if f not in ("-h", "--help")]

    if not files:
        print("Please provide one or more PDF filenames as arguments.")
        sys.exit(1)

    # if all ok
    from concurrent.futures import ProcessPoolExecutor
    from unstructured.partition.pdf import partition_pdf

    with ProcessPoolExecutor() as executor:
        executor.map(process_pdf, files)
