from flask_login import current_user
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.contrib.github import make_github_blueprint
import json

with open('koda/../keys.json') as keys:
	data = json.load(keys)
	client_id = data['github']["client_id"]
	client_secret = data['github']["client_secret"]

	github_bp = make_github_blueprint(
		client_id=client_id,
	    client_secret=client_secret
	    )

from main import db, OAuth

github_bp.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

from oauth.template import logged_in, error
# create/login local user on successful OAuth login
@oauth_authorized.connect_via(github_bp)
def github_logged_in(blueprint, token):
    logged_in(blueprint=blueprint, token=token)

# notify on OAuth provider error
@oauth_error.connect_via(github_bp)
def github_error(blueprint, error, error_description=None, error_uri=None):
    error(blueprint=blueprint, error=error, error_description=error_description, error_uri=error_uri)

