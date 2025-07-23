# URL Shortener 

A simple, fully functional URL shortening service — similar to [bit.ly](https://bit.ly) or [TinyURL](https://tinyurl.com/) 

## Features

-  Shorten long URLs into unique 6-character codes
-  Redirection using the short code
-  6 comprehensive test cases using `pytest`
-  Basic error handling and URL validation
-  Clean modular structure that's easy to extend

---

## Tech Stack

- Python 3.8+
- Flask 3.x
- Pytest
- Standard Library only (no DBs, no external services)

---

## Running Locally

### 1. Clone the repo

```bash
git clone https://github.com/himanshukumar8/url-shortener.git
cd url-shortener
```
### 2. Create and activate a virtual environment:

# On Windows
```bash
python -m venv venv
```
```bash
.\venv\Scripts\activate
```

# On macOS/Linux
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run the application:
```bash
flask --app app.main run
```
The API will be available at http://localhost:5000.

### 5.  Run tests:
```bash
pytest
```
