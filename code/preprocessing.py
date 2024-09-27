import re
import os
from langchain_core.documents import Document

def clean_text(text):
    """
    Cleans the text by removing redundant page footers, headers, and useless spaces.

    Args:
        text (str): The full text extracted from the PDF.

    Returns:
        str: Cleaned text with headers and footers removed, and spaces adjusted.
    """
    # Define patterns to identify and remove headers and footers
    footer_pattern = re.compile(
        r'\n?\s*page\s+\d+\s*/\s*\d+\s+https?://\S+\n?',
        re.IGNORECASE
    )
    header_pattern = re.compile(
        r'\n?ACTE UNIFORME RELATIF.*\nAdopté le.*\n\s*Publié au Journal Officiel.*\n?',
        re.IGNORECASE
    )

    # Remove all occurrences of the footer and header patterns
    cleaned_text = footer_pattern.sub('', text)
    cleaned_text = header_pattern.sub('', cleaned_text)

    # Remove excessive blank lines or spaces caused by removal
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)
    return cleaned_text.strip()

def separate_sections(text, return_documents=True):
    """
    Separates the 'Contexte', 'Preambule', and each 'Chapitre' from the given text.

    Args:
        text (str): The full text extracted from the PDF.

    Returns:
        dict: A dictionary with 'Contexte', 'Preambule', and 'Chapitres' as keys.
    """
    sections = {
        'Contexte': '',
        'Preambule': '',
        'Chapitres': {}
    }

    # Clean text to remove headers, footers, and redundant spaces
    text = clean_text(text)

    # Capture Contexte section
    contexte_pattern = re.compile(r'^(.*?)\s*(?=Preambule)', re.DOTALL | re.IGNORECASE)
    contexte_match = contexte_pattern.search(text)
    if contexte_match:
        sections['Contexte'] = contexte_match.group(1).strip()

    # Capture Preambule section
    preambule_pattern = re.compile(r'Preambule\s*(.*?)\s*(?=Chapitre\s+\d+\s*-)', re.DOTALL | re.IGNORECASE)
    preambule_match = preambule_pattern.search(text)
    if preambule_match:
        sections['Preambule'] = preambule_match.group(1).strip()

    # Capture each Chapitre section
    chapitre_pattern = re.compile(r'Chapitre\s+(\d+)\s*-\s*(.*?)\s*(?=Chapitre\s+\d+\s*-|$)', re.DOTALL | re.IGNORECASE)
    chapitres = chapitre_pattern.findall(text)
    for num, title_content in chapitres:
        split_content = title_content.strip().split('\n', 1)
        title = split_content[0].strip()
        content = split_content[1].strip() if len(split_content) > 1 else ''
        sections['Chapitres'][f'Chapitre {num} - {title}'] = split_articles(content)

    if return_documents:
        documents = []
        for section, details in sections.items():
            if not isinstance(details, str) :
                chapters = sections[section]
                for chapter, articles in chapters.items():
                    for article, content in articles.items():
                        sep = "_"
                        if article.count(sep) > 1:
                            _ = article.split(sep)
                            article = sep.join(_[:2])
                            content = sep.join(_[2:]) + content
                        page_content = f'"{chapter}" - {article}: {content}'
                        document = Document(page_content=page_content, metadata={"source": f'"{chapter}": {article}'})
                        documents.append(document)
            
            else:
                page_content = f"{section}: {details}"
                document = Document(page_content=page_content, metadata={"source": section})
                documents.append(document)

        return documents

    return sections

def split_articles(chapitre_content):
    """
    Splits the chapitre content into individual articles based on the "Article" keyword.
    Refined to ensure that multi-paragraph articles are kept as one.

    Args:
        chapitre_content (str): The content of a single chapter.

    Returns:
        dict: A dictionary with article titles as keys and their content as values.
    """
    articles = {}

    # Improved pattern to capture articles more accurately, including multi-paragraph content
    article_pattern = re.compile(
        r'(Article\s+\d+\s*(?:\d+\s*)?\-?\s*)(.*?)(?=\nArticle\s+\d+\s*(?:\d+\s*)?\-?|\Z)',
        re.DOTALL | re.IGNORECASE
    )

    # Find and split articles in the chapter content
    article_matches = article_pattern.findall(chapitre_content)
    for article_title, article_content in article_matches:
        # Clean and format the article title
        article_title = article_title.strip().replace('\n', ' ')
        safe_article_title = re.sub(r'[^\w\-]', '_', article_title)
        articles[safe_article_title] = article_content.strip()

    return articles

def process_file(file_path, output_directory):
    """
    Processes a single text file to extract 'Contexte', 'Preambule', and 'Chapitres' with their 'Articles',
    and saves the extracted sections into separate files.

    Args:
        file_path (str): The path to the text file.
        output_directory (str): The directory where extracted sections will be saved.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    sections = separate_sections(text)
    base_filename = os.path.splitext(os.path.basename(file_path))[0]

    # Save Contexte
    contexte_path = os.path.join(output_directory, f"{base_filename}_Contexte.txt")
    with open(contexte_path, 'w', encoding='utf-8') as f:
        f.write(sections['Contexte'])

    # Save Preambule
    preambule_path = os.path.join(output_directory, f"{base_filename}_Preambule.txt")
    with open(preambule_path, 'w', encoding='utf-8') as f:
        f.write(sections['Preambule'])

    # Save Chapitres and Articles
    chapitres_dir = os.path.join(output_directory, f"{base_filename}_Chapitres")
    os.makedirs(chapitres_dir, exist_ok=True)
    for chapitre_title, articles in sections['Chapitres'].items():
        chapitre_safe_title = re.sub(r'[^\w\-]', '_', chapitre_title)
        chapitre_path = os.path.join(chapitres_dir, chapitre_safe_title)
        os.makedirs(chapitre_path, exist_ok=True)
        for article_title, article_content in articles.items():
            article_filename = re.sub(r'[^\w\-]', '_', article_title) + '.txt'
            article_path = os.path.join(chapitre_path, article_filename)
            with open(article_path, 'w', encoding='utf-8') as f:
                f.write(article_content)

    print(f"Processed and saved sections and articles for {file_path}")

def main():
    # Directory containing your text files
    input_directory = 'path_to_your_input_directory'    # Replace with your input directory path
    output_directory = 'path_to_your_output_directory'  # Replace with your desired output directory path

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over all .txt files in the input directory
    for filename in os.listdir(input_directory):
        if filename.lower().endswith('.txt'):
            file_path = os.path.join(input_directory, filename)
            process_file(file_path, output_directory)

# if __name__ == "__main__":
#     main()
