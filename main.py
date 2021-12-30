from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from get_movie import GetMovie


app = Flask(__name__)
app.config['SECRET_KEY'] = 'U6YkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///themovdb.db"
db = SQLAlchemy(app)
movie_global_list = []


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_db_id = db.Column(db.Integer, unique=True, nullable=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    rating = db.Column(db.Float(100), nullable=False)
    ranking = db.Column(db.Integer, unique=False)
    review = db.Column(db.String(400))
    img_url = db.Column(db.String(100), unique=True, nullable=False)


class Addform(FlaskForm):
    title = StringField('Movie Title ')
    submit = SubmitField('Add Movie')


class Updateform(FlaskForm):
    new_rating = FloatField("Your rating out of 10 :", render_kw={"placeholder": ''})
    review = StringField("Your Review")
    submit = SubmitField("Done")


@app.route("/")
def home():
    all_movies = db.session.query(Movie).order_by(Movie.rating).all()
    print('Executing Home def')
    print(all_movies)
    print(len(all_movies))
    return render_template("index.html", movies=all_movies, list_len=len(all_movies))


@app.route("/add", methods=['GET', 'POST'])
def add_movie():
    form = Addform()
    if form.validate_on_submit():
        movie_to_search = form.title.data
        movie_list = GetMovie(movie_to_search).final_movie_list
        movie_global_list.append(movie_list)
        print(movie_global_list)

        return render_template('select.html', movie_data=movie_list)
    return render_template('add.html', form=form)


@app.route("/add-new-record/<int:movie_index>", methods=['GET'])
def add_new_record(movie_index):
    print("\n\n\nInside add_new_record")
    movie_to_add = movie_global_list[0][movie_index]

    new_movie = Movie(
        movie_db_id=movie_to_add['movie_db_id'],
        title=movie_to_add['title'],
        year=movie_to_add['release_date'],
        description=movie_to_add['overview'],
        rating=movie_to_add['rating'],
        img_url=movie_to_add['poster_url']
    )
    db.session.add(new_movie)
    db.session.commit()
    movie_global_list.clear()
    id_of_movie_to_update = Movie.query.filter_by(movie_db_id=movie_to_add['movie_db_id']).first().id
    # return redirect(url_for('update_rating', id_of_movie_to_update))
    return redirect(f"/update/{id_of_movie_to_update}")


@app.route("/delete/<int:movie_id>", methods=['GET', 'POST'])
def delete_movie_record(movie_id):
    movie_to_delete = Movie.query.filter_by(id=movie_id).first()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/update/<int:movie_id>", methods=['GET', 'POST'])
def update_rating(movie_id):
    print(movie_id)
    movie_to_update = Movie.query.filter_by(id=movie_id).first()
    form = Updateform()
    print(movie_to_update, type(movie_to_update))
    if form.validate_on_submit():
        movie_to_update.rating = form.new_rating.data
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', movie=movie_to_update, form=form)


if __name__ == '__main__':
    app.run(debug=True)
