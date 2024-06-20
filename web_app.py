import logging
import time
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, request, jsonify, send_from_directory, g
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from backend.web.handlers.api.dispatcher import RequestDispatcher
from backend.web.service.cbi.service import CBIService
from backend.web.service.codal.service import CodalService
from backend.web.service.log import LogService
from backend.web.service.oilprice.service import OilPriceService

app = Flask(__name__, template_folder='frontend/build', static_folder='frontend/build/static')

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
    log = LogService()
    log.create_log(endpoint=request.endpoint, http_method=request.method, client_ip=request.remote_addr)
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


@app.route('/oilprice_filter_submit_form', methods=['POST'])
@limiter.limit("5/second")
def op_filter_submit_form():
    id = request.form['id']
    from_date = request.form['from_date']
    to_date = request.form['to_date']

    print(f"id: {id}")
    print(f"from_date: {from_date}")
    print(f"to_date: {to_date}")

    oilPriceService = OilPriceService()
    data = oilPriceService.get_relative_data(id, to_date, from_date)

    columns = ["Name", "Price", "Date"]
    cells = ["item.blend_name", "item.price", "item.time"]

    cells = [cell.split(".")[1] for cell in cells]

    oilPriceService = OilPriceService()
    dropdown_data = oilPriceService.get_combined_dropdown_data()

    return render_template('/endpoints/oilprice/filter.html',
                           dropdown_data=dropdown_data,
                           data=data[:1000],
                           columns=columns,
                           cells=cells
                           )


@app.route('/op/filter')
@limiter.limit("5/second")
def oilprice_filter():
    oilPriceService = OilPriceService()
    dropdown_data = oilPriceService.get_combined_dropdown_data()

    columns = ["Name", "Last Close Price", "Last Price", "Change Percent", "Date Time"]
    cells = ["item.blend_name", "item.last_close_price", "item.last_price", "item.change_percent", "item.last_time"]

    cells = [cell.split(".")[1] for cell in cells]

    return render_template('/endpoints/oilprice/filter.html',
                           dropdown_data=dropdown_data,
                           data=dropdown_data,
                           columns=columns,
                           cells=cells
                           )


@app.route('/cbi_filter_submit_form', methods=['POST'])
@limiter.limit("5/second")
def cbi_filter_submit_form():
    year = request.form['year']
    month = request.form['month']
    type = request.form['type']

    year = '' if year == '0' else year
    month = '' if month == '0' else month
    type = '' if type == '0' else type

    print(f"year: {year}")
    print(f"month: {month}")
    print(f"type: {type}")

    cbiService = CBIService()
    data = cbiService.get_relative_data(year, month, type)

    columns = ["Inflations", "Price Index", "Type", "Month", "Year"]
    cells = ["item.Inflation", "item.price_index", "item.type", "item.month", "item.year"]

    cells = [cell.split(".")[1] for cell in cells]

    months, types, years = cbiService.get_combined_dropdown_data()

    return render_template('/endpoints/cbi/filter.html',
                           years=years,
                           months=months,
                           types=types,
                           data=data,
                           columns=columns,
                           cells=cells
                           )


@app.route('/cbi/filter')
@limiter.limit("5/second")
def cbi_filter():
    cbiService = CBIService()
    months, types, years = cbiService.get_combined_dropdown_data()

    return render_template('/endpoints/cbi/filter.html',
                           years=years,
                           months=months,
                           types=types,
                           data=[],
                           columns=[],
                           cells=[]
                           )


@app.route('/codal/filter')
@limiter.limit("5/second")
def codal_filter():
    codalService = CodalService()
    all_letters = codalService.get_all_letters()

    columns = ["اطلاعیه در کدال", "زمان انتشار", "نام اطلاعیه", "نام شرکت", "نماد شرکت"]
    cells = ["item.Url", "item.PublishDateTime", "item.Title", "item.persian_company_name", "item.Symbol"]

    cells = [cell.split(".")[1] for cell in cells]

    return render_template('/endpoints/codal/filter.html',
                           letters=all_letters[:10],
                           symbols=[],
                           companyNames=[],
                           tracingNos=[],
                           sources=["letters"],
                           columns=columns,
                           cells=cells
                           )


if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(host="127.0.0.1", port="12345", debug=False)
