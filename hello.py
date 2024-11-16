from flask import Flask, request
import git

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./f4lazylifes')
        origin = repo.remotes.origin
        repo.create_head('main', 
    origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
        origin.pull()
        return '', 200
    else:
            return '', 400

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"