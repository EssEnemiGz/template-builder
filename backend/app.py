from flask import *
from flask_cors import CORS
from dotenv import load_dotenv

# Micro services import
import services.render as render

app = Flask(__name__)
CORS(app, resources={
    r"/users": {
        "origins": ["http://127.0.0.1:5555", "http://localhost:5555"]
    }
})

load_dotenv()

# Blueprints
app.register_blueprint(render.render_bp)

@app.route('/')
def hello_world():
    """Renders the index page."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Renders the dashboard page."""
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)