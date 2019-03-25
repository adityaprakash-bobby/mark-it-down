from flask import Flask, render_template, request, jsonify
# from flaskext.markdown import Markdown
from flask_babel import _

import markdown
from markdown import Markdown
from markdown_checklist.extension import ChecklistExtension
from mdx_unimoji import UnimojiExtension

app = Flask(__name__)

# markdown_app = Markdown(app)

md = Markdown(extensions=[ChecklistExtension(), UnimojiExtension()])

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":

        mkd = md.convert(request.form['simplemarkdown'])

        return render_template('home.html', mkd=mkd)
    
    mkd = ''

    return render_template('home.html', mkd=mkd)

@app.route('/markdown', methods=['POST'])
def markdown():

    return jsonify({'mkd':request.form['simplemarkdown']})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')
