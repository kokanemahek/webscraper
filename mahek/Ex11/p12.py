from bs4 import BeautifulSoup
import re

def fetch_data():
    with open('Ex11/p12.html','r',encoding="utf-8") as f:
        html_content = f.read()
        
    html_content = html_content.replace('\n','')
    html_content = html_content.replace('\r','')
    html_content = html_content.replace('\t','')

    return [str(html_content)]
    
heading_pattern = re.compile(r'^[IVX]+\.')
title_pattern = re.compile(r'^Title\s[IVX]+')
subheading_pattern = re.compile(r'^[A-Z]\.')
sub_sub_heading_pattern = re.compile(r'^\d+\w*\.')
    
def make_clean_soup(content:str):
    soup = BeautifulSoup(content,'lxml')

    for tag in soup.select('head , figure , aside '):
        tag.decompose()
        
    for tag in soup.find_all('h1',attrs={"role":"title"}):
        next_tag = tag.find_next_sibling()
        if next_tag and next_tag.name == 'table':
            next_tag.decompose()
            tag.decompose()

    return [str(soup)]

def make_level(content:str):
    soup = BeautifulSoup(content,'lxml')
    
    for tag in soup.select('h1:not(table *), h2:not(table *), h3:not(table *), h4:not(table *), h5:not(table *), h6:not(table *)'):
        if re.search(heading_pattern,tag.text.strip()):
            tag.name = 'h1'
            del tag["role"]
            tag.attrs['content_type'] = "heading"
            tag.attrs['data-num'] = re.search(heading_pattern,tag.text.strip()).group()
        elif re.search(title_pattern,tag.text.strip()):
            tag.name = 'h2'
            del tag["role"]
            tag.attrs['content_type'] = "title"
            tag.attrs['data-num'] = re.search(title_pattern,tag.text.strip()).group() 
        elif re.search(subheading_pattern,tag.text.strip()):
            tag.name = 'h3'
            del tag["role"]
            tag.attrs['content_type'] = "subheading"
            tag.attrs['data-num'] = re.search(subheading_pattern,tag.text.strip()).group() 
        elif re.search(sub_sub_heading_pattern,tag.text.strip()):
            if tag.name == "h4" or tag.name == "h3":
                tag.name = "h4"
                tag.attrs['content_type'] = "subsubheading"
                tag.attrs['data-num'] = re.search(sub_sub_heading_pattern,tag.text.strip()).group()
        
    tag_h1 = soup.find('h1',attrs={"content_type":"heading"})
    for tag in tag_h1.find_previous_siblings():
        tag.decompose()

    for tag in soup.select('p > b'):
        if re.search(sub_sub_heading_pattern,tag.text.strip()):
            subsubheading = re.search(sub_sub_heading_pattern,tag.text.strip()).group()
            h_tag = tag.parent
            tag.unwrap()
            h_tag.name = "h4"
            h_tag.attrs['content_type'] = "subsubheading"
            h_tag.attrs['data-num'] = subsubheading 
        
    for tag in soup.select('p:not(table p):not(ul p)'):
        if re.search(sub_sub_heading_pattern,tag.text.strip()):
            para = re.search(sub_sub_heading_pattern,tag.text.strip()).group() 
            new_tag = soup.new_tag('h5', content_type = "paragraph" , **{"data-num":para})
            new_tag.string = para
            tag.string = re.sub(para,'',tag.text.strip())
            tag.insert_before(new_tag)
        if re.search(title_pattern,tag.text.strip()):
            tag.name = 'h2'
            del tag["role"]
            tag.attrs['content_type'] = "title"
            tag.attrs['data-num'] = re.search(title_pattern,tag.text.strip()).group()
            
    return [str(soup)]
    
def remove_extra_content(content:str):
    soup = BeautifulSoup(content,'lxml')
        
    for tag in soup.select('ul,li'):
        tag.unwrap()
    
    return [str(soup)]

    