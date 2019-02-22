from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    com = db.relationship('Comment', backref='user')

    def __repr__(self):
        return '<user %r>' % (self.name)


class Txt(db.Model):
    __tablename__ = 'txt'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    cont = db.Column(db.String(160), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    time = db.Column(db.Text(20), nullable=False)
    com = db.relationship('Comment', backref='txt')

    def __repr__(self):
        return '<activity %r>' % (self.title)


class Comment(db.Model):
    __tablename__ = 'com'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    txtid = db.Column(db.Integer, db.ForeignKey('txt.id'))
    cont = db.Column(db.String(160))
    time = db.Column(db.Text(20), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<com %r>' % (self.id)
