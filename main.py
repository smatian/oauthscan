from flask import Flask, redirect
from config import Config
from blueprints.instagram import instagram_blueprint

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(instagram_blueprint, url_prefix='/instagram')

@app.route("/")
def instaRedirect():
    return redirect("/instagram")
    


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
