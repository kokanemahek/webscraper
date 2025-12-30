from bs4 import BeautifulSoup,Comment
import re
import time
from selenium import webdriver
 
"""   
driver = webdriver.Chrome()

 try:
    driver.get("https://laws-lois.justice.gc.ca/eng/acts/b-1.01/FullText.html")
    time.sleep(20)
    html_content = driver.page_source
    print("Successfully captured the page source.")
finally:
    driver.quit()"""
 
        
section_pattern = re.compile(r'^\d+\w*\.\d+\w*|^\d+\w*')
part_pattern = re.compile(r'^PART\s[IVX\.\d]+')
division_pattern = re.compile(r'^DIVISION\s\d+\w*\s')
para_pattern = re.compile(r'^\(\d+w*\)') 
heading_pattern = re.compile(r'^h\d+') 

def cleaning_before_soup(content:str):    
    content = content.replace('\n','')
    content = content.replace('\r','')
    content = content.replace('\t','') 
    return [str(content)]

def making_cleaning_soup(content:str):    
    soup = BeautifulSoup(content,'lxml')

    for tag in soup.select('head , body > span , body > nav , body > header , div.legisHeader , div.FCSelector , section.intro , div.ScheduleRP , div.ScheduleNIF , section.pagedetails , iframe , footer#wb-info , script , span#wb-rsz , body > main > div > section , p.MarginalNote > span.wb-invisible , dt , header.modal-header , div.modal-body'):
        tag.decompose()
        
    comments = soup.find_all(string=lambda text : isinstance(text,Comment))

    for comment in comments:
        comment.decompose()

    for tag in soup.select('div , ul.ProvisionList , li , section , header , a , dl , dd , dfn , p.Definition > span , p.Definition > cite , main '):
        tag.unwrap() 
        
    for tag in soup.select('ul.HistoricalNote , cite.XRefExternalAct'):
        tag.name = 'p'

    preamble_tag =  soup.select_one('h6#preamble')
    preamble_tag.name = "h1"
    return [str(soup)]  
       
def make_level(content:str):
    soup = BeautifulSoup(content,'lxml')       
    for tag in soup.select('span'):
        classes = tag.get("class", [])
        if "HTitleText1" in classes:
            tag.parent.name = "h1"
            tag.parent.attrs['content_type'] = "part"
        elif "HTitleText2" in classes:
            tag.parent.name = "h2"
            tag.parent.attrs['content_type'] = "heading" 
        elif "HTitleText3" in classes:
            tag.parent.name = "h3"
            tag.parent.attrs["content_type"] = "subheading" 
        elif "HTitleText4" in classes:
            tag.parent.name = "h4"   
            tag.parent.attrs["content_type"] = "subsubheading"
        elif "scheduleLabel" in classes:
            tag.parent.attrs['content_type'] = "schedule" 
   
    for tag in soup.select('h1,h2,h3,h4,h5,h6'):
        if re.search(division_pattern,tag.text.strip()):
                tag.attrs['content_type'] = "division"

    for p in soup.select('p,h2,h3,h4,h5,h6'):
        next_p = p.find_next_sibling('p')
        if "MarginalNote" in p.get("class",[]) and next_p and any(c in next_p.get("class", []) for c in ["Section", "Subsection"]):
            match = re.search(section_pattern, next_p.text.strip())
            if match:
                section = match.group()
                p.string = section + "  " + p.get_text(strip=True)
                p.name = "h5"
                del p["class"]
                p.attrs['content-type'] = "section"
                p.attrs['data-num'] = section
                next_p.string = re.sub(section_pattern, '', next_p.text.strip())

    for p in soup.select('p:not(table p)'):
        match = re.search(para_pattern, p.text.strip())
        if match:
            para = match.group()
            p.string = re.sub(para_pattern, '', p.text.strip())
            new_tag = soup.new_tag('h7', content_type = "paragraph" , **{"data-num":para})
            new_tag.string = para
            p.insert_before(new_tag)
            
    for p in soup.select('p.MarginalNote'):
        p.name = "h6" 
        p.attrs["content-type"] = "subsubsubheading"
            
    for tag in soup.select('h5'):
        sibling = tag.find_next_sibling()
        if sibling and sibling.name == "h7":
            new_tag = soup.new_tag('h6',content_type = "subsubsubheading")
            tag.insert_after(new_tag)
    
    for tag in soup.select('p,span'): 
        if not tag.get_text(strip=True) and not tag.name == "image":
            tag.decompose()
            
    return [str(soup)]

def removing_extra_attr(content:str):
    soup = BeautifulSoup(content,'lxml')       

    attr_array = ['style','align','typeof','vocab']

    body = soup.body
    for tag in body.find_all(True):
        for attr in attr_array:
            if attr in tag.attrs:
                del tag[attr]  
    return [str(soup)]  
