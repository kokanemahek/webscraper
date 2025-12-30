from selenium import webdriver
from bs4 import BeautifulSoup,Comment 
import re
import time

def fetch_data():
    driver = webdriver.Chrome()
    try:
        driver.get("https://eur-lex.europa.eu/eli/reg/2017/2394")
        time.sleep(10)
        page_source_variable = driver.page_source
        print("Successfully captured the page source.")
        return [str(page_source_variable)]
    finally:
        driver.quit()
    
chapter_pattern = re.compile(r'^CHAPTER\s([IVX]+)')
article_pattern = re.compile(r'^Article\s*(\d+\w*)\s*')
para_pattern = re.compile(r'^\d+\w*\.')
para2_pattern = re.compile(r'^\([\d\w]+\)')

def cleaning_data(content:str):
    soup = BeautifulSoup(content ,'lxml')

    for tag in soup.select('script , head > meta , head > link , style.wt-noconflict , div#cookie-consent-banner , div.wt-cck--container , div#globan ,input#piwikProSiteID , input#piwikProSummariesSiteID , div#myModal , header#op-header , div#op-header-pdf , div.NavSearch , div.ecl-container , div#PP2 , div#PP2Contents , div#MainContent > div.PageTitle , nav#AffixSidebar , div#PP1Contents , div#PP3 , div#PP3Contents , div.PP3Contents , div#document1 > div.tabContent > div > table , p.reference , hr.separator , p.disclaimer ,  div#document1 > div.tabContent > div > p , div#document1 > div.tabContent > div > hr , div#PP4 , div.eli-container > p , div.eli-container > div#tit_1 , div.Wrapper > a[href="#MainContent"] , a[class~=linkToTop] , button#tocBtnMbl , button#tocHideBtnMbl , aside#TOC-off-canvas , canvas , footer , div.modificationTablePanel , div#enc_1 > p , p.modref , p > i'):
        tag.decompose()
    
    comments = soup.find_all(string=lambda text: isinstance(text,Comment))

    for comment in comments:
        comment.decompose() 

    for tag in soup.select('div.norm'):
        for child in tag.children:
            if child.name == "div":
                child.name = 'p'          

    for tag in soup.select('div , a , span.boldface'):
        tag.unwrap()
        
    return [str(soup)] 
  
def process_heading(p1, next_p , new_tag , content_type , pattern=None):
    p1.string = p1.get_text(strip=True) + "  " + next_p.get_text(strip=True)
    next_p.decompose()
    p1.name = new_tag
    p1["content_type"] = content_type
    if pattern:
        match = re.search(pattern , p1.text.strip())
        if match:
            p1["data-num"] = match.group(2)

def make_level(content:str):
    soup = BeautifulSoup(content ,'lxml') 
       
    for p1 in soup.select("p:not(table p)"):
        next_p = p1.find_next_sibling()
        if next_p and next_p.name == "p":
            if "title-division-2" in next_p.get("class", []):
                process_heading(p1 , next_p ,new_tag="h1" , content_type="chapter", pattern=chapter_pattern)
            elif "stitle-article-norm" in next_p.get("class", []):
                process_heading(p1 , next_p ,new_tag="h2" , content_type="article" , pattern=article_pattern)
            elif "title-annex-1" in p1.get("class", []):
                process_heading(p1 , next_p , new_tag="h1" , content_type="annex" , pattern=None)
            
    for tag_span in soup.select('span'):
        next_p = tag_span.find_next_sibling()
        if re.search(para2_pattern,tag_span.text.strip()):
            next_p.string = tag_span.get_text(strip=True) + " " + next_p.get_text(strip=True)
            tag_span.decompose()
                        
    for tag in soup.select('span'):
        if "superscript" in tag.get("class", []):
            tag.name = 'sup'
        elif "italics" in tag.get("class",[]):
            tag.name = 'i'
        elif re.search(para_pattern,tag.text.strip()):
            tag.name = 'h3'
            tag['content_type'] = "paragraph"
            tag['data-num'] = re.search(para_pattern,tag.text.strip()).group() 
            
    for p_tag in soup.select('p:not(table p)'):
        if p_tag.parent.name == 'p':
            p_tag.parent.unwrap()
        if p_tag.select('span[style]'):
            tag_span = p_tag.select('span[style]')
            for tag in tag_span:
                tag.decompose()
        if p_tag.select('br'):
            p_tag.decompose()  
        if re.search(para_pattern,p_tag.text.strip()):
            para = re.search(para_pattern, p_tag.text.strip()).group(0)                        
            p_tag.string = re.sub(para_pattern, '',p_tag.text.strip())
            new_tag = soup.new_tag('h2',content_type = "annex-paragraph" , **{"data-num" : para})
            new_tag.string = para
            p_tag.insert_before(new_tag)
    return [str(soup)]  

def attr_cleaning(content:str):
    soup = BeautifulSoup(content ,'lxml')      
    body = soup.body
    attr_array = ['id','style']
        
    for tag in body.find_all(True):
        for attr in attr_array:
            if attr in tag.attrs:
                del tag[attr]
    
    return [str(soup)]
