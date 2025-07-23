from __init__ import create_app
from Database.db import RequestsLog
app = create_app()

if __name__ == '__main__':
    RequestsLog.init_db()
    app.run(debug=True)
