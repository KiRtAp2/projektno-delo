from flask_login import current_user
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.contrib.twitter import make_twitter_blueprint


twitter_bp = make_twitter_blueprint(
  	api_key="3dXqbLcXrrFcRePS20dBkOuER",
    api_secret="9qTupdudfn1wne8ziqg43LNZUIIrw7y8vFDIBsZxFFm4PQuJ7e",)

from main import OAuth, db
twitter_bp.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

from oauth.template import logged_in, error
# create/login local user on successful OAuth login
@oauth_authorized.connect_via(twitter_bp)
def twitter_logged_in(blueprint, token):
    logged_in(blueprint=blueprint, token=token)

# notify on OAuth provider error
@oauth_error.connect_via(twitter_bp)
def twitter_error(blueprint, error, error_description=None, error_uri=None):
    error(blueprint=blueprint, error=error, error_description=error_description, error_uri=error_uri)

