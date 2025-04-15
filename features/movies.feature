# features/movies.feature
Feature: Movie App Functionality
  As a user of the movie application
  I want to browse and search for movies
  So that I can find information about films currently in theaters or popular ones

  Scenario: View the home page
    Given the application is running
    When I visit the home page
    Then I should see a welcome message
    And I should see links to "Films en salle" and "Films populaires"

  Scenario: View movies currently in theaters
    Given the application is running
    When I visit the "now-playing" page
    Then I should see the title "Films actuellement au cinéma"
    And I should see a list of movies

  Scenario: View popular movies
    Given the application is running
    When I visit the "popular" page
    Then I should see the title "Films populaires"
    And I should see a list of movies

  Scenario: Search for a movie
    Given the application is running
    When I search for "Avengers"
    Then I should see search results
    And the results should contain "Avengers" related movies

  Scenario: Filter movies by genre
    Given the application is running
    And I am on the "now-playing" page
    When I filter by the "Action" genre
    Then I should only see movies in the "Action" genre

  Scenario: Navigate from home to now playing
    Given the application is running
    And I am on the home page
    When I click on the "Films en salle" link
    Then I should be redirected to the "now-playing" page

  Scenario: Navigate from home to popular
    Given the application is running
    And I am on the home page
    When I click on the "Films populaires" link
    Then I should be redirected to the "popular" page

  # Remplacer le scénario "View popular movies" dans features/movies.feature
  Scenario: View top rated TV shows
    Given the application is running
    When I visit the "top-rated-tv" page
    Then I should see the title "Séries TV les mieux notées"
    And I should see a list of TV shows

  # Remplacer le scénario "Navigate from home to popular" dans features/movies.feature
  Scenario: Navigate from home to top rated TV
    Given the application is running
    And I am on the home page
    When I click on the "Séries TV les mieux notées" link
    Then I should be redirected to the "top-rated-tv" page