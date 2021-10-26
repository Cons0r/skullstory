<<<<<<< HEAD
from website import create_app
app = create_app()
=======
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello again World!"
>>>>>>> a76924e01e7b11824210b7f45cb4c0eb17ce6020

if __name__ == "__main__":
  app.run('0.0.0.0', 8080, True)