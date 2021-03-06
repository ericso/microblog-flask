import sys
# Whoosh has bugs with Python 3
if sys.version_info >= (3, 0):
  enable_search = False
else:
  enable_search = True
  import flask.ext.whooshalchemy as whooshalchemy

import re
from hashlib import md5

from app import app, db



# Association table for linking users to followed users
followers = db.Table(
  'followers',
  db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nickname = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime)
  followed = db.relationship(
    'User',
    secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref('followers', lazy='dynamic'),
    lazy='dynamic'
  )

  # The following methods required by Flask-Login
  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    try:
      return unicode(self.id) # Python 2
    except NameError:
      return str(self.id) # Python 3

  # Use gravatar.com to get a user profile picture
  def avatar(self, size):
    return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (
      md5(self.email.encode('utf-8')).hexdigest(),
      size
    )

  # Following functionality
  def follow(self, user):
    """
    Returns self if success, none if failure
    Returned object has to be committed to db
    """
    if not self.is_following(user):
      self.followed.append(user)
      return self

  def unfollow(self, user):
    """
    Returns self if success, none if failure
    Returned object has to be committed to db
    """
    if self.is_following(user):
      self.followed.remove(user)
      return self

  def is_following(self, user):
    """
    Returns True if self is following user, False otherwise
    """
    return self.followed.filter(
      followers.c.followed_id == user.id
    ).count() > 0

  def followed_posts(self):
    """
    Returns the posts from users that this user follows
    """
    return Post.query.join(
      followers,
      (followers.c.followed_id == Post.user_id)
    ).filter(
      followers.c.follower_id == self.id
    ).order_by(
      Post.timestamp.desc()
    )

  def sorted_posts(self):
    """Returns a query object sorted by timestamp
    """
    return Post.query.filter(
      Post.user_id == self.id
    ).order_by(
      Post.timestamp.desc()
    )

  @staticmethod
  def make_unique_nickname(nickname):
    if User.query.filter_by(nickname=nickname).first() is None:
      return nickname

    version = 2
    while True:
      new_nickname = nickname + str(version)
      if User.query.filter_by(
        nickname=new_nickname
      ).first() is None:
        break
      version += 1

    return new_nickname

  @staticmethod
  def make_valid_nickname(nickname):
    return re.sub('[^a-zA-Z0-9\.]', '', nickname)

  def __repr__(self):
    return '<User %r>' % (self.nickname)


class Post(db.Model):

  __searchable__ = ['body']

  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  language = db.Column(db.String(5))

  def __repr__(self):
    return '<Post %r>' % (self.body)


if enable_search:
  whooshalchemy.whoosh_index(app, Post)
