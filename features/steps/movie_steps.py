# features/steps/movie_steps.py
from behave import given, when, then
import requests
import os
import sys
from unittest.mock import patch, MagicMock

# Ajout du répertoire parent au chemin pour pouvoir importer app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import app

# Configuration des mocks pour les tests
mock_movies = {
    "now_playing": [
        {"id": 1, "title": "Test Action Movie", "release_date": "2025-04-01", "vote_average": 8.5, 
         "overview": "An action movie", "poster_path": "/action.jpg", "genre_ids": [28]},
        {"id": 2, "title": "Test Comedy", "release_date": "2025-04-02", "vote_average": 7.5, 
         "overview": "A comedy movie", "poster_path": "/comedy.jpg", "genre_ids": [35]}
    ],
    "popular": [
        {"id": 3, "title": "Popular Action", "release_date": "2025-04-03", "vote_average": 9.0, 
         "overview": "A popular action movie", "poster_path": "/popular_action.jpg", "genre_ids": [28]},
        {"id": 4, "title": "Popular Drama", "release_date": "2025-04-04", "vote_average": 8.0, 
         "overview": "A popular drama movie", "poster_path": "/popular_drama.jpg", "genre_ids": [18]}
    ],
    "search": [
        {"id": 5, "title": "Avengers: Endgame", "release_date": "2019-04-24", "vote_average": 8.3, 
         "overview": "After the devastating events of Avengers: Infinity War...", "poster_path": "/avengers.jpg", "genre_ids": [28, 12, 878]},
        {"id": 6, "title": "The Avengers", "release_date": "2012-05-04", "vote_average": 7.7, 
         "overview": "Earth's mightiest heroes must come together...", "poster_path": "/avengers1.jpg", "genre_ids": [28, 12, 878]}
    ]
}

mock_genres = [
    {"id": 28, "name": "Action"},
    {"id": 12, "name": "Aventure"},
    {"id": 35, "name": "Comédie"},
    {"id": 18, "name": "Drame"},
    {"id": 878, "name": "Science-Fiction"}
]

@given('the application is running')
def step_impl(context):
    # Création d'un client de test Flask
    context.client = app.test_client()
    app.config['TESTING'] = True
    
    # Patcher les fonctions d'API
    context.patches = []
    
    # Patch get_now_playing_movies
    now_playing_patch = patch('app.get_now_playing_movies')
    mock_now_playing = now_playing_patch.start()
    mock_now_playing.return_value = {"results": mock_movies["now_playing"]}
    context.patches.append(now_playing_patch)
    
    # Patch get_popular_movies
    popular_patch = patch('app.get_popular_movies')
    mock_popular = popular_patch.start()
    mock_popular.return_value = {"results": mock_movies["popular"]}
    context.patches.append(popular_patch)
    
    # Patch search_movies
    search_patch = patch('app.search_movies')
    mock_search = search_patch.start()
    mock_search.return_value = {"results": mock_movies["search"]}
    context.patches.append(search_patch)
    
    # Patch get_movie_genres
    genres_patch = patch('app.get_movie_genres')
    mock_genres_func = genres_patch.start()
    mock_genres_func.return_value = mock_genres
    context.patches.append(genres_patch)

@given('I am on the home page')
def step_impl(context):
    context.response = context.client.get('/')

@given('I am on the "{page}" page')
def step_impl(context, page):
    context.response = context.client.get(f'/{page}')

@when('I visit the home page')
def step_impl(context):
    context.response = context.client.get('/')

@when('I visit the "{page}" page')
def step_impl(context, page):
    context.response = context.client.get(f'/{page}')

@when('I search for "{query}"')
def step_impl(context, query):
    context.response = context.client.get(f'/search?query={query}')

@when('I filter by the "{genre_name}" genre')
def step_impl(context, genre_name):
    # Trouver l'ID du genre à partir du nom
    genre_id = None
    for genre in mock_genres:
        if genre["name"] == genre_name:
            genre_id = genre["id"]
            break
    
    if genre_id is None:
        raise ValueError(f"Genre '{genre_name}' not found in mock data")
    
    # Récupérer l'URL actuelle
    path = context.response.request.path
    context.response = context.client.get(f'{path}?genre={genre_id}')

@when('I click on the "{link_text}" link')
def step_impl(context, link_text):
    # Simuler un clic sur un lien - dans un contexte BDD avec un client Flask,
    # nous allons simplement rediriger vers l'URL appropriée
    if link_text == "Films en salle":
        context.response = context.client.get('/now-playing')
    elif link_text == "Films populaires":
        context.response = context.client.get('/popular')
    else:
        raise ValueError(f"Unknown link text: {link_text}")

@then('I should see a welcome message')
def step_impl(context):
    assert b'Bienvenue sur Cin\xc3\xa9ma Explorer' in context.response.data

@then('I should see links to "Films en salle" and "Films populaires"')
def step_impl(context):
    assert b'Films en salle' in context.response.data
    assert b'Films populaires' in context.response.data

@then('I should see the title "{title}"')
def step_impl(context, title):
    assert title.encode('utf-8') in context.response.data

@then('I should see a list of movies')
def step_impl(context):
    # Vérifier si au moins un titre de film apparaît dans la réponse
    if context.response.request.path == '/now-playing':
        assert mock_movies["now_playing"][0]["title"].encode('utf-8') in context.response.data
    elif context.response.request.path == '/popular':
        assert mock_movies["popular"][0]["title"].encode('utf-8') in context.response.data

@then('I should see search results')
def step_impl(context):
    assert b'Recherche de films' in context.response.data

@then('the results should contain "{query}" related movies')
def step_impl(context, query):
    # Vérifier que les résultats contiennent des films liés à la requête
    for movie in mock_movies["search"]:
        if query in movie["title"]:
            assert movie["title"].encode('utf-8') in context.response.data

@then('I should only see movies in the "{genre_name}" genre')
def step_impl(context, genre_name):
    # Trouver l'ID du genre à partir du nom
    genre_id = None
    for genre in mock_genres:
        if genre["name"] == genre_name:
            genre_id = genre["id"]
            break
    
    if genre_id is None:
        raise ValueError(f"Genre '{genre_name}' not found in mock data")
    
    # Vérifier que les films du genre apparaissent
    path = context.response.request.path
    if path == '/now-playing':
        for movie in mock_movies["now_playing"]:
            if genre_id in movie["genre_ids"]:
                assert movie["title"].encode('utf-8') in context.response.data
            else:
                assert movie["title"].encode('utf-8') not in context.response.data
    elif path == '/popular':
        for movie in mock_movies["popular"]:
            if genre_id in movie["genre_ids"]:
                assert movie["title"].encode('utf-8') in context.response.data
            else:
                assert movie["title"].encode('utf-8') not in context.response.data

@then('I should be redirected to the "{page}" page')
def step_impl(context, page):
    assert context.response.request.path == f'/{page}'

mock_tv_shows = [
    {"id": 3, "name": "Top Rated Drama", "first_air_date": "2025-04-03", "vote_average": 9.8, 
     "overview": "A top rated drama series", "poster_path": "/top_rated_drama.jpg", "genre_ids": [18]},
    {"id": 4, "name": "Top Rated Comedy", "first_air_date": "2025-04-04", "vote_average": 9.5, 
     "overview": "A top rated comedy series", "poster_path": "/top_rated_comedy.jpg", "genre_ids": [35]}
]

mock_tv_genres = [
    {"id": 18, "name": "Drame"},
    {"id": 35, "name": "Comédie"},
    {"id": 10765, "name": "Science-Fiction & Fantastique"}
]

# Dans la fonction step_impl de @given('the application is running'),
# ajouter les patches pour les fonctions de séries TV:

# Patch get_top_rated_tv_shows
top_rated_tv_patch = patch('app.get_top_rated_tv_shows')
mock_top_rated_tv = top_rated_tv_patch.start()
mock_top_rated_tv.return_value = {"results": mock_tv_shows}
context.patches.append(top_rated_tv_patch)

# Patch get_tv_genres
tv_genres_patch = patch('app.get_tv_genres')
mock_tv_genres_func = tv_genres_patch.start()
mock_tv_genres_func.return_value = mock_tv_genres
context.patches.append(tv_genres_patch)

# Modifier la fonction step_impl de @when('I click on the "{link_text}" link')
@when('I click on the "{link_text}" link')
def step_impl(context, link_text):
    # Simuler un clic sur un lien
    if link_text == "Films en salle":
        context.response = context.client.get('/now-playing')
    elif link_text == "Séries TV les mieux notées":  # Changé
        context.response = context.client.get('/top-rated-tv')  # Changé
    else:
        raise ValueError(f"Unknown link text: {link_text}")

# Ajouter cette nouvelle étape
@then('I should see a list of TV shows')
def step_impl(context):
    # Vérifier si au moins un titre de série TV apparaît dans la réponse
    assert mock_tv_shows[0]["name"].encode('utf-8') in context.response.data