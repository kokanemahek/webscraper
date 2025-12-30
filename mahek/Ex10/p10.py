from bs4 import BeautifulSoup,Comment
from selenium import webdriver
import time
import re 

def fetch_data():
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.elegislation.gov.hk/hk/cap405")
        time.sleep(10)
        new_page_source = driver.page_source
        print("successfully captured the page source")
        new_page_source = new_page_source.replace('\n','')
        new_page_source = new_page_source.replace('\t','')
        new_page_source = new_page_source.replace('\r','')
        return [str(new_page_source)]
    finally:
        driver.quit()
    

part_pattern = re.compile(r'^Part\s*([IVX]+)')
section_pattern = re.compile(r'^\d+\w*\.') 
para_pattern = re.compile(r'^\(\d+\w*\)') 
schedule_pattern = re.compile(r'^Schedule\s*(\d+\w*)')
heading_pattern = re.compile(r'^h\d+')

def make_clean_soup(content:str):    
    soup = BeautifulSoup(content,'lxml')

    for tag in soup.select('head , script ,  div#Header , div#MESSAGE_ , div#LEG_PREVIEW , div#LegDetailsWrapper , div#Timeline , div#searchWithinCapContainer , div#TopToolBar0 , div#TopToolBar , div#ViewDividerWrapper , div.left-pane , div#ProgressBar , h3.leg-content-header , div.loading-top , div#BottomToolBar , div.portlet-header ,  div.hklm_meta, div.panel , ul.accordion , div#WCAGLogo , img'):
        tag.decompose()
        
    for tag in soup.select('form , input , a , div.hklm_term '):
        tag.unwrap()
        
    comments = soup.find_all(string=lambda text: isinstance(text,Comment))

    for comment in comments:
        comment.decompose() 

def make_level(content:str):
    soup = BeautifulSoup(content,'lxml')
    
    for tag in soup.select('div.hklm_num'):
        find_next = tag.find_next_sibling()
        if "hklm_heading" in find_next.get("class",[]):
            tag.string = tag.text.strip() + " " + find_next.text.strip()
            find_next.decompose()

    for tag in soup.select('div.hklm_num , div.hklm_commencementNote , div.hklm_content , div.hklm_leadIn , div.hklm_def , div.hklm_continued , div.hklm_referenceNote , div.hklm_note , div.hklm_heading , div.hklm_text'):
        if re.search(part_pattern,tag.text.strip()):
            tag.name = 'h1'
            tag.attrs['content_type'] = "part"
            tag.attrs['data-num'] = re.search(part_pattern,tag.text.strip()).group(1)
        elif re.search(section_pattern,tag.text.strip()):
            tag.name = 'h2'
            tag.attrs['content_type'] = "section"
            tag.attrs['data-num'] = re.search(section_pattern,tag.text.strip()).group()
        elif re.search(para_pattern,tag.text.strip()):
            tag.name = "h3"
            tag.attrs['content_type'] = "paragraph"
            tag.attrs['data-num'] = re.search(para_pattern,tag.text.strip()).group()
        elif re.search(schedule_pattern,tag.text.strip()):
            tag.name = "h1"
            tag.attrs['content_type'] = "schedule"
            tag.attrs['data-num'] = re.search(schedule_pattern,tag.text.strip()).group(1)
        else:
            tag.name = 'p' 
    
    for tag in soup.select('div.hklm_fillIn , div.hklm_sourceNote'):
        tag.name = 'span'
        
    for tag in soup.select('div , p.hklm_leadIn'):
        if "hklm_leadIn" in tag.get("class",[]) and "hklm_def" in tag.parent.get("class",[]):
            tag.parent.unwrap()
        if tag.name == "div":
            tag.unwrap()    
            
    for tag in soup.select('p.hklm_num'):
        next_tag = tag.find_next_sibling()
        if "hklm_content" in next_tag.get("class",[]) or "hklm_leadIn" in next_tag.get("class",[]):
            tag.string = tag.text.strip() + " " + next_tag.text.strip()
            next_tag.decompose() 
            
    for tag in soup.select('p.hklm_heading'):
        prev_tag = tag.find_previous_sibling(heading_pattern)
        if prev_tag :
            prev_tag.string = prev_tag.text.strip() + " " + tag.text.strip()
            tag.decompose()
            
    for tag_table in soup.find_all('table',attrs={"data-domidx":["26","104","122"]}):
        tag_table.colgroup.decompose()
        for tag in tag_table.select('tr , tbody'):
            tag.unwrap()   
        for tag in tag_table.select('td'):
            tag.name = 'p'
        tag_table.unwrap()

def del_extra_content(content:str):
    soup = BeautifulSoup(content,'lxml')
    
    body = soup.body
    attr_array = ['style','name','data-domidx','type',"align","align_right"]

    for tag in body.find_all(True):
        for attr in attr_array:
            if attr in tag.attrs:
                del tag[attr]
                
    for tag in soup.select('p,span'): 
        if not tag.get_text(strip=True) and not tag.name == "image":
            tag.decompose()
     
    return [str(soup)]    



