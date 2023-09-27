from flask import Flask , render_template, url_for,redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from Authentication import LoginFrom, RegisterFrom, DashbordForm, UserratingForm,UdateProfileFrom
from model import get_similar,movieDict
from databaseTable import db, User, History
import random

app = Flask(__name__)
bcrypt = Bcrypt(app)

# 2) Set the DATABASE URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #connect to the database by SQLALCHEMY_DATABASE_URI : sqlite:/// and it used default connection engine
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # it is used to reduce some warning in the terminal
app.config["SECRET_KEY"] = 'thisisasecreatkey'



db.init_app(app)  #initialize app with database
app.app_context().push()

login_manager = LoginManager() # for instantiating flask login extension
login_manager.init_app(app) # login manager initialize
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

userName = ""
#Home URL
@app.route('/')
def home ():
    key, val = random.choice(list(movieDict.items()))
    similar_movies, recommend_poster = get_similar([key],[5])
    return render_template('home.html',similar_movies = similar_movies,recommend_poster=recommend_poster)

# Login URL
@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginFrom()
    error_massage = ""
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        global userName 
        if user:
            userName = userName + form.username.data
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user) 
                return redirect(url_for('dashboard'))
            else:
                error_massage = "Please put correct password"
               
        else:
            error_massage = "Username is incorrect"
    return render_template('login.html', form=form,error_massage=error_massage)


#Profile URL
@app.route('/profile', methods = ['GET','POST'])
@login_required
def profile():
    global userName 
    succes_msg = ""
    form = UdateProfileFrom()
    user = User.query.filter_by(username = userName ).first()
    if form.validate_on_submit():
        user.username = form.username.data
        db.session.commit()
        succes_msg = "Successfuly update your profile"
        userName = form.username.data
        return render_template('profile.html', form = form,succes_msg=succes_msg)
    return render_template('profile.html',form = form,succes_msg=succes_msg)

#Logout URL
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    global userName
    userName = ""
    logout_user()
    return redirect(url_for('login'))

#Dashboard URL
@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    global userName 
    movie_recod = User.query.filter_by(username = userName).first() # fetch from user object from user table 
    watchlist = movie_recod.history
    if watchlist:
        watchlist.reverse()
        pre_movie = watchlist[0].movie  #fetch last watch movie
        pre_rating = watchlist[0].rating
    else:
        pre_movie, val = random.choice(list(movieDict.items())) # if new user
        pre_rating = 5
    similar_movies, recommend_poster = get_similar([pre_movie],[pre_rating])  # get similar movie of last watch movie
    form = DashbordForm()  # Select movie by this selected form
    
    if form.validate_on_submit():
        searchMovie = form.moviename.data
        similar_movies, recommend_poster = get_similar([searchMovie],[5]) #fetch al similar movie of the selected movie
        return render_template('dashboard.html',form = form,similar_movies = similar_movies,recommend_poster=recommend_poster)
    return render_template('dashboard.html',form = form, similar_movies=similar_movies,recommend_poster=recommend_poster)


@app.route("/review/<string:movie_name>/<path:poster>", methods = ['GET','POST'])
@login_required
def review(movie_name,poster):
    global userName 
    form = UserratingForm()
    feetback_massage = ""
    if form.validate_on_submit():
        rating_value = form.rating.data
        comment = form.comment.data
        user = User.query.filter_by(username = userName).first() #fetch user record
        userMovie = History(movie=movie_name, rating=rating_value, comment = comment,  user = user) #one to many relationship
        db.session.add(userMovie) 
        db.session.commit()
        feetback_massage = "You have successfully reviewed"
        return render_template('review.html',form = form, movie_name = movie_name,poster=poster,feetback_massage = feetback_massage)
    return render_template('review.html',form = form, movie_name = movie_name,poster=poster ,feetback_massage = feetback_massage)


# Registration URL
@app.route('/register', methods= ['GET','POST'])
def register():
    form = RegisterFrom()
    error_massage = ""
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            error_massage = "Username already registered"
            return  render_template('register.html',form = form,error_massage=error_massage)
        else:
            hashed_pass = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username = form.username.data, password = hashed_pass)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return  render_template('register.html',form = form,error_massage=error_massage)


#Main function from where the program start
if __name__ == "__main__":
    app.run(debug=True)
