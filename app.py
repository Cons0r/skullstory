from website import create_app, apis
import os
app = create_app()
app.run('0.0.0.0', 8080, True)