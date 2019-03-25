from flask import Flask, render_template, request, jsonify
from flaskext.markdown import Markdown
from flask_babel import _

app = Flask(__name__)

markdown_app = Markdown(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        # mkd = open('test.md', 'r')

        # mkd = mkd.read()

        mkd = request.form['simplemarkdown']
        
        return render_template('home.html', mkd=mkd)
    
    mkd = ''

    return render_template('home.html', mkd=mkd)

@app.route('/markdown', methods=['POST'])
def markdown():

    return jsonify({'mkd':request.form['simplemarkdown']})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')
