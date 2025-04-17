# Point d'entrée principal de l'application
from application.app_factory import create_app
from application.jobs.scheduler import create_scheduler

# Création de l'application Flask
app = create_app()

# Configuration et démarrage du planificateur de tâches
create_scheduler(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
