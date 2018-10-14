from main import db, OAuth, User
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user, login_user


def logged_in(blueprint, token):
    if not token:
        return False

    resp = blueprint.session.get("/user")
    if not resp.ok:
        msg = "Failed to fetch user info from GitHub."
        return False

    github_info = resp.json()
    print(github_info)
    github_user_id = github_info["id"]
    print(github_user_id)

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=my_id
    )
    print(query)
    try:
        oauth = query.one()
        print(oauth)
    except NoResultFound:
        print(github_user_id)
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=github_user_id,
            token=token,
        )
        print(github_user_id, type(github_user_id))

    if oauth.user:
        # If this OAuth token already has an associated local account,
        # log in that local user account.
        # Note that if we just created this OAuth token, then it can't
        # have an associated local account yet.
        login_user(oauth.user)

    else:
        # If this OAuth token doesn't have an associated local account,
        # create a new local user account for this user. We can log
        # in that account as well, while we're at it.
        user = User(
            # Remember that `email` can be None, if the user declines
            # to publish their email address on GitHub!
            email=github_info["email"],
            username=github_info["login"],
            admin=False
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)

    # Since we're manually creating the OAuth model in the database,
    # we should return False so that Flask-Dance knows that
    # it doesn't have to do it. If we don't return False, the OAuth token
    # could be saved twice, or Flask-Dance could throw an error when
    # trying to incorrectly save it for us.
    return False


def error(blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
