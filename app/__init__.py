from flask import Flask
import os
from dotenv import load_dotenv
from app.extensions import db  # <- Importe db depuis extensions
from app.domain.movie_controller import movie_bp
from app.domain.tv_controller import tv_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "une_clé_par_défaut")
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db/{os.getenv('POSTGRES_DB')}"
    )

    db.init_app(app)

    with app.app_context():
        from app.models import Movie, Genre
        db.create_all()

    app.register_blueprint(movie_bp)
    app.register_blueprint(tv_bp)

    return app
