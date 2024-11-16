from app import app
from flask import request
from app.lib import is_valid_signature
import git
import os
import json

W_SECRET = app.config['W_SECRET']

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # abort_code = 418
        # # Do initial validations on required headers
        # if 'X-Github-Event' not in request.headers:
        #     abort(abort_code)
        # if 'X-Github-Delivery' not in request.headers:
        #     abort(abort_code)
        # if 'X-Hub-Signature' not in request.headers:
        #     abort(abort_code)
        # if not request.is_json:
        #     abort(abort_code)
        # if 'User-Agent' not in request.headers:
        #     abort(abort_code)
        # ua = request.headers.get('User-Agent')
        # if not ua.startswith('GitHub-Hookshot/'):
        #     abort(abort_code)

        # event = request.headers.get('X-GitHub-Event')
        # if event == "ping":
        #     return json.dumps({'msg': 'Hi!'})
        # if event != "push":
        #     return json.dumps({'msg': "Wrong event type"})

        x_hub_signature = request.headers.get('X-Hub-Signature')
        # webhook content type should be application/json for request.data to have the payload
        # request.data is empty in case of x-www-form-urlencoded
        if not is_valid_signature(x_hub_signature, request.data, W_SECRET):
            print('Deploy signature failed: {sig}'.format(sig=x_hub_signature))
            # abort(abort_code)
            return '', 404

        payload = request.get_json()
        if payload is None:
            print('Deploy payload is empty: {payload}'.format(
                payload=payload))
            # abort(abort_code)
            return '', 404

        if payload['ref'] != 'refs/heads/main':
            return json.dumps({'msg': 'Not main; ignoring'})
        
        repo = git.Repo('./f4lazylifes')
        origin = repo.remotes.origin

        pull_info = origin.pull()

        if len(pull_info) == 0:
            return json.dumps({'msg': "Didn't pull any information from remote!"})
        if pull_info[0].flags > 128:
            return json.dumps({'msg': "Didn't pull any information from remote!"})

        commit_hash = pull_info[0].commit.hexsha
        build_commit = f'build_commit = "{commit_hash}"'
        print(f'{build_commit}')
        return 'Updated PythonAnywhere server to commit {commit}'.format(commit=commit_hash), 200
    else:
        return 'Wrong event type', 400

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World! Not sure if works 😅"