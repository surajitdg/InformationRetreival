from flask import Flask, render_template, request, redirect, escape

app = Flask(__name__)


@app.route('/')
def entrypage()->'html':
    return render_template('search.html', the_title="Enter the query below to search")


@app.route('/search', methods=['POST'])
def do_search() -> 'html':
    title = "Here are your so called results for the query : "
    query = request.form['query']
    title = title+query
    result1 = "Pehla result"
    result2 = "Doosra result"
    result3 = "Aur kitna result chahiye be...isi se khush reh"
    #result = str(search4letters(phrase, letters))
    #log_request(request, result)
    return render_template('results.html', the_title=title, the_query=query, the_result1=result1, the_result2=result2, the_result3=result3)


app.run(port=8080, debug=True)
