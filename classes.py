import sqlalchemy
from db_functions import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'userdata'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    login = sqlalchemy.Column(sqlalchemy.String, unique=True)

    passwordhash = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)

    username = sqlalchemy.Column(sqlalchemy.Text, default='User')

    rp = sqlalchemy.Column(sqlalchemy.Text)

    favourite = sqlalchemy.Column(sqlalchemy.Text)
