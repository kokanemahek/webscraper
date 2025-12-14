from bs4 import BeautifulSoup,Comment
import re

file_path = 'p7.html'

try:
    file = open(file_path, 'r', encoding='utf-8')
    html_content = file.read()
    file.close() 
    print("File content successfully read and stored in 'html_content' variable.")
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

section_pattern = re.compile(r'^\d+\.\d+|^\d+')
part_pattern = re.compile(r'^PART\s[IVX]+')
division_pattern = re.compile(r'^DIVISION\s\d+\w*')
para_pattern = re.compile(r'^\(\d+w*\)')    
    
soup = BeautifulSoup(html_content,'lxml')

for tag in soup.select('head , body > span , body > nav , body > header , div.legisHeader , div.FCSelector , section.intro , div.ScheduleRP , div.ScheduleNIF , section.pagedetails , iframe , footer#wb-info , script , span#wb-rsz , body > main > div > section , p.MarginalNote > span.wb-invisible '):
    tag.decompose()
    
comments = soup.find_all(string=lambda text : isinstance(text,Comment))

for comment in comments:
    comment.decompose()

for tag in soup.select('div , a , ul , li , section , dl , dt , header , dd , dfn'):
    tag.unwrap()

part_level = 1
subheading_level = 2
section_level = 3

current_scope = None   # "part" | "subheading"

for tag in soup.find_all(['p','h1','h2','h3','h4','h5','h6']):

    classes = tag.get("class", [])

    # PART
    if "Part" in classes:
        tag.name = "h1"
        tag['content_type'] = "part"
        current_scope = "part"

    # Subheading (ALL siblings → SAME LEVEL)
    elif "Subheading" in classes:
        tag.name = "h2"
        if re.search(division_pattern,tag.text.strip()):
            tag['content_type'] = "division"
        else:
            tag['content_type'] = "heading"
        current_scope = "subheading"

    # MarginalNote (sections inside subheading)
    elif "MarginalNote" in classes:
        if current_scope == "subheading":
            tag.name = "h3"
        else:
            tag.name = "h2"

        tag['content_type'] = "section"
    elif "scheduleLabel" in classes:
        tag['content_type'] = "schedule"

    # deeper content (optional)
    elif tag.name == "p":
        continue

for p in soup.select('h2,h3,h4,h5,h6'):
    next_p = p.find_next_sibling('p')
    if next_p and any(c in next_p.get("class", []) for c in ["Section", "Subsection"]):
        match = re.search(section_pattern, next_p.text.strip())
        if match:
            section = match.group()
            p.string = section + "  " + p.get_text(strip=True)
            p['data-num'] = section
            next_p.string = re.sub(section_pattern, '', next_p.text.strip())


for p in soup.select('p'):
    prev_tag = p.find_previous_sibling()

    if (
        prev_tag
        and prev_tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        and 'MarginalNote' in prev_tag.get('class', [])
    ):
        match = re.search(para_pattern, p.text.strip())
        if match:
            para = match.group()

            # Remove para number from p text
            p.string = re.sub(para_pattern, '', p.text.strip())

            # Get next heading level safely (max h6)
            prev_level = int(prev_tag.name[1])
            new_level = min(prev_level + 1, 6)

            # Create new heading
            new_tag = soup.new_tag(f'h{new_level}' , content_type = "paragraph" , **{"data-num":para})
            new_tag.string = para

            # Insert before <p>
            p.insert_before(new_tag)



""" for p in soup.select('h2,h3, h4, h5, h6'):
    next_p = p.find_next_sibling('p')
    if next_p and "Section" or "Subsection" in next_p.get("class", []):
        match = re.search(section_pattern, next_p.text.strip())
        if match:
            section = match.group()
            p.string = section + "  " + p.get_text(strip=True)
            p['data-num'] = section
            next_p.string = re.sub(section_pattern, '', next_p.text.strip()) """




with open('p6.html','w+',encoding='utf-8') as f:
    f.write(str(soup.prettify())) 