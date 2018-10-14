from flask_login import current_user
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.contrib.google import make_google_blueprint


google_bp = make_google_blueprint(
    client_id="61570463416-39jkgsv8h1bfkl7epvqebli5l1qbfvcj.apps.googleusercontent.com",
    client_secret="lS5ex9zq9S-CWA7sMd_TnOoE",
    scope=["profile", "email"],
)

from main import OAuth, db
google_bp.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

from oauth.template import logged_in, error
# create/login local user on successful OAuth login
@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    logged_in(blueprint=blueprint, token=token)

# notify on OAuth provider error
@oauth_error.connect_via(google_bp)
def google_error(blueprint, error, error_description=None, error_uri=None):
    error(blueprint=blueprint, error=error, error_description=error_description, error_uri=error_uri)

