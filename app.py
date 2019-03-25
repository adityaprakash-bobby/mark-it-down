from flask import Flask, render_template, request
from flaskext.markdown import Markdown

app = Flask(__name__)

markdown_app = Markdown(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    # if request.method == "POST":
    mkd = open('test.md', 'r')

    mkd = mkd.read()

    return render_template('home.html', mkd=mkd)

    # return render_template('home.html', mkd='None')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')
