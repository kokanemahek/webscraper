from bs4 import BeautifulSoup,NavigableString
import re

para_pattern = re.compile(r'^\d+\w*[\s\w*]+\§')
chapter_pattern = re.compile(r'^(\d+\w*)\skap\.') 
    
def make_soup(content:str):
    content = content.replace('\n','')
    content = content.replace('\r','')
    content = content.replace('\t','')
    content = content.replace('<br/>','<p>')
    content = content.replace('</p>','</p><p>')
    content = content.replace('</h3>1987:672', '</h3><p>1987:672')
    
    soup = BeautifulSoup(content ,'lxml')

    for tag in soup.select('style , head , div#top , header , nav , footer , script, main > div > hgroup , div > section'):
        tag.decompose()
        
    for tag in soup.select('div , main , i , b , a'):
        tag.unwrap()
            
    h_tag = soup.find('h3',attrs={"name":"K1"})
    
    for tag in h_tag.find_previous_siblings():
        tag.decompose()
        
    return [str(soup)]

def make_level(content:str):
    soup = BeautifulSoup(content ,'lxml')
        
    tag_h = soup.find('h3',attrs={"name":"overgang"})
    tag_h.name = "h1"    
        
    for tag in soup.select('h3'):
        if re.search(chapter_pattern,tag.text.strip()):
            chapter = re.search(chapter_pattern,tag.text.strip()).group(1) 
            tag.name = "h1"
            tag.attrs['content_type'] = "chapter"
            tag.attrs['data-num'] = chapter
        
    for tag in soup.select('p:not(table p)'):
        if re.search(para_pattern,tag.text.strip()):
            para = re.search(para_pattern,tag.text.strip()).group()
            new_tag = soup.new_tag('h3', content_type = "paragraph" , **{"data-num":para} )
            new_tag.string = re.search(para_pattern,tag.text.strip()).group() 
            tag.string = re.sub(para_pattern,'',tag.text.strip()) 
            tag.insert_before(new_tag)
            
    for tag in soup.select('h4'):
        tag.name = "h2"
        tag.attrs['content_type'] = "heading"
    
    return [str(soup)]
        
def remove_extra_content(content:str): 
    soup = BeautifulSoup(content ,'lxml')
           
    for tag in soup.select('p,span'): 
        if not tag.get_text(strip=True) and not tag.name == "image":
            tag.decompose()
        
    body = soup.body

    for content in list(body.contents): 
        if isinstance(content, NavigableString) and content.strip():
            content.decompose() 
    
    return [str(soup)] 

def del_extra_attr(content:str):
    soup = BeautifulSoup(content ,'lxml')
            
    attr_array = ['style','align']

    body = soup.body
    for tag in body.find_all(True):
        for attr in attr_array:
            if attr in tag.attrs:
                del tag[attr] 
    return [str(soup)]

        