from flask import Flask
import builder

app = Flask(__name__)

@app.route("/")
def live_debugger():
    html = builder.build()
    return html

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)