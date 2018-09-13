import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment


my_url = "https://www.hpshopping.in/laptops-tablets.html?hp_facet_processortype=Intel+Core+i7&p=3"
my_url2 = "https://en.wikipedia.org/wiki/Change_management"
#my_url = "http://bgr.com/2014/10/15/google-android-5-0-lollipop-release/"
html = urllib.request.urlopen(my_url2)
soup = BeautifulSoup(html, "html.parser")
data = soup.findAll(text=True)
#print(data)


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    if element.parent.name in ['p', 'b', 'a', 'ul']:
        return True



def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


#html = urllib.request.urlopen('http://www.nytimes.com/2009/12/21/us/21storm.html').read()
html = urllib.request.urlopen(my_url2).read()
print(text_from_html(html))
