from flask import Flask, jsonify, render_template
from flask_cors import CORS
import asyncio
import threading
from datetime import datetime, timedelta
from scraper import SeatScraper

app = Flask(__name__)
CORS(app)

cache_data = {}
cache_timestamp = None
CACHE_DURATION = 15 * 60  # 15 minutes in seconds

scraper = SeatScraper()

def is_cache_valid():
    global cache_timestamp
    if cache_timestamp is None:
        return False
    return datetime.now() - cache_timestamp < timedelta(seconds=CACHE_DURATION)

def run_async_scraping():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(scraper.get_all_seats_data())
    finally:
        loop.close()

def update_cache():
    global cache_data, cache_timestamp
    try:
        cache_data = run_async_scraping()
        cache_timestamp = datetime.now()
        return True
    except Exception as e:
        print(f"Error updating cache: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/seats')
def get_seats():
    global cache_data, cache_timestamp
    
    if not is_cache_valid():
        success = update_cache()
        if not success:
            return jsonify({
                'error': 'Failed to fetch seat data',
                'cached_at': cache_timestamp.isoformat() if cache_timestamp else None
            }), 500
    
    return jsonify({
        'data': cache_data,
        'cached_at': cache_timestamp.isoformat(),
        'cache_expires_at': (cache_timestamp + timedelta(seconds=CACHE_DURATION)).isoformat()
    })

@app.route('/api/status')
def get_status():
    return jsonify({
        'cache_valid': is_cache_valid(),
        'cached_at': cache_timestamp.isoformat() if cache_timestamp else None,
        'cache_expires_at': (cache_timestamp + timedelta(seconds=CACHE_DURATION)).isoformat() if cache_timestamp else None
    })

if __name__ == '__main__':
    # For development only - use gunicorn for production
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)