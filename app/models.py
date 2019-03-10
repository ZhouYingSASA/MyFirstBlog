from . import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash


class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    com = db.relationship('Comment')
    right = db.relationship('Right', backref='Users')

    def generate_confirmation_token(self, expiration=3000):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm', self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf.8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.name


class Right(db.Model):
    __tablename__ = "Right"
    r_id = db.Column(db.Integer, primary_key=True, nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    r_name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(200))


class Txt(db.Model):
    __tablename__ = 'Txt'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    cont = db.Column(db.String(160), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    time = db.Column(db.Text(20), nullable=False)
    com = db.relationship('Comment')

    def __repr__(self):
        return '<Activity %r>' % self.title


class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    txt_id = db.Column(db.Integer, db.ForeignKey('Txt.id'))
    cont = db.Column(db.String(160))
    time = db.Column(db.Text(20), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return '<Comment %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
