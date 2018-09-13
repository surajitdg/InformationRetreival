from flask import Flask, render_template, request, redirect, escape
from searchengine import querysearch
app = Flask(__name__)


@app.route('/')
def entrypage()->'html':
    return render_template('search.html', the_title="Enter the query below to search")


@app.route('/search', methods=['POST'])
def do_search() -> 'html':
    title = "Here are the top 10 results for the query : "
    query = request.form['query']

    url_list = querysearch.search(query)
    print(url_list)
    title = title+query



    #log_request(request, result)
    return render_template('results.html', the_title=title, the_query=query, the_result1=url_list[0], the_result2=url_list[1], the_result3=url_list[2])


app.run(port=8080, debug=True)
