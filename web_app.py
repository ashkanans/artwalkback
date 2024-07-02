import logging
import time
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, request, jsonify, send_from_directory, g
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from backend.web.handlers.api.dispatcher import RequestDispatcher

app = Flask(__name__, template_folder='templates', static_folder='templates')

auth = HTTPBasicAuth()

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

CORS(app, origins='*')

# Set the secret key to enable sessions
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

UPLOAD_FOLDER = 'uploaded_files'
EXCEL_FOLDER = 'excel_files'
WORD_FOLDER = 'word'
app.config['EXCEL_FOLDER'] = EXCEL_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['WORD_FOLDER'] = WORD_FOLDER
app.config['ROUTES_JSON'] = 'routes.json'

# Default session duration in seconds (5 hours)
DEFAULT_SESSION_DURATION = 5 * 60 * 60

requestDispatcher = RequestDispatcher()

requestDispatcher.add_routes_from_json(app.config['ROUTES_JSON'])

# Setup logging
handler = RotatingFileHandler('app.log', maxBytes=90000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


@app.before_request
def start_timer():
    g.start_time = time.time()


@app.after_request
def log_request(response):
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        log_details = {
            'method': request.method,
            'path': request.path,
            'status': response.status_code,
            'duration': duration,
            'client_ip': request.remote_addr
        }
        app.logger.info(f"Request log: {log_details}")
    return response


@app.route('/')
@limiter.limit("100/second")
def root():
    return render_template('index.html')


@app.route('/api/<path:route>', methods=['GET', 'POST'])
@limiter.limit("1000/second")
def api_route(route):
    response = requestDispatcher.dispatch_request(route, request)
    return jsonify(response)



# Route to serve PDF files
@app.route('/uploaded_files/<filename>')
@limiter.limit("5/second")
def serve_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/excel_files/<filename>')
@limiter.limit("5/second")
def serve_excel(filename):
    return send_from_directory(app.config['EXCEL_FOLDER'], filename)




if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(host="127.0.0.1", port="12345", debug=False)
