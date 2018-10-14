from flask_login import current_user
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.contrib.facebook import make_facebook_blueprint


facebook_bp = make_facebook_blueprint(
    client_id='215709269202041',
    client_secret='8ee08326a8d49532a6c737e09cbd086b',
    scope=["public_profile", "email"],
)

from main import OAuth, db
facebook_bp.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

from oauth.template import logged_in, error
# create/login local user on successful OAuth login
@oauth_authorized.connect_via(facebook_bp)
def facebook_logged_in(blueprint, token):
    logged_in(blueprint=blueprint, token=token)

# notify on OAuth provider error
@oauth_error.connect_via(facebook_bp)
def facebook_error(blueprint, error, error_description=None, error_uri=None):
    error(blueprint=blueprint, error=error, error_description=error_description, error_uri=error_uri)

