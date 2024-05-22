from flask import Flask
from config import Config
from blueprints.instagram import instagram_blueprint

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(instagram_blueprint, url_prefix='/instagram')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
