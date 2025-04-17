from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

def create_scheduler(app: Flask) -> None:
    """
    Crée et configure le planificateur de tâches
    
    Args:
        app: Instance de l'application Flask
    """
    # Récupération de la configuration
    sync_interval = app.config.get('SYNC_INTERVAL_MINUTES', 60)
    
    # Création du planificateur
    scheduler = BackgroundScheduler()
    
    # Définition de la tâche de synchronisation
    def sync_movies_job():
        with app.app_context():
            # Récupération du cas d'utilisation
            sync_movies_use_case = app.config['USE_CASES']['sync_movies']
            # Exécution de la synchronisation
            result = sync_movies_use_case.execute()
            # Log des résultats
            print(f"Synchronisation TMDB terminée: {result}")
    
    # Ajout de la tâche au planificateur
    scheduler.add_job(
        func=sync_movies_job,
        trigger=IntervalTrigger(minutes=sync_interval),
        id='sync_movies_job',
        name='Synchronisation des films TMDB',
        replace_existing=True
    )
    
    # Démarrage du planificateur
    scheduler.start()
    
    # Arrêt du planificateur à la fermeture de l'application
    atexit.register(lambda: scheduler.shutdown())
