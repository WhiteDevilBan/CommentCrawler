from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html)
#格式化
# print(soup.prettify())

# print(soup.a)
# print(soup.a.name)
# print(soup.a.attrs)
#
# print(soup.title.string)
#
# print(type(soup.title))

#打印子节点
# print(soup.html.contents)
#
# print(soup.head.children)
# for child in soup.html.children:
#     print(child)

# for child in soup.body.descendants:
#     print(child)
#
# for string in soup.stripped_strings:
#     print(repr(string))

# print(soup.p.next_sibling.next_sibling)


# for sibling in soup.p.next_siblings:
#     print(sibling)
print(soup.a.next_element.next_element.next_element.next_element)
