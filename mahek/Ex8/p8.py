from bs4 import BeautifulSoup,Comment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def fetch_data():
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.law.go.kr/LSW/eng/engLsSc.do?menuId=2&section=lawNm&query=%EA%B8%88%EC%9C%B5%ED%9A%8C%EC%82%AC%EC%9D%98+%EC%A7%80%EB%B0%B0%EA%B5%AC%EC%A1%B0%EC%97%90+%EA%B4%80%ED%95%9C+%EB%B2%95%EB%A5%A0&x=0&y=0#liBgcolor0")
        link_text_to_find = "ACT ON CORPORATE GOVERNANCE OF FINANCIAL COMPANIES"
        link_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, link_text_to_find))
        )
        print(f"Found link with text: '{link_text_to_find}'")
        link_element.click()
        print(f"Clicked the '{link_text_to_find}' link.")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gtit"))
        )
        new_page_source = driver.page_source
        new_page_url = driver.current_url
        print(f"Navigated to new URL: {new_page_url}")
        new_page_source = new_page_source.replace('\n','')
        new_page_source = new_page_source.replace('\r','')
        new_page_source = new_page_source.replace('\t','')
        return [str(new_page_source)]
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()  
    
# file_path = "Ex8/p9.html"

# try:
#     with open(file_path,'r',encoding="utf-8") as f:
#         new_page_source = f.read()
#     print("successfully read the page!")
# finally:
#     f.close() 
    
chapter_pattern = re.compile(r'^CHAPTER\s([IVX]+)')
section_pattern = re.compile(r'^SECTION\s(\d+\w*)')
article_pattern = re.compile(r'^Article\s(\d+\w*)')
para_pattern = re.compile(r'^\(\d+\w*\)')


# new_page_source = new_page_source.replace(' ','')

def make_clean_soup(content:str):
    soup = BeautifulSoup(content,'lxml')

    for tag in soup.select('head , script , div#north-top , div#west-panel , div#west-panel-xsplit , div#ext-gen6 , div#listSaveLayer , div#engInfoSaveLayer, div#slideLeft , div.confnla4 , form#search , div#bodyContentTOP , div#bodySideContent > input , div#sideCenter > div.topinfoTxt , div.subtit1 , div.subtit2 , div#sideCenter > h2'):
        tag.decompose() 
        
    comments = soup.find_all(string=lambda text : isinstance(text,Comment))

    for comment in comments:
        comment.decompose()
        
    for tag in soup.select('div , a'):
        tag.unwrap()
    
    return [str(soup)]

def make_level(content:str): 
    soup = BeautifulSoup(content,'lxml')
    
    for tag in soup.select('p'):
        classes = tag.get("class",[])
        if "pty3" in classes:
            tag.name = "h1"
        if re.search(chapter_pattern,tag.text.strip()):
            chapter = re.search(chapter_pattern,tag.text.strip()).group(1)
            tag.name = 'h1'
            tag.attrs['content_type'] = "chapter"
            tag.attrs['data-num'] = chapter
        if re.search(section_pattern,tag.text.strip()):
            section = re.search(section_pattern,tag.text.strip()).group(1)
            tag.name = 'h2'
            tag.attrs['content_type'] = "section"
            tag.attrs['data-num'] = section
        if re.search(article_pattern,tag.text.strip()):
            article = re.search(article_pattern,tag.text.strip()).group(1)
            tag_span = tag.span.extract()
            tag_span.name = "h3"
            tag_span.attrs['content_type'] = "article"
            tag.attrs['data-num'] = article
            tag.insert_before(tag_span)  
        if re.search(para_pattern,tag.text.strip()):
            para = re.search(para_pattern,tag.text.strip()).group()
            tag.string = re.sub(para_pattern,'',tag.text.strip())
            new_tag = soup.new_tag('h4', content_type = "paragraph" , **{"data-num":para})
            new_tag.string = para
            tag.insert_before(new_tag)
            
    for tag in soup.select('p,span'): 
        if not tag.get_text(strip=True) and not tag.name == "image":
            tag.decompose()
    
    return [str(soup)]  
  
def del_extra_attr(content:str):
    soup = BeautifulSoup(content,'lxml')
            
    attr_array = ['style','align']

    body = soup.body
    for tag in body.find_all(True):
        for attr in attr_array:
            if attr in tag.attrs:
                del tag[attr] 
                
    return [str(soup)]

def save_result(content:str):
    soup = BeautifulSoup(content,'lxml')
    
    with open('Ex8/p8.html','w+',encoding='utf-8') as f:
        f.write(str(soup.prettify()))

