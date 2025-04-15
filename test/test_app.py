# tests/test_app.py
import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Ajout du répertoire parent au chemin pour pouvoir importer app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, get_now_playing_movies, get_popular_movies, search_movies, get_movie_genres, format_movies

class FlaskMovieAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenue sur Cin\xc3\xa9ma Explorer', response.data)
        
    @patch('app.get_now_playing_movies')
    @patch('app.get_movie_genres')
    def test_now_playing_page(self, mock_genres, mock_now_playing):
        # Mock des données
        mock_now_playing.return_value = {"results": [
            {"id": 1, "title": "Test Movie", "release_date": "2025-04-01", "vote_average": 8.5, 
             "overview": "A test movie", "poster_path": "/test.jpg", "genre_ids": [28, 12]}
        ]}
        mock_genres.return_value = [
            {"id": 28, "name": "Action"},
            {"id": 12, "name": "Aventure"}
        ]
        
        response = self.app.get('/now-playing')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Films actuellement au cin\xc3\xa9ma', response.data)
        self.assertIn(b'Test Movie', response.data)
        
    @patch('app.get_popular_movies')
    @patch('app.get_movie_genres')
    def test_popular_page(self, mock_genres, mock_popular):
        # Mock des données
        mock_popular.return_value = {"results": [
            {"id": 2, "title": "Popular Test", "release_date": "2025-04-01", "vote_average": 9.0, 
             "overview": "A popular test movie", "poster_path": "/popular.jpg", "genre_ids": [28]}
        ]}
        mock_genres.return_value = [
            {"id": 28, "name": "Action"}
        ]
        
        response = self.app.get('/popular')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Films populaires', response.data)
        self.assertIn(b'Popular Test', response.data)
        
    @patch('app.search_movies')
    @patch('app.get_movie_genres')
    def test_search_page(self, mock_genres, mock_search):
        # Mock des données
        mock_search.return_value = {"results": [
            {"id": 3, "title": "Searched Movie", "release_date": "2025-04-01", "vote_average": 7.5, 
             "overview": "A searched movie", "poster_path": "/search.jpg", "genre_ids": [28]}
        ]}
        mock_genres.return_value = [
            {"id": 28, "name": "Action"}
        ]
        
        response = self.app.get('/search?query=test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recherche de films', response.data)
        self.assertIn(b'Searched Movie', response.data)
        
    @patch('requests.get')
    def test_get_now_playing_movies(self, mock_get):
        # Mock de la réponse de l'API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [{"title": "Test Movie"}]}
        mock_get.return_value = mock_response
        
        result = get_now_playing_movies()
        self.assertEqual(result, {"results": [{"title": "Test Movie"}]})
        
    @patch('requests.get')
    def test_get_popular_movies(self, mock_get):
        # Mock de la réponse de l'API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [{"title": "Popular Movie"}]}
        mock_get.return_value = mock_response
        
        result = get_popular_movies()
        self.assertEqual(result, {"results": [{"title": "Popular Movie"}]})
        
    @patch('requests.get')
    def test_search_movies(self, mock_get):
        # Mock de la réponse de l'API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [{"title": "Search Result"}]}
        mock_get.return_value = mock_response
        
        result = search_movies("test")
        self.assertEqual(result, {"results": [{"title": "Search Result"}]})
        
    @patch('requests.get')
    def test_get_movie_genres(self, mock_get):
        # Mock de la réponse de l'API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"genres": [{"id": 28, "name": "Action"}]}
        mock_get.return_value = mock_response
        
        result = get_movie_genres()
        self.assertEqual(result, [{"id": 28, "name": "Action"}])
        
    def test_format_movies(self):
        movies = [
            {"title": "Movie 1", "poster_path": "/poster1.jpg"},
            {"title": "Movie 2", "poster_path": None}
        ]
        
        formatted_movies = format_movies(movies)
        
        self.assertEqual(formatted_movies[0]["poster_url"], "https://image.tmdb.org/t/p/w500/poster1.jpg")
        self.assertEqual(formatted_movies[1]["poster_url"], "/static/no-poster.jpg")

    def test_filter_by_genre(self):
        # Test du filtrage par genre
        with patch('app.get_now_playing_movies') as mock_now_playing, \
             patch('app.get_movie_genres') as mock_genres:
            
            # Mock des données
            mock_now_playing.return_value = {"results": [
                {"id": 1, "title": "Action Movie", "genre_ids": [28], "poster_path": "/poster1.jpg"},
                {"id": 2, "title": "Comedy Movie", "genre_ids": [35], "poster_path": "/poster2.jpg"}
            ]}
            mock_genres.return_value = [
                {"id": 28, "name": "Action"},
                {"id": 35, "name": "Comédie"}
            ]
            
            # Test du filtrage pour le genre Action (id=28)
            response = self.app.get('/now-playing?genre=28')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Action Movie', response.data)
            self.assertNotIn(b'Comedy Movie', response.data)

def test_top_rated_tv_page(self, mock_genres, mock_top_rated_tv):
    # Mock des données
    mock_top_rated_tv.return_value = {"results": [
        {"id": 2, "name": "Top Rated TV Show", "first_air_date": "2025-04-01", "vote_average": 9.8, 
         "overview": "A top rated TV show", "poster_path": "/toprated.jpg", "genre_ids": [18]}
    ]}
    mock_genres.return_value = [
        {"id": 18, "name": "Drame"}
    ]
    
    response = self.app.get('/top-rated-tv')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'S\xc3\xa9ries TV les mieux not\xc3\xa9es', response.data)
    self.assertIn(b'Top Rated TV Show', response.data)

@patch('requests.get')
def test_get_top_rated_tv_shows(self, mock_get):
    # Mock de la réponse de l'API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"results": [{"name": "Top Rated TV Show"}]}
    mock_get.return_value = mock_response
    
    result = get_top_rated_tv_shows()
    self.assertEqual(result, {"results": [{"name": "Top Rated TV Show"}]})

@patch('requests.get')
def test_get_tv_genres(self, mock_get):
    # Mock de la réponse de l'API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"genres": [{"id": 18, "name": "Drame"}]}
    mock_get.return_value = mock_response
    
    result = get_tv_genres()
    self.assertEqual(result, [{"id": 18, "name": "Drame"}])

def test_format_tv_shows(self):
    tv_shows = [
        {"name": "Show 1", "poster_path": "/poster1.jpg", "first_air_date": "2025-04-01"},
        {"name": "Show 2", "poster_path": None, "first_air_date": "2025-04-02"}
    ]
    
    formatted_shows = format_tv_shows(tv_shows)
    
    # Vérifier que les URL d'image sont correctes
    self.assertEqual(formatted_shows[0]["poster_url"], "https://image.tmdb.org/t/p/w500/poster1.jpg")
    self.assertEqual(formatted_shows[1]["poster_url"], "/static/no-poster.jpg")
    
    # Vérifier que les champs title et release_date ont été ajoutés
    self.assertEqual(formatted_shows[0]["title"], "Show 1")
    self.assertEqual(formatted_shows[0]["release_date"], "2025-04-01")

if __name__ == '__main__':
    unittest.main()
