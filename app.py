from website import create_app, apis
import os
import dotenv
dotenv.load_dotenv()
if not bool(int(os.environ['PRODenv'])):
    app = create_app()
    app.run('0.0.0.0', 8080, True)
else:
    from waitress import serve
    serve(create_app(), host='0.0.0.0', port=8080)