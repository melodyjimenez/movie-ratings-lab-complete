"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():

    return render_template('homepage.html')

@app.route('/movies')
def movies():
    
    movies = crud.return_all_movies()
    return render_template('all_movies.html', movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)
    

@app.route('/users')
def show_user():
    users = crud.get_all_users()
    return render_template("users.html", users=users)


@app.route('/users', methods=["POST"])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route('/login', methods = ["POST"])
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user.password == password:
        session['current_user'] = user.email
        flash("Logged in!")
        return redirect("/")

@app.route('/ratings/<movie_id>')
def create_rating(movie_id):
    user_rating = request.args.get('rating')
    email = session['current_user']
    user = crud.get_user_by_email(email)
    movie = crud.get_movie_by_id(movie_id)

    rating = crud.create_rating(user,movie,user_rating)

    db.session.add(rating)
    flash(f"Rating added, your rating is {rating.score}")

    return redirect("/movies")



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

