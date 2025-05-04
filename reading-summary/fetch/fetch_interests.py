import markdown
from bs4 import BeautifulSoup

def extract_section_from_markdown(md_file, heading_text, heading_level=2):
    # Convert Markdown to HTML
    with open(md_file) as f:
        md_text = f.read()
        
    html = markdown.markdown(md_text)

    # Parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # Find the heading
    heading_tag = f"h{heading_level}"
    target = soup.find(heading_tag, string=heading_text)
    if not target:
        return None

    # Collect content until the next heading of the same or higher level
    result = []
    for sibling in target.find_next_siblings():
        if sibling.name and sibling.name.startswith("h"):
            sibling_level = int(sibling.name[1])
            if sibling_level <= heading_level:
                break
        result.append(sibling.get_text())

    return "\n\n".join(result).strip() 