import requests
from bs4 import BeautifulSoup,Comment
import re

para_pattern = re.compile(r'^\(\w*\)')
subdivison_pattern = re.compile(r'^(Subdivision|Subd)[.\s]+(\d+\.)\s*\w*\.$')
section_pattern = re.compile(r'^\d+\w*\.\d+')
text_without_prefix_pattern = re.compile(r'^\(\w*\)\s*')

          
def cleaning_data(content:str):  
    soup = BeautifulSoup(content, 'lxml')
    for tag in soup.select("div#breadcrumb, div#doc_nav div#resource_box, footer#legFooter, nav, form , h1#leg-title-text , h3 , ul , script , div#resource_box , a.skip-navigation , div.leg-brand-container , div.leg-banner , div#doc_nav , footer#legFooter , div.history , div#legContainerMain > div > div > div > div > p, a.permalink , head > link "):
        tag.decompose()    
    
    for tag in soup.select('div, a'):
        tag.unwrap() 

    for tag in soup.select('p'):
        if (tag.has_attr('class') or tag.has_attr('style')):
            del tag['class']
            del tag['style']
            
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    for comment in comments:
        comment.decompose()
    
    return [str(soup)]
       
def make_level(content:str):
    soup = BeautifulSoup(content, 'lxml')
    for tag in soup.select('p, h2.subd_no, h1.shn'):
        if re.search(para_pattern,tag.text.strip()):
            para = re.search(para_pattern, tag.text.strip()).group(0)                        
            tag.string = re.sub(text_without_prefix_pattern, '',tag.text.strip())
            new_tag = soup.new_tag('h4')
            new_tag.string = para
            new_tag['content-type'] = "paragraph"
            new_tag['data-num'] = para
            tag.insert_before(new_tag)
        elif re.search(section_pattern,tag.text.strip()):
            section = re.search(section_pattern, tag.text.strip()).group(0)  
            tag.name = "h2"
            tag['content-type'] = "section"
            tag['data-num'] = section
        elif re.search(subdivison_pattern,tag.text.strip()):
            tag.name = "h3"
            subdivison = re.search(subdivison_pattern, tag.text.strip()).group(2)
            tag['content-type'] = "subdivision"
            tag['data-num'] = subdivison
    return [str(soup)]    


