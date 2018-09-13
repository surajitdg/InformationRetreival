import wikipedia as wiki
import urllib.request
from bs4 import BeautifulSoup as bs
from configparser import ConfigParser

cfg = ConfigParser()

cfg.read('static/config.ini')
numlinks = cfg.get('others', 'numlinks')
ignore = cfg.get('others', 'ignoresections')


for i in range(1, int(numlinks)+1, 1):
    linkstr = 'link'+str(i)
    docName = 'doc'+str(i)+'.txt'
    url = cfg.get('links', linkstr)
    print(url)

    link = urllib.request.urlopen(url)
    soup = bs(link, 'html.parser')
    pagetitle = url.split('/')
    title = pagetitle[len(pagetitle)-1]
    print('Title = '+title)
    spans = soup.find_all('span', {"class": "mw-headline"})
    section = []
    for span in spans:
        a = span.string
        # a = a.encode("ascii")
        section.append(a)

    print('Printing total sections for link '+str(i))
    print(section)
    #print(wiki.summary(link))


    docText = ''

    wikip = wiki.WikipediaPage(title)

    summary = wikip.summary
    docText = docText + 'Summary \n' + summary
    #print(summary)

    for sec in section:
        if str(sec) not in ignore:
            docText = '\n' + docText + '\n' + str(sec) + '\n'
            secText = wikip.section(section_title=str(sec))
            docText = docText + str(secText)

    print(docText)

    f = open('corpus/'+docName, 'w+')
    f.write(docText)
    f.close()




