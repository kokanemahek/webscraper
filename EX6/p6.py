from bs4 import BeautifulSoup,Comment
from selenium import webdriver
import re
import time
import requests

"""
url = "https://laws-lois.justice.gc.ca/eng/acts/b-1.01/FullText.html"

response = requests.get(url)

if response.status_code == 200:
    print("Successfully fetched the data!")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    
""" 
"""
driver = webdriver.Chrome()

 try:
    driver.get("https://laws-lois.justice.gc.ca/eng/acts/b-1.01/FullText.html")
    time.sleep(20)
    page_source_variable = driver.page_source
    print("Successfully captured the page source.")
finally:
    driver.quit()


with open('Ex6/p7.html','w+',encoding='utf-8') as f:
    f.write(page_source_variable) """ 


file_path = 'Ex6/p7.html'

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
    
soup = BeautifulSoup(html_content,'lxml')

for tag in soup.select('head , body > span , body > nav , body > header , div.legisHeader , div.FCSelector , section.intro , div.ScheduleRP , div.ScheduleNIF , section.pagedetails , iframe , footer#wb-info , script , span#wb-rsz , body > main > div > section , p.MarginalNote > span.wb-invisible '):
    tag.decompose()
    
comments = soup.find_all(string=lambda text : isinstance(text,Comment))

for comment in comments:
    comment.decompose() 
"""     
for tag in soup.select_one('p.Section'):
    print(tag) """
    
for tag in soup.select('h6#preamble'):
    tag.name = 'h1'
    
for p in soup.select('p.MarginalNote'):
    next_p = p.find_next()
    if next_p and "Section" in next_p.get("class",[]):
        if re.search(section_pattern,next_p.text.strip()):
            section = re.search(section_pattern,next_p.text.strip()).group()
            p.string = section + "  " + p.get_text(strip=True)
            p.name = 'h3'
            p['content_type'] = "section"
            p['data-num'] = section
            next_p.string = re.sub(section_pattern,'',next_p.text.strip())
     
       
for tag in soup.select('h2.Part'):
    if re.search(part_pattern,tag.text.strip()):
        part = re.search(part_pattern,tag.text.strip()).group()
        tag.name = 'h1'
        tag['content_type'] = "part"
        tag['data-num'] = part 
        
for tag in soup.select('h3.Subheading , h4.Subheading'):
    tag.name = 'h2'
    tag['content_type'] = "heading"
    
for tag in soup.select('span'):
    if "HTitleText1" in tag.get("class",[]):
        tag.parent.name = "h1"
    elif "HTitleText2" in tag.get("class",[]):
        tag.parent.name = "h2"
    elif "HTitleText3" in tag.get("class",[]):
        tag.parent.name = "h3"
    elif "HTitleText4" in tag.get("class",[]):
        tag.parent.name = "h4"       
    
""" for tag in soup.select('h2.Subheading'):
    sibling = tag.find_next_sibling()
    if sibling and "Subheading" in sibling.get("class",[]):
        sibling.name = 'h3'
        next_h = sibling.find_next()
        next_h.name = 'h4'  """ 
        
"""  if prev_p and "MarginalNote" in prev_p.get("class",[]):
        if re.search(section_pattern,p.text.strip()):
            section = re.search(section_pattern,p.text.strip()).group()
            print(section)
            prev_p.string = p.get_text(strip=True) + " " + section  """

with open('Ex6/p6.html','w+',encoding='utf-8') as f:
    f.write(str(soup.prettify()))     
