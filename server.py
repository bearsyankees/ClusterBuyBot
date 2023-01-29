from os import environ
from flask import Flask
import main
app = Flask(__name__)


@app.route("/")
def home():
    main.main()
    return "@testingmybotbot on twitter"

app.run(host= '0.0.0.0', port=environ.get('PORT'))