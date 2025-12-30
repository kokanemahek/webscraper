from selenium import webdriver
from bs4 import BeautifulSoup,Comment 
import re

title_pattern = re.compile(r'^Title\s(\d+\w*)\s')
chapter_pattern = re.compile(r'^Chapter\s(\d+\w*)\s')
section_pattern = re.compile(r'^Section\s(\d+\w*\.\d+\w*)\s')
para_effective_pattern = re.compile(r'^Effective\:')
para_Latest_Legislation_pattern = re.compile(r'^Latest\sLegislation\:')
para_pattern = re.compile(r'^(\([A-Z]+\))')
clause_pattern = re.compile(r'^\(\d+\)')

driver = webdriver.Chrome()

try:
    driver.get("https://law.justia.com/codes/ohio/2021/title-13/chapter-1349/section-1349-61/")
    page_source_variable = driver.page_source
    print("Successfully captured the page source.")
finally:
    driver.quit()
    
content = re.sub('<br>','</h1><h1>',page_source_variable)
soup = BeautifulSoup(content,'lxml')

for tag in soup.select('head > link , header#header , div#pills-wrapper , nav , div#crosslink-pill , div.pills-wrapper , div#primary-sidebar , div.disclaimer ,div.notification-banner , div#footer , script , noscript , iframe , div.pagination-v3 , div.block > div > span , div.block > div > strong , div.citation , style'):
    if tag:
        tag.decompose()

for tag in soup.select('div:not(table div)'):
    tag.unwrap()
        
for tag in soup.select('body,head,html'):
    if tag.attrs:
        del tag.attrs
            
comments = soup.find_all(string=lambda text: isinstance(text, Comment))

for comment in comments:
    comment.decompose()
    
for tag in soup.select('h1:not(table h1)'):
    if re.search(title_pattern , tag.text.strip()):
        tag['content_type'] = "title"
        tag['data-num'] = re.search(title_pattern , tag.text.strip()).group(1)
    elif re.search(chapter_pattern , tag.text.strip()):
        tag.name = 'h2'
        tag['content_type'] = "chapter"
        tag['data-num'] = re.search(chapter_pattern , tag.text.strip()).group(1)
    elif re.search(section_pattern , tag.text.strip()):
        tag.name = 'h3'
        tag['content_type'] = "section"
        tag['data-num'] = re.search(section_pattern , tag.text.strip()).group(1)
                     
for tag in soup.select('p:not(table p)'):
    if (re.search(para_effective_pattern , tag.text.strip()) or re.search(para_Latest_Legislation_pattern , tag.text.strip())):
        tag.decompose()
    elif re.search(para_pattern,tag.text.strip()):
        para = re.search(para_pattern, tag.text.strip()).group(0)                        
        tag.string = re.sub(para_pattern, '',tag.text.strip())
        new_tag = soup.new_tag('h4', content_type="paragraph", **{"data-num": para})
        new_tag.string = para
        tag.insert_before(new_tag)      
        
for tag in soup.select('p:not(table p)'):
    if re.search(clause_pattern,tag.text.strip()):
        clause = re.search(clause_pattern, tag.text.strip()).group()                        
        new_tag = soup.new_tag('h5',content_type="clause", **{"data-num": clause})
        new_tag.string = clause
        tag.insert_before(new_tag) 
        tag.string = re.sub(clause_pattern, '',tag.text.strip())

for tag in soup.select_one('h1:not(table h1)'):
    if tag.parent.contents:
        tag.parent.decompose() 
            
with open("Ex3/p2.html","w+") as fp:
    fp.write(soup.prettify())    