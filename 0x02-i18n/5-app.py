#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, request, render_template, g
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)

# User table mockup
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user(user_id):
    """
    Retrieve a user dictionary by user_id.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: The user dictionary if found, None otherwise.
    """
    return users.get(user_id)

@app.before_request
def before_request():
    """
    A function that runs before each request to set the current user
    in the global Flask context if a user ID is provided via the
    'login_as' URL parameter.
    """
    user_id = request.args.get('login_as')
    if user_id:
        g.user = get_user(int(user_id))
    else:
        g.user = None

@babel.localeselector
def get_locale():
    """
    Select the best matching locale from the request. Checks for a 'locale'
    parameter in the URL and defaults to the accepted languages from the request.

    Returns:
        str: The locale to use for this request.
    """
    if 'locale' in request.args:
        requested_locale = request.args.get('locale')
        if requested_locale in ['fr', 'en']:
            return requested_locale
    return request.accept_languages.best_match(['en', 'fr'])

@app.route('/', strict_slashes=False)
def index():
    """
    Render the index page.

    Returns:
        str: The rendered HTML template for the index page.
    """
    return render_template('5-index.html')

if __name__ == '__main__':
    app.run(debug=True)
