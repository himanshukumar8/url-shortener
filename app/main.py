# app/main.py

from flask import Flask, request, jsonify, redirect, abort
from .services import URLShortenerService
from .storage import InMemoryStorage

# --- App Initialization ---
app = Flask(__name__)

# --- Singleton Instances (created here, not imported) ---
storage = InMemoryStorage()
service = URLShortenerService(storage=storage)

# --- API Endpoints ---

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint to confirm the service is running."""
    return jsonify({"status": "healthy"}), 200

@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    """Shorten URL Endpoint"""
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400

    original_url = data["url"]
    try:
        mapping = service.create_shortened_url(original_url)
        short_url = request.host_url + mapping.short_code
        return jsonify({
            "short_code": mapping.short_code,
            "short_url": short_url
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/<string:short_code>", methods=["GET"])
def redirect_to_url(short_code: str):
    """Redirect Endpoint"""
    original_url = service.get_and_track_url(short_code)
    if original_url:
        return redirect(original_url, code=302)
    else:
        abort(404)

@app.route("/api/stats/<string:short_code>", methods=["GET"])
def get_stats(short_code: str):
    """Analytics Endpoint"""
    stats = service.get_url_stats(short_code)
    if stats:
        stats_dict = {
            "url": stats.original_url,
            "clicks": stats.clicks,
            "created_at": stats.created_at.isoformat()
        }
        return jsonify(stats_dict), 200
    else:
        abort(404)

@app.errorhandler(404)
def not_found(error):
    """Custom error handler for 404 Not Found errors."""
    return jsonify({"error": "Not Found"}), 404