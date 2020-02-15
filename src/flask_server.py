from flask import Flask, request

app = Flask(__name__)


@app.route('/api/callback/', methods=['GET'])
def hello_world():
    auth_code: str = request.args.get("code")
    return {"auth-token": auth_code}


app.run(port=5000, debug=True)
