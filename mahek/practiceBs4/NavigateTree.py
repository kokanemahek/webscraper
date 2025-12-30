html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.head.title)
print(soup.body.b)

print(soup.find_all('a'))

head_tag = soup.head

print(head_tag.contents)

title_tag = head_tag.contents[0]

print(title_tag.contents)

# for child in title_tag.children:
#     print(child)
    
for child in head_tag.descendants:
    print(child)

print(len(list(head_tag.children)))
print(len(list(head_tag.descendants)))

# for string in soup.strings:
#     print(repr(string))

""" for string in soup.stripped_strings:
    print(repr(string))
    
print(title_tag.parent)
print(head_tag.parent)

html_tag = soup.html
print(type(html_tag.parent)) 

link = soup.a
link
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
for parent in link.parents:
    if parent is None:
        print(parent)
    else:
        print(parent.name)"""
        
sibling_soup = BeautifulSoup("<a><b>text1</b><c>text2</c></b></a>",'html.parser')
print(sibling_soup.prettify())

print(sibling_soup.b.next_sibling)
print(sibling_soup.c.previous_sibling)

print(sibling_soup.b.next_element)
print(sibling_soup.c.previous_element)







