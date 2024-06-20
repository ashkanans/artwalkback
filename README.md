# Dollar-Dashboard-Flask

A Flask-based web application for monitoring and visualizing real-time and historical data related to the Dollar,
featuring interactive tables and dynamic charts using Chart.js and DataTables.

# Project Dependencies

## Scraper

Install the packages required for web scraping:

```bash
pip install requests beautifulsoup4
```

## Flask Web App

Install Flask:

```bash
pip install Flask
```

## HTML File Dependencies

The HTML file includes external dependencies such as Chart.js, Bootstrap, and DataTables. These are included through CDN
links in the HTML file, so no separate installation is required. Ensure your internet connection is active when running
the Flask app to fetch these dependencies.

# Running the Project

Once dependencies are installed, navigate to the project directory and run your Flask application:

```bash
python web_app.py
```

Access the app in your web browser at http://127.0.0.1:5000/.

# Project Structure

The project follows a typical structure for a web application, with 3-tier a backend (Model, DAO and Service layers),
frontend, and associated configuration files. Here's a brief description of each major component:

1. **Backend:**
    - **dao (OLD):** Contains modules related to data access for different entities like 'tgju' and 'tsetmc' (Will be
      revised soon).
    - **database_config:** Configuration files related to the database.
    - **model (OLD):** Contains modules defining data models for entities similar to those in the 'dao' directory (Will
      be revised soon).
    - **scraper:** Modules for web scraping, likely retrieving data from 'tgju' and 'tsetmc' and 'codal'.
    - **service (OLD):** Modules responsible for business logic, possibly including modules for user login and financial
      data services (Will be revised soon).
    - **tests:** Directory for test modules.

2. **Files:** A directory that presumably contains miscellaneous files used by the application.

3. **Frontend:** Empty (for now!)

4. **Static:**
    - **css, img, js, json, lib:** Directories for static files used by the frontend.
    - **scss/bootstrap:** Stylesheets for the Bootstrap framework.

5. **Templates:** Contains HTML templates for different parts of the application, organized into subdirectories like '
   indexes,' 'instruments,' and 'stocks.'
