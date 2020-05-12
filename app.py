from flask import Flask, render_template, request
from firststep import wordPassingTimeInURL
from secondstep import resultsForUrls
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/firststep')
def firststep():
    return render_template('firststep.html')

@app.route("/firststep/", methods=['POST'])
def func():
    url = request.form['url']
    keyword = request.form['keyword']
    result = wordPassingTimeInURL(url, keyword)
    return render_template('firststep.html', message=result)

@app.route('/secondstep')
def secondstep():
    del urls[:]
    return render_template('secondstep.html')

urls =[]
@app.route("/secondstep/", methods=['POST'])
def func2():
    if 'searchBtn' in request.form:
        keywords = request.form['keywords']
        results = resultsForUrls(urls, keywords)
        table = ""
        for i in results:
            table += "<tr>"
            for j in i:
                table += "<td>%s</td>" % (j)
            table += "</tr>"

        del urls[:]
        return render_template('secondstep.html', output = table)
    elif 'addUrlBtn' in request.form:
        url = request.form['url']
        urls.append(url)

    return render_template('secondstep.html')



if __name__ == '__main__':
    app.run(debug=True)
