# backend/config/config.py
import urllib

SQL_SERVER_CONFIG = {
    'server':'192.168.0.57',
    # 'server': 'localhost',
    'database': 'estdco',
    # 'database': 'realtimedata',
    'username': 'estdco_service_account',
    'password': 'qH,40b1]A08=',
    'driver': 'ODBC Driver 17 for SQL Server',  # Use the appropriate driver name without curly braces
}

SQL_SERVER_URL = (
    f"mssql+pyodbc://{SQL_SERVER_CONFIG['username']}:{urllib.parse.quote_plus(SQL_SERVER_CONFIG['password'])}@"
    f"{SQL_SERVER_CONFIG['server']}/{SQL_SERVER_CONFIG['database']}?driver={SQL_SERVER_CONFIG['driver']}"
)

# SQL Server configuration
# SQL_SERVER_CONFIG = {
#     'server': 'localhost\\SQLEXPRESS01',
#     'database': 'cm',
#     'driver': 'ODBC Driver 17 for SQL Server',  # Use the appropriate driver name without curly braces
#     # Other SQL Server connection parameters...
# }
#
# # Connection string
# SQL_SERVER_URL = (
#     f"mssql+pyodbc://{SQL_SERVER_CONFIG['server']}/{SQL_SERVER_CONFIG['database']}?"
#     f"driver={SQL_SERVER_CONFIG['driver']}&trusted_connection=yes"
# )
