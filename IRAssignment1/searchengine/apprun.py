from flask import Flask, render_template, request, redirect, escape
from searchengine import querysearch
app = Flask(__name__)


@app.route('/')
def entrypage()->'html':
    return render_template('search.html', the_title="Enter the query below to search")


def get_title(url):
    pagetitle = url.split('/')
    title = 'Wikipedia - '+pagetitle[len(pagetitle) - 1]
    title = title.replace('_', ' ')
    return title

@app.route('/search', methods=['POST'])
def do_search() -> 'html':
    title = "Here are the top results for the query : "
    query = request.form['query']

    url_list = querysearch.search(query)
    title_list = []
    for link in url_list:
        title_list.append(get_title(link))

    #print(url_list)
    title = title+query
    #log_request(request, result)
    return render_template('results.html', the_title=title, links=url_list, the_query=query, titles=title_list)


app.run(port=8080, debug=True)


