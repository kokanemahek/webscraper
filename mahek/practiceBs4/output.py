from bs4 import BeautifulSoup

print(BeautifulSoup("<a><b /></a>", "xml"))

print(BeautifulSoup("<a></p>", "lxml"))

print(BeautifulSoup("<a></p>", "html5lib"))

print(BeautifulSoup("<a></p>", "html5lib"))

markup = "<h1>Sacr\xc3\xa9 bleu!</h1>"
soup = BeautifulSoup(markup,'html.parser')
print(soup.h1)
print(soup.h1.string)

markup = "<p\n>Paragraph 1</p>\n    <p>Paragraph 2</p>"
soup = BeautifulSoup(markup, 'html.parser')
for tag in soup.find_all('p'):
    print(tag.sourceline, tag.sourcepos, tag.string)
    
markup = "<p>I want <b>pizza</b> and more <b>pizza</b>!</p>"
soup = BeautifulSoup(markup, 'html.parser')
first_b, second_b = soup.find_all('b')
print (first_b == second_b)

print (first_b.previous_element == second_b.previous_element)

import copy
p_copy = copy.copy(soup.p)
print (p_copy)


from bs4 import SoupStrainer

only_a_tags = SoupStrainer("a")
print(only_a_tags)

only_tags_with_id_link2 = SoupStrainer(id="link2")
print(only_tags_with_id_link2)

def is_short_string(string):
    return len(string) < 10

only_short_strings = SoupStrainer(string=is_short_string)
print(only_short_strings)