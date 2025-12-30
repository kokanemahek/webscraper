from bs4 import BeautifulSoup
import re

section_pattern = re.compile(r'^\d+\w*[\s\w*]+\§')
chapter_pattern = re.compile(r'^(\d+\w*)\skap\.') 

def fetch_data():
    with open('Ex9/p10.html','r',encoding="utf-8") as f:
        html_content = f.read()
    
    html_content = html_content.replace('\n','')
    html_content = html_content.replace('\r','')
    html_content = html_content.replace('\t','')
    
    return [str(html_content)]
    
def make_clean_soup(content:str):
    soup = BeautifulSoup(content,'lxml')

    for tag in soup.select('aside , figure '):
        tag.decompose() 
        
    for tag in soup.select('i , b '):
        tag.unwrap()
    
    return [str(soup)]

def make_level(content:str):
    soup = BeautifulSoup(content,'lxml')
    
    for tag in soup.select('h2'):
        if re.search(chapter_pattern,tag.text.strip()):
            del tag["role"]
            chapter = re.search(chapter_pattern,tag.text.strip()).group(1)
            tag.name = "h1"
            tag.attrs['content_type'] = "chapter"
            tag.attrs['data-num'] = chapter 
            
    for tag in soup.select('p'):
        if re.search(section_pattern,tag.text.strip()):
            para = re.search(section_pattern,tag.text.strip()).group()
            new_tag = soup.new_tag('h3' , content_type = "section" , **{"data-num":para})    
            new_tag.string =  re.search(section_pattern,tag.text.strip()).group()
            tag.string = re.sub(section_pattern,'',tag.text.strip()) 
            tag.insert_before(new_tag)
            
    for tag in soup.find_all(attrs={"role":"sectionHeading"}):
        tag.name = 'h2'
        tag.attrs['content-type'] = "heading"
        
    for tag in soup.find_all(attrs={"role":"pageHeader"}):
        tag.decompose()
        
    tag_h = soup.find('h1',attrs={"data-num":"1"})
    for tag in tag_h.find_previous_siblings():
        tag.decompose()
        
    return [str(soup)]
  