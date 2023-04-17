'''
  this demo shows how to pass data to and from a flask server
'''
from flask import Flask, request, render_template

# import my personal GPT class
from gpt import GPT

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fun/<type>")
def fun(type):
    pretext=''
    if type=='1':
        pretext='PreText:Change the code to the python code:'
    return render_template("fun.html",type=type,pretext=pretext)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/team")
def team():
    return render_template("team.html")




@app.route('/getGPTResponse/<num>', methods=["POST"])
def getGPTResponse(num):
    outV=""
    print(num)
    if num == '0':
        inputV = request.form["input"]
        outV = g.getResponse(inputV)
    elif num=='1':
        inputV = request.form["input"]
        outV = g.getResponse2Python(inputV)

    return {
        "out": outV.strip()
    }


if __name__ == '__main__':
    APIKEY = "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"
    g = GPT(APIKEY)
    app.run(debug=True, port=5001)
