from bs4 import BeautifulSoup

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup,'html.parser')

tag = soup.a
tag.string = "New link text."
print(tag)

soup = BeautifulSoup("<a>Foo</a>")
soup.a.append("Bar")
print(soup)

soup = BeautifulSoup("<a>Soup</a>")
soup.a.extend(["'s", " ", "on"])
print(soup)

soup = BeautifulSoup("<b></b>")
tag = soup.b
tag.append("Hello")
new_string = " there"
tag.append(new_string)
print(tag)

soup = BeautifulSoup("<b></b>")
original_tag = soup.b
new_tag = soup.new_tag("a", href="http://www.example.com")
original_tag.append(new_tag)
new_tag.string = "Link text."
print(original_tag)

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup,'html.parser')
tag = soup.a

tag.insert(1, "but did not endorse ")
print(tag)

soup = BeautifulSoup("<b>stop</b>")
tag = soup.new_tag("i")
tag.string = "Don't"
soup.b.string.insert_before(tag)
print(soup.b)

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup,'html.parser')
tag = soup.a

tag.clear()
print(tag)

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup,'html.parser')
a_tag = soup.a
i_tag = soup.i.extract()
print(a_tag)
# <a href="http://example.com/">I linked to</a>
print(i_tag)
# <i>example.com</i>
print(i_tag.parent)

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup,'html.parser')
a_tag = soup.a
soup.i.decompose()
print(a_tag)

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup,'html.parser')
a_tag = soup.a
new_tag = soup.new_tag("b")
new_tag.string = "example.net"
a_tag.i.replace_with(new_tag)
print(a_tag)

soup = BeautifulSoup("<p>I wish I was bold.</p>")
soup.p.string.wrap(soup.new_tag("b"))
soup.p.wrap(soup.new_tag("div"))

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup,'html.parser')
a_tag = soup.a
a_tag.i.unwrap()
print(a_tag)