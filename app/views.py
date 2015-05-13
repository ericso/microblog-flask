from flask import render_template

from app import app


@app.route('/')
@app.route('/index')
def index():
  user = {'nickname': 'Eric'} # Fake user
  posts = [ # Fake array of posts
    {
      'author': {'nickname': 'John'},
      'body': 'Beautiful day in San Francisco!'
    },{
      'author': {'nickname': 'Susan'},
      'body': 'The Avengers movie, soOooOOoOooo cool!'
    }
  ]

  return render_template(
    'index.html',
    title='Home',
    user=user,
    posts=posts
  )
