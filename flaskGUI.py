from flask import Flask, render_template, request
import webbrowser
app = Flask(__name__)


def contact():
    if request.method == 'POST':
        if request.form['submit'] == 'Do Something':
            pass # do something
        elif request.form['submit'] == 'Do Something Else':
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
	url = "http://127.0.0.1:5000/"
	webbrowser.open(url)
	app.run()