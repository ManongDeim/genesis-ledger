
from flask import Flask
from flask_cors import CORS

from routes.auth import auth_bp
from routes.mining import mining_bp

app = Flask(__name__)
CORS(app)  # Opens the API to the React frontend

#Auth Logic
app.register_blueprint(auth_bp)

#Mining Logic
app.register_blueprint(mining_bp)
    
if __name__ == '__main__':
    app.run(debug=True)