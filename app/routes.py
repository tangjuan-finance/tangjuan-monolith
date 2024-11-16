from app import app
from flask import request
import git

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

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"