from gino import Gino
from datetime import date


PG_DSN = 'postgres://aiohttp:1234@127.0.0.1:5432/aiohttp'
db = Gino()


class AdModel(db.Model):
    __tablename__ = 'advertisements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(100))
    create_date = db.Column(db.String, default=str(date.today().strftime('%d.%m.%Y')))
    owner = db.Column(db.String(50))

    _idx1 = db.Index('app_advertisements_title', 'title', unique=True)

    def to_dict(self):
        ad_data = super().to_dict()
        return ad_data
