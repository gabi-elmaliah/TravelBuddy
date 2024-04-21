from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy()
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	password = db.Column(db.String(80), nullable=False)
	openness=  db.Column(db.Integer(), nullable=False)
	conscientiousness=db.Column(db.Integer(), nullable=False)
	extraversion=db.Column(db.Integer(), nullable=False)
	agreeableness=db.Column(db.Integer(), nullable=False)
	neuroticism=db.Column(db.Integer(), nullable=False)
	
	
	
	

db.init_app(app)
 
 
with app.app_context():
	db.create_all()
 
	

	
class RegisterForm(FlaskForm):
	username = StringField(validators=[
						   InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

	password = PasswordField(validators=[
							 InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

	submit = SubmitField('Continue')

	def validate_username(self, username):
		existing_user_username = User.query.filter_by(
			username=username.data).first()
		if existing_user_username:
			raise ValidationError(
				'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
	username = StringField(validators=[
						   InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

	password = PasswordField(validators=[
							 InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

	submit = SubmitField('Login')


@app.route('/')
def home():
	return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user)
				return redirect(url_for('dashboard'))
			
	return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	session.pop("username",None)
	session.pop("password",None)
	logout_user()
	return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		#new_user = User(username=form.username.data, password=hashed_password)
		#new_user.openness = 1
		#new_user.conscientiousness = 0
		#new_user.extraversion = 0
		#new_user.agreeableness = 0
		#new_user.neuroticism = 0
		username=form.username.data
		session["username"]=username
		session["password"]=hashed_password
		#db.session.add(new_user)
		#db.session.commit()
		return redirect(url_for('questionnaire'))

	return render_template('register.html', form=form)

@ app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
	print(request.form)
	if request.method=='POST':
		username = session["username"]
		password = session["password"]
		openness = request.form.get('openness',type=int)
		conscientiousness = request.form.get('conscientiousness',type=int)
		extraversion = request.form.get('extraversion',type=int)
		agreeableness = request.form.get('agreeableness',type=int)
		neuroticism = request.form.get('neuroticism',type=int)
		 # Check if all fields have been filled out
		if not (openness and conscientiousness and extraversion and agreeableness and neuroticism):
			# If any field is missing, render the questionnaire template again with an error message.
			return render_template('questionnaire.html', error="Please answer all questions.")

		new_user = User(username=username, password=password, openness=openness, conscientiousness=conscientiousness, extraversion=extraversion, agreeableness=agreeableness, neuroticism=neuroticism)
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('questionnaire.html')

	

if __name__ == "__main__":
	app.run(debug=True)