from app import app
from models import db, User


db.drop_all()
db.create_all()

u1 = User(username='Rambo', password='p123', email='rambo@google.com',
          first_name='Jack', last_name='Williams')
u2 = User(username='Catty', password='p334', email='mw@aol.com',
          first_name='May', last_name='Wilks')

db.session.add_all([u1, u2])
db.session.commit()
