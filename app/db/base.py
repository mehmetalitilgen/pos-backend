from sqlalchemy.orm import declarative_base




Base = declarative_base()


from app.models.user import User
from app.models.payment import Payment
from app.models.transaction import Transaction
