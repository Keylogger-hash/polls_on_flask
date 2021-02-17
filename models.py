from sqlalchemy import ForeignKey, Column, Integer, DateTime, String,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from __init__ import db

from flask_login import UserMixin, LoginManager
from flask_security import RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash


login_manager = LoginManager()
class Polls(db.Model):
    __tablename__ = 'polls'
    id = Column(Integer,unique=True,primary_key=True,autoincrement=True)
    text = Column(String)
    pub_date=Column(DateTime,default=datetime.now())

    def __repr__(self):
        return f'polls_text:{self.text}'

class Choice(db.Model):
    __tablename__ = 'choice'
    choice_id = Column(Integer,unique=True,primary_key=True,autoincrement=True)
    choice_text = Column(String,nullable=False)
    votes = Column(Integer,default=0,nullable=False)
    question_id = Column(Integer,ForeignKey('polls.id',ondelete='CASCADE'))


roles_users = db.Table(
"roles_users",
Column('user_id',db.Integer(),db.ForeignKey('users.id')),
Column('role_id',db.Integer(),db.ForeignKey('roles.id'))
)


class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer,primary_key=True)
    name = Column(String(80),unique=True)
    description = Column(String(255))

    def __repr__(self):
        return self.name


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True,)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow)
    # Нужен для security
    active = Column(Boolean)
    # для получения доступа к связанным объектам
    roles = relationship('Role',secondary=roles_users,backref=db.backref('users',lazy='dynamic'))

    #Flask Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    #Flask has security
    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})


    def get_id(self):
        return self.id
    #Required administrative interface
    def __unicode__(self):
        return self.username

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
