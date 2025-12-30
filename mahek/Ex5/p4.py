from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time

def fetch_data():
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.retsinformation.dk/eli/lta/2021/686")
        time.sleep(10)
        page_source_variable = driver.page_source
        print("Successfully captured the page source.")
        return [str(page_source_variable)]
    finally:
        driver.quit()
    
section_pattern = re.compile(r'^\§\s[\d\w\s]+\.')
heading_pattern = re.compile(r'^h\d+')

def make_new_soup(content:str):
    soup = BeautifulSoup(content,'lxml')

    div_tag = soup.select_one('div#restylingRoot')

    soup2 = BeautifulSoup('<html><body>','lxml')

    soup2.body.append(div_tag)
    return [str(soup2)] 

def cleaning_data(content:str):
    soup2 = BeautifulSoup(content,'lxml') 
    for tag in soup2.select('p.Titel2 , div.bjelke , p.Fodnote , hr.IKraftStreg , a.FodnoteHenvisning'):
        tag.decompose()
        
    for tag in soup2.select('div,span'):
        tag.unwrap()
    return [str(soup2)] 

def processing_new_tag(soup2,name,text,content_type,data_num=None,):
    new_tag = soup2.new_tag(name)
    if content_type:
        new_tag['content_type'] = content_type
    if (data_num != None):
        new_tag['data-num'] = data_num
    new_tag.string = text
    return new_tag
 
def make_level(content:str):
    soup2 = BeautifulSoup(content,'lxml')    
    for tag in soup2.select('p.ParagrafGruppeOverskrift'):
        tag.name = 'h1'
        tag['content_type'] = "heading"
        
    for tag in soup2.select('p:not(table p)'):
        if "Paragraf" in tag.get("class", []):
            if re.search(section_pattern,tag.text.strip()):
                section = re.search(section_pattern,tag.text.strip()).group()
                tag.string = re.sub(section_pattern,'',tag.text.strip())
                tag["content_type"] = "paragraph"
                new_tag = processing_new_tag(soup2,name='h2',text=section,content_type="section",data_num=section)
                tag.insert_before(new_tag) 
        elif "IkraftTekst" in tag.get("class", []):
            tag_text = tag.get_text()
            new_text = tag_text.split('indeholder')[0]
            new_tag = processing_new_tag(soup2,name='h1',text=new_text,content_type="heading")
            tag.insert_before(new_tag)
        elif "CentreretParagraf" in tag.get("class", []):
            tag.name = 'h2'
            tag['content_type'] = "section"
            tag['data-num'] = tag.string
    
    for tag in soup2.select_one('p:not(table p)'):
        if not tag.find_previous_sibling():
            new_tag = processing_new_tag(soup2,name='h1',text="[Leading text]",content_type="intro")
            tag.parent.insert_before(new_tag) 

    for heading_tag in soup2.select('h1:not(table h1)'):     
        sibling = heading_tag.find_next_sibling(heading_pattern)
        if heading_tag.find_next().name == 'p' and sibling:
            if heading_tag.name[1] < sibling.name[1]: 
                new_tag = processing_new_tag(soup2,name='h2',text="[Leading text]",content_type="intro")
                heading_tag.insert_after(new_tag)  
    return [str(soup2)]

def remove_attr(content:str):
    soup2 = BeautifulSoup(content,'lxml')      
    attr_array = ['style','align']

    body = soup2.body
    for tag in body.find_all(True):
        for attr in attr_array:
            if attr in tag.attrs:
                del tag[attr]  
    return [str(soup2)]           
