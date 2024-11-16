from app import app
from flask import request
import git

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./f4lazylifes')
        origin = repo.remotes.origin
        repo.create_head('main', 
    origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
            return 'Wrong event type', 400

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"