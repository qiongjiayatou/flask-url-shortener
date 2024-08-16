from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
import string, random, os

app = Flask(__name__)

# Configure the PostgreSQL database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/url_shortener_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@database-1.cvyo8iqekh2m.eu-west-3.rds.amazonaws.com:5432/url_shortener_db'
# Connect to rds
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@database-1.cvyo8iqekh2m.eu-west-3.rds.amazonaws.com:5432/url_shortener_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.before_first_request
def before_first_request():
    upgrade()

class URLMap(db.Model):
    __tablename__ = 'url_map'
    __table_args__ = {'schema': 'public'} 
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(6), unique=True, nullable=False)

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        existing_url = URLMap.query.filter_by(original_url=original_url).first()
        if existing_url:
            short_url = existing_url.short_url
        else:
            short_url = generate_short_url()
            new_url = URLMap(original_url=original_url, short_url=short_url)
            db.session.add(new_url)
            db.session.commit()
        return render_template('home.html', short_url=short_url)
    return render_template('home.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url_entry = URLMap.query.filter_by(short_url=short_url).first_or_404()
    return redirect(url_entry.original_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
