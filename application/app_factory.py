from flask import Flask, render_template
from config import get_config
from infrastructure.db.database import init_db
from application.dependency_injection import setup_dependencies

def create_app() -> Flask:
    """
    Factory pour créer et configurer l'application Flask
    
    Returns:
        Instance configurée de l'application Flask
    """
    # Création de l'application
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Configuration
    app.config.from_object(get_config())
    
    # Initialisation de la base de données
    init_db(app)
    
    # Configuration des dépendances et des contrôleurs
    setup_dependencies(app)
    
    # Route principale (homepage)
    @app.route('/')
    def home():
        # Récupération des contrôleurs
        from adapters.controllers.movie_controller import MovieController
        movie_controller = app.config['CONTROLLERS']['movie']
        
        # Réutilisation de la logique du contrôleur des films populaires
        return movie_controller.popular()
    
    # Gestionnaire d'erreur 404
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html', title="Page non trouvée"), 404
    
    return app
