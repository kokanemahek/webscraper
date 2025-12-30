from bs4 import BeautifulSoup

html = '<b id="b1" class="boldest">Extremely bold</b>'
soup = BeautifulSoup(html, features="lxml")

tag = soup.b

print(tag.attrs)

tag['id'] = "bold1"
tag['another-attribute'] = "1"

print(tag)

del tag['id']
del tag['another-attribute']

print(tag)


rel_soup = BeautifulSoup('<p>Back to the <a rel="index">homepage</a></p>', features="lxml")
rel_soup.a['rel']
# ['index']
rel_soup.a['rel'] = ['index', 'contents']
print(rel_soup.p)
# <p>Back to the <a rel="index contents">homepage</a></p>

#navigableString
print(rel_soup.a.string)

rel_soup.a.string.replace_with("AboutPage")

print(rel_soup.a.string)




