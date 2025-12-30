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

import re
""" for tag in soup.find_all(re.compile("t")):
    print(tag.name)

for tag in soup.find_all(re.compile("^b")):
    print(tag.name)
    
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')
 
print(soup.find_all(has_class_but_no_id))
print(soup.find_all("p","title"))
print(soup.find_all("p","title",))
print(soup.find_all("a",limit=2))
print(soup.find_all(id="link2")) 

print(soup.find_all(href=re.compile("elsie")))
print(soup.find_all("a",class_="sister"))

soup.find_all(string="Elsie")

soup.find_all(string=["Tillie", "Elsie", "Lacie"])

soup.find_all(string=re.compile("Dormouse"))

def is_the_only_string_within_a_tag(s):
    return (s == s.parent.string)

print(soup.find_all(string=is_the_only_string_within_a_tag)) """

a_string = soup.find(string="Lacie")
print(a_string)

print(a_string.find_parents("a"))

print(a_string.find_parent("p"))

print(a_string.find_parents("p", class_="title"))


print(soup.select("title"))
# [<title>The Dormouse's story</title>]

print(soup.select("p:nth-of-type(3)"))
# [<p class="story">...</p>]

soup.select("head > title")
# [<title>The Dormouse's story</title>]

soup.select("p > a")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie"  id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select("p > a:nth-of-type(2)")
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]

soup.select("p > #link1")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.select("body > a")

soup.select('a[href="http://example.com/elsie"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.select('a[href^="http://example.com/"]')

soup.select('a[href$="tillie"]')
# [<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select('a[href*=".com/el"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]