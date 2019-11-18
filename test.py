from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return 'Hello World' 

#@app.route('/.well-known/acme-challenge/aVK-Lm7n4jviUzqEeBPw7MmdHv2CndVxi098jjuBbpE')
#def test():
#    return 'aVK-Lm7n4jviUzqEeBPw7MmdHv2CndVxi098jjuBbpE'


if __name__ == '__main__':
    app.run(debug=True)
