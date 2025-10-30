# clear_users.py
from database import session, Teacher

session.query(Teacher).delete()
session.commit()
print("All teachers deleted!")
