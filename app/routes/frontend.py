from flask import Blueprint, redirect, render_template
from app.models import URL
from app import db

frontend_bp = Blueprint('frontend', __name__)
url_model = URL(db)

@frontend_bp.route('/')
def index():
    return render_template('index.html')

@frontend_bp.route('/<short_code>')
def redirect_to_url(short_code):
    # 1. Find the URL
    url = url_model.find_by_short_code(short_code)
    if not url:
        return "URL not found", 404
    
    # 2. Increment accessCount
    try:
        result = url_model.increment_access_count(short_code)
        if result.modified_count == 0:
            print(f"⚠️ Failed to increment accessCount for {short_code}")
        else:
            print(f"✅ Incremented accessCount for {short_code}")
    except Exception as e:
        print(f"🔥 Error incrementing accessCount: {str(e)}")
    
    # 3. Redirect with anti-cache headers
    response = redirect(url['originalUrl'], code=301)
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response
