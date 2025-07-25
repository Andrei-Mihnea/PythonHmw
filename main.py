from __init__ import create_app
from router import *
from Database.log_db import RequestsLog

app = create_app()
router = Router()
RequestsLog.init_db()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handle_request(path):
    full_path = "/" + path
    if full_path.startswith('/api') or full_path.startswith('/static'):
        return f"Skipped by router: {full_path}", 404
    return router.route(full_path)

app.run(host="0.0.0.0", port=8000)
if __name__ == '__main__':

    app.run(debug=True)
