import models
from main import db

def update_score(kategorija, current_user, score):
    if current_user.is_authenticated and score:
        resp = models.Scores.query.filter_by(user_id=current_user.id, kategorija=kategorija).first()
        total = models.Scores.query.filter_by(user_id=current_user.id, kategorija="total").first()
        if resp:
            resp.score += score
        else:
            new_score = models.Scores(score=score, user_id=current_user.id, kategorija=kategorija)
            db.session.add(new_score)

        if total:
            total.score += score
        else:
            new_total = models.Scores(score=score, user_id=current_user.id, kategorija="total")
            db.session.add(new_total)
        db.session.commit()

