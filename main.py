from __init__ import create_app
from router import *
from Database.log_db import RequestsLog
from Database.user_db import User
from Frontend import request_context
from flask import Flask, request, redirect, make_response

app = create_app()
router = Router()

RequestsLog.init_db()
User.init_db()

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def handle_request(path):
    full_path = "/" + path

    if full_path.startswith('/api') or full_path.startswith('/static'):
        return f"Skipped by router: {full_path}", 404
    return router.route(full_path)

app.run(host="0.0.0.0", port=8000)
if __name__ == '__main__':

    app.run(debug=True)
