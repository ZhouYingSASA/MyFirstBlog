from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, nullable=False, default=False)
    com = db.relationship('Comment', backref='users')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<user %r>' % self.name


class Txt(db.Model):
    __tablename__ = 'txt'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    cont = db.Column(db.String(160), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    time = db.Column(db.Text(20), nullable=False)
    com = db.relationship('Comment', backref='txt')

    def __repr__(self):
        return '<activity %r>' % self.title


class Comment(db.Model):
    __tablename__ = 'com'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    txtid = db.Column(db.Integer, db.ForeignKey('txt.id'))
    cont = db.Column(db.String(160))
    time = db.Column(db.Text(20), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<com %r>' % self.id
