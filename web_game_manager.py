#!/usr/bin/env python3
"""
Web Game Manager - A beautiful web interface for managing your game collection
Features:
- Web-based interface with modern design
- All the same functionality as the command-line version
- Random game picker, statistics, search, and Galaxy sync
- Favorites management
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import csv
import random
import os
import subprocess
import sys
from datetime import datetime
import json
import shutil

app = Flask(__name__)

class WebGameManager:
    def __init__(self, game_db_file="gameDB.csv", played_file="Played_game.csv", backup_file="gameDB_backup.csv", favorites_file="Favorite_games.csv", want_to_play_file="Want_to_play.csv"):
        self.game_db_file = game_db_file
        self.played_file = played_file
        self.backup_file = backup_file
        self.favorites_file = favorites_file
        self.want_to_play_file = want_to_play_file
        self.headers = []
        self.load_headers()
        
    def load_headers(self):
        """Load the CSV headers from the game database"""
        try:
            with open(self.game_db_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='\t')
                self.headers = next(reader)
                return True
        except FileNotFoundError:
            self.headers = []
            return False
        except Exception as e:
            self.headers = []
            return False
    
    def read_games(self):
        """Read all games from the database"""
        games = []
        try:
            with open(self.game_db_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    games.append(row)
        except FileNotFoundError:
            pass
        except Exception as e:
            pass
        return games
    
    def get_played_game_titles(self):
        """Get a set of titles of games that have been played"""
        played_titles = set()
        if os.path.exists(self.played_file):
            try:
                with open(self.played_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter='\t')
                    for row in reader:
                        title = row.get('title', '').strip().lower()
                        if title:
                            played_titles.add(title)
            except Exception as e:
                pass
        return played_titles

    def get_favorite_game_titles(self):
        """Get a set of titles of games that have been marked as favorites"""
        favorite_titles = set()
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter='\t')
                    for row in reader:
                        title = row.get('title', '').strip().lower()
                        if title:
                            favorite_titles.add(title)
            except Exception as e:
                pass
        return favorite_titles
    
    def get_played_games(self):
        """Get all games that have been played with their metadata"""
        played_games = []
        if os.path.exists(self.played_file):
            try:
                with open(self.played_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter='\t')
                    for row in reader:
                        played_games.append(row)
            except Exception as e:
                pass
        return played_games

    def get_favorite_games(self):
        """Get all games that have been marked as favorites with their metadata"""
        favorite_games = []
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter='\t')
                    for row in reader:
                        favorite_games.append(row)
            except Exception as e:
                pass
        return favorite_games
    
    def get_want_to_play_game_titles(self):
        """Get a set of titles of games that have been marked as want to play"""
        want_to_play_titles = set()
        if os.path.exists(self.want_to_play_file):
            try:
                with open(self.want_to_play_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter='\t')
                    for row in reader:
                        title = row.get('title', '').strip().lower()
                        if title:
                            want_to_play_titles.add(title)
            except Exception as e:
                pass
        return want_to_play_titles
    
    def get_want_to_play_games(self):
        """Get all games that have been marked as want to play with their metadata"""
        want_to_play_games = []
        if os.path.exists(self.want_to_play_file):
            try:
                with open(self.want_to_play_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter='\t')
                    for row in reader:
                        want_to_play_games.append(row)
            except Exception as e:
                pass
        return want_to_play_games
    
    def get_unplayed_games(self):
        """Get all games that haven't been played yet"""
        all_games = self.read_games()
        played_titles = self.get_played_game_titles()
        
        unplayed_games = []
        for game in all_games:
            title = game.get('title', '').strip().lower()
            if title not in played_titles:
                unplayed_games.append(game)
        
        return unplayed_games
    
    def add_played_game(self, game):
        """Add a game to the played games file"""
        try:
            # Define the correct headers for played games file
            played_headers = self.headers + ['playedDate']
            
            # Add a timestamp for when the game was marked as played
            game_copy = game.copy()  # Make a copy to avoid modifying the original
            game_copy['playedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Read existing games if file exists
            existing_games = []
            if os.path.exists(self.played_file):
                try:
                    with open(self.played_file, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file, delimiter='\t')
                        for row in reader:
                            existing_games.append(row)
                except Exception as e:
                    print(f"Error reading existing played games file: {e}")
                    # If file is corrupted, start fresh
                    existing_games = []
            
            # Check if game is already in the list
            game_title_lower = game_copy.get('title', '').strip().lower()
            for existing_game in existing_games:
                if existing_game.get('title', '').strip().lower() == game_title_lower:
                    return False  # Game already exists
            
            # Add the new game
            existing_games.append(game_copy)
            
            # Write all games back to file
            with open(self.played_file, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=played_headers, delimiter='\t')
                writer.writeheader()
                writer.writerows(existing_games)
                    
            return True
        except Exception as e:
            print(f"Error adding played game: {e}")  # Debug print
            return False

    def add_favorite_game(self, game):
        """Add a game to the favorites file"""
        try:
            # Define the correct headers for favorites file
            favorite_headers = self.headers + ['favoriteDate']
            
            # Add a timestamp for when the game was added to favorites
            game_copy = game.copy()  # Make a copy to avoid modifying the original
            game_copy['favoriteDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Read existing games if file exists
            existing_games = []
            if os.path.exists(self.favorites_file):
                try:
                    with open(self.favorites_file, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file, delimiter='\t')
                        for row in reader:
                            existing_games.append(row)
                except Exception as e:
                    print(f"Error reading existing favorites file: {e}")
                    # If file is corrupted, start fresh
                    existing_games = []
            
            # Check if game is already in the list
            game_title_lower = game_copy.get('title', '').strip().lower()
            for existing_game in existing_games:
                if existing_game.get('title', '').strip().lower() == game_title_lower:
                    return False  # Game already exists
            
            # Add the new game
            existing_games.append(game_copy)
            
            # Write all games back to file
            with open(self.favorites_file, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=favorite_headers, delimiter='\t')
                writer.writeheader()
                writer.writerows(existing_games)
                    
            return True
        except Exception as e:
            print(f"Error adding favorite game: {e}")  # Debug print
            return False
    
    def add_want_to_play_game(self, game):
        """Add a game to the want to play file"""
        try:
            # Add a timestamp for when the game was added to want to play
            game_copy = game.copy()  # Make a copy to avoid modifying the original
            game_copy['wantToPlayDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Define the correct headers for want to play file
            want_to_play_headers = self.headers + ['wantToPlayDate']
            
            # Read existing games if file exists
            existing_games = []
            if os.path.exists(self.want_to_play_file):
                try:
                    with open(self.want_to_play_file, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file, delimiter='\t')
                        for row in reader:
                            existing_games.append(row)
                except Exception as e:
                    print(f"Error reading existing want to play file: {e}")
                    # If file is corrupted, start fresh
                    existing_games = []
            
            # Check if game is already in the list
            game_title_lower = game_copy.get('title', '').strip().lower()
            for existing_game in existing_games:
                if existing_game.get('title', '').strip().lower() == game_title_lower:
                    return False  # Game already exists
            
            # Add the new game
            existing_games.append(game_copy)
            
            # Write all games back to file
            with open(self.want_to_play_file, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=want_to_play_headers, delimiter='\t')
                writer.writeheader()
                writer.writerows(existing_games)
                    
            return True
        except Exception as e:
            print(f"Error adding want to play game: {e}")  # Debug print
            return False
    
    def remove_played_game(self, game_title):
        """Remove a game from the played games file"""
        if not os.path.exists(self.played_file):
            return False
        
        try:
            # Read all played games
            played_games = []
            with open(self.played_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                headers = reader.fieldnames
                for row in reader:
                    if row.get('title', '').strip().lower() != game_title.lower():
                        played_games.append(row)
            
            # Rewrite the file without the specified game
            with open(self.played_file, 'w', encoding='utf-8', newline='') as file:
                if headers and played_games:
                    writer = csv.DictWriter(file, fieldnames=headers, delimiter='\t')
                    writer.writeheader()
                    writer.writerows(played_games)
                elif headers:
                    # If no games left, still write headers
                    writer = csv.DictWriter(file, fieldnames=headers, delimiter='\t')
                    writer.writeheader()
            
            return True
        except Exception as e:
            return False

    def remove_favorite_game(self, game_title):
        """Remove a game from the favorites file"""
        if not os.path.exists(self.favorites_file):
            return False
        
        try:
            # Read all favorite games
            favorite_games = []
            with open(self.favorites_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                headers = reader.fieldnames
                for row in reader:
                    if row.get('title', '').strip().lower() != game_title.lower():
                        favorite_games.append(row)
            
            # Rewrite the file without the specified game
            with open(self.favorites_file, 'w', encoding='utf-8', newline='') as file:
                if headers and favorite_games:
                    writer = csv.DictWriter(file, fieldnames=headers, delimiter='\t')
                    writer.writeheader()
                    writer.writerows(favorite_games)
                elif headers:
                    # If no games left, still write headers
                    writer = csv.DictWriter(file, fieldnames=headers, delimiter='\t')
                    writer.writeheader()
            
            return True
        except Exception as e:
            return False
    
    def remove_want_to_play_game(self, game_title):
        """Remove a game from the want to play file"""
        if not os.path.exists(self.want_to_play_file):
            return False
        
        try:
            # Read all want to play games
            want_to_play_games = []
            with open(self.want_to_play_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                headers = reader.fieldnames
                for row in reader:
                    if row.get('title', '').strip().lower() != game_title.lower():
                        want_to_play_games.append(row)
            
            # Rewrite the file without the specified game
            with open(self.want_to_play_file, 'w', encoding='utf-8', newline='') as file:
                if headers and want_to_play_games:
                    writer = csv.DictWriter(file, fieldnames=headers, delimiter='\t')
                    writer.writeheader()
                    writer.writerows(want_to_play_games)
                elif headers:
                    # If no games left, still write headers
                    writer = csv.DictWriter(file, fieldnames=headers, delimiter='\t')
                    writer.writeheader()
            
            return True
        except Exception as e:
            return False
    
    def update_game_rating(self, game_title, rating):
        """Update the personal rating for a game (0-100)"""
        try:
            # Read all games
            games = []
            with open(self.game_db_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                headers = reader.fieldnames
                for row in reader:
                    if row.get('title', '').strip() == game_title.strip():
                        row['myRating'] = str(rating) if rating is not None else ''
                    games.append(row)
            
            # Write back to file
            with open(self.game_db_file, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers, delimiter='\t')
                writer.writeheader()
                writer.writerows(games)
            
            return True
        except Exception as e:
            return False
    
    def get_game_details(self, game_title):
        """Get detailed information for a specific game"""
        all_games = self.read_games()
        for game in all_games:
            if game.get('title', '').strip() == game_title.strip():
                # Add some formatted data
                game['formatted_rating'] = self.format_rating(game.get('myRating', ''))
                game['formatted_critic_score'] = self.format_critic_score(game.get('criticsScore', ''))
                return game
        return None
    
    def format_rating(self, rating):
        """Format personal rating for display"""
        if not rating or rating == '':
            return 'Not Rated'
        try:
            rating_num = int(rating)
            if 0 <= rating_num <= 100:
                return f"{rating_num}/100"
            else:
                return 'Invalid Rating'
        except ValueError:
            return 'Invalid Rating'
    
    def format_critic_score(self, score):
        """Format critic score for display"""
        if not score or score == '':
            return 'No Score'
        try:
            score_num = int(score)
            return f"{score_num}/100"
        except ValueError:
            return 'No Score'
    
    def get_stats(self):
        """Get collection statistics"""
        all_games = self.read_games()
        played_titles = self.get_played_game_titles()
        favorite_titles = self.get_favorite_game_titles()
        unplayed_games = self.get_unplayed_games()
        
        # Calculate rating statistics
        personal_ratings = []
        critic_scores = []
        
        for game in all_games:
            # Personal ratings
            my_rating = game.get('myRating', '')
            if my_rating and my_rating != '':
                try:
                    rating_num = int(my_rating)
                    if 0 <= rating_num <= 100:
                        personal_ratings.append(rating_num)
                except ValueError:
                    pass
            
            # Critic scores
            critic_score = game.get('criticsScore', '')
            if critic_score and critic_score != '':
                try:
                    score_num = int(critic_score)
                    critic_scores.append(score_num)
                except ValueError:
                    pass
        
        stats = {
            'total_games': len(all_games),
            'played_games': len(played_titles),
            'favorite_games': len(favorite_titles),
            'unplayed_games': len(unplayed_games),
            'completion_percentage': (len(played_titles) / len(all_games) * 100) if len(all_games) > 0 else 0,
            'last_backup': None,
            'rated_games': len(personal_ratings),
            'average_personal_rating': sum(personal_ratings) / len(personal_ratings) if personal_ratings else 0,
            'average_critic_score': sum(critic_scores) / len(critic_scores) if critic_scores else 0,
            'highest_rated_personal': max(personal_ratings) if personal_ratings else 0,
            'lowest_rated_personal': min(personal_ratings) if personal_ratings else 0
        }
        
        # Get backup info
        if os.path.exists(self.backup_file):
            backup_time = datetime.fromtimestamp(os.path.getmtime(self.backup_file))
            stats['last_backup'] = backup_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Get genre and platform distribution
        genres = {}
        platforms = {}
        
        for game in all_games:
            # Count genres
            game_genres = game.get('genres', '').split()
            for genre in game_genres:
                genre = genre.strip('",')
                if genre:
                    genres[genre] = genres.get(genre, 0) + 1
            
            # Count platforms
            game_platforms = game.get('platformList', '').split()
            for platform in game_platforms:
                platform = platform.strip('",')
                if platform:
                    platforms[platform] = platforms.get(platform, 0) + 1
        
        stats['top_genres'] = sorted(genres.items(), key=lambda x: x[1], reverse=True)[:5]
        stats['top_platforms'] = sorted(platforms.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return stats
    
    def search_games(self, search_term):
        """Search for games in the collection"""
        all_games = self.read_games()
        played_titles = self.get_played_game_titles()
        favorite_titles = self.get_favorite_game_titles()
        want_to_play_titles = self.get_want_to_play_game_titles()
        
        matches = []
        search_lower = search_term.lower()
        
        for game in all_games:
            # Search in multiple fields
            title = game.get('title', '').lower()
            genres = game.get('genres', '').lower()
            platforms = game.get('platformList', '').lower()
            developers = game.get('developers', '').lower()
            publishers = game.get('publishers', '').lower()
            summary = game.get('summary', '').lower()
            themes = game.get('themes', '').lower()
            
            if (search_lower in title or 
                search_lower in genres or 
                search_lower in platforms or 
                search_lower in developers or
                search_lower in publishers or
                search_lower in summary or
                search_lower in themes):
                
                # Add played, favorite, and want to play status
                game_title_lower = game.get('title', '').strip().lower()
                game['is_played'] = game_title_lower in played_titles
                game['is_favorite'] = game_title_lower in favorite_titles
                game['is_want_to_play'] = game_title_lower in want_to_play_titles
                
                matches.append(game)
        
        return matches
    
    def refresh_from_galaxy(self):
        """Run the Galaxy export script to refresh the game database"""
        if not os.path.exists("galaxy_library_export.py"):
            return False, "galaxy_library_export.py not found"
        
        try:
            result = subprocess.run([sys.executable, "galaxy_library_export.py"], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                self.load_headers()  # Reload headers after refresh
                return True, "Galaxy export completed successfully"
            else:
                return False, f"Galaxy export failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "Galaxy export timed out"
        except Exception as e:
            return False, f"Error running Galaxy export: {str(e)}"

# Initialize the game manager
manager = WebGameManager()

@app.route('/', endpoint='index')
def dashboard():
    """Dashboard showing collection overview"""
    stats = manager.get_stats()
    return render_template('index.html', stats=stats)

@app.route('/random')
def random_game():
    """Random game picker page"""
    return render_template('random.html')

@app.route('/search')
def search():
    """Search page"""
    return render_template('search.html')

@app.route('/played')
def played_games():
    """Played games page"""
    return render_template('played.html')

@app.route('/all-games')
def all_games():
    """All games page"""
    return render_template('all_games.html')

@app.route('/unplayed')
def unplayed_games():
    """Unplayed games page"""
    return render_template('unplayed_games.html')

@app.route('/favorites')
def favorites():
    """Favorites page"""
    return render_template('favorites.html')

@app.route('/want-to-play')
def want_to_play():
    """Want to play page"""
    return render_template('want_to_play.html')

@app.route('/api/random-game')
def api_random_game():
    """API endpoint to get a random unplayed game"""
    unplayed_games = manager.get_unplayed_games()
    
    if not unplayed_games:
        return jsonify({
            'success': False,
            'message': 'No unplayed games available!'
        })
    
    random_game = random.choice(unplayed_games)
    
    # Format game data for frontend
    game_data = {
        'title': random_game.get('title', 'Unknown'),
        'platform': random_game.get('platformList', 'Unknown'),
        'genre': random_game.get('genres', 'Unknown'),
        'developer': random_game.get('developers', 'Unknown'),
        'summary': random_game.get('summary', 'No description available.'),
        'vertical_cover': random_game.get('verticalCover', ''),
        'square_icon': random_game.get('squareIcon', ''),
        'my_rating': random_game.get('myRating', ''),
        'critics_score': random_game.get('criticsScore', '')
    }
    
    return jsonify({
        'success': True,
        'game': game_data,
        'remaining': len(unplayed_games) - 1
    })

@app.route('/api/random-want-to-play-game')
def api_random_want_to_play_game():
    """API endpoint to get a random want to play game"""
    want_to_play_games = manager.get_want_to_play_games()
    
    if not want_to_play_games:
        return jsonify({
            'success': False,
            'message': 'No want to play games available!'
        })
    
    random_game = random.choice(want_to_play_games)
    
    # Format game data for frontend
    game_data = {
        'title': random_game.get('title', 'Unknown'),
        'platform': random_game.get('platformList', 'Unknown'),
        'genre': random_game.get('genres', 'Unknown'),
        'developer': random_game.get('developers', 'Unknown'),
        'summary': random_game.get('summary', 'No description available.'),
        'vertical_cover': random_game.get('verticalCover', ''),
        'square_icon': random_game.get('squareIcon', ''),
        'my_rating': random_game.get('myRating', ''),
        'critics_score': random_game.get('criticsScore', '')
    }
    
    return jsonify({
        'success': True,
        'game': game_data,
        'remaining': len(want_to_play_games) - 1
    })

@app.route('/api/played-games')
def api_played_games():
    """API endpoint to get all played games"""
    try:
        played_games = manager.get_played_games()
        return jsonify({
            'success': True,
            'games': played_games
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading played games: {str(e)}'
        })

@app.route('/api/favorite-games')
def api_favorite_games():
    """API endpoint to get all favorite games"""
    try:
        favorite_games = manager.get_favorite_games()
        return jsonify({
            'success': True,
            'games': favorite_games
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading favorite games: {str(e)}'
        })

@app.route('/api/want-to-play-games')
def api_want_to_play_games():
    """API endpoint to get all want to play games"""
    try:
        want_to_play_games = manager.get_want_to_play_games()
        return jsonify({
            'success': True,
            'games': want_to_play_games
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading want to play games: {str(e)}'
        })

@app.route('/api/all-games')
def api_all_games():
    """API endpoint to get all games"""
    try:
        all_games = manager.read_games()
        played_titles = manager.get_played_game_titles()
        favorite_titles = manager.get_favorite_game_titles()
        want_to_play_titles = manager.get_want_to_play_game_titles()
        
        # Add played, favorite, and want to play status to each game
        for game in all_games:
            game_title_lower = game.get('title', '').strip().lower()
            game['is_played'] = game_title_lower in played_titles
            game['is_favorite'] = game_title_lower in favorite_titles
            game['is_want_to_play'] = game_title_lower in want_to_play_titles
            
        return jsonify({
            'success': True,
            'games': all_games
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading games: {str(e)}'
        })

@app.route('/api/unplayed-games')
def api_unplayed_games():
    """API endpoint to get unplayed games"""
    try:
        unplayed_games = manager.get_unplayed_games()
        return jsonify({
            'success': True,
            'games': unplayed_games
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading unplayed games: {str(e)}'
        })

@app.route('/api/mark-played', methods=['POST'])
def api_mark_played():
    """API endpoint to mark a game as played"""
    data = request.get_json()
    game_title = data.get('title')
    
    # Find the game in the database
    all_games = manager.read_games()
    target_game = None
    
    for game in all_games:
        if game.get('title', '').strip().lower() == game_title.lower():
            target_game = game
            break
    
    if target_game:
        if manager.add_played_game(target_game):
            return jsonify({'success': True, 'message': f'{game_title} marked as played!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to mark game as played'})
    else:
        return jsonify({'success': False, 'message': 'Game not found'})

@app.route('/api/mark-unplayed', methods=['POST'])
def api_mark_unplayed():
    """API endpoint to mark a game as unplayed (remove from played list)"""
    data = request.get_json()
    game_title = data.get('title')
    
    if manager.remove_played_game(game_title):
        return jsonify({'success': True, 'message': f'{game_title} marked as unplayed!'})
    else:
        return jsonify({'success': False, 'message': 'Failed to mark game as unplayed'})

@app.route('/api/mark-favorite', methods=['POST'])
def api_mark_favorite():
    """API endpoint to mark a game as favorite"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
            
        game_title = data.get('title')
        if not game_title:
            return jsonify({'success': False, 'message': 'Game title is required'})
        
        print(f"Attempting to add '{game_title}' to favorites")  # Debug
        
        # Find the game in the database
        all_games = manager.read_games()
        target_game = None
        
        for game in all_games:
            if game.get('title', '').strip().lower() == game_title.strip().lower():
                target_game = game
                break
        
        if not target_game:
            print(f"Game '{game_title}' not found in database")  # Debug
            return jsonify({'success': False, 'message': f'Game "{game_title}" not found in database'})
        
        # Check if already a favorite
        favorite_titles = manager.get_favorite_game_titles()
        if game_title.strip().lower() in favorite_titles:
            return jsonify({'success': False, 'message': f'{game_title} is already in favorites'})
        
        # Try to add to favorites
        success = manager.add_favorite_game(target_game)
        if success:
            print(f"Successfully added '{game_title}' to favorites")  # Debug
            return jsonify({'success': True, 'message': f'{game_title} added to favorites!'})
        else:
            print(f"Failed to add '{game_title}' to favorites")  # Debug
            return jsonify({'success': False, 'message': 'Failed to add game to favorites - check file permissions'})
            
    except Exception as e:
        print(f"Exception in mark-favorite: {e}")  # Debug
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'})

@app.route('/api/mark-unfavorite', methods=['POST'])
def api_mark_unfavorite():
    """API endpoint to mark a game as unfavorite (remove from favorites list)"""
    data = request.get_json()
    game_title = data.get('title')
    
    if manager.remove_favorite_game(game_title):
        return jsonify({'success': True, 'message': f'{game_title} removed from favorites!'})
    else:
        return jsonify({'success': False, 'message': 'Failed to remove game from favorites'})

@app.route('/api/mark-want-to-play', methods=['POST'])
def api_mark_want_to_play():
    """API endpoint to mark a game as want to play"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
            
        game_title = data.get('title')
        if not game_title:
            return jsonify({'success': False, 'message': 'Game title is required'})
        
        print(f"Attempting to add '{game_title}' to want to play")  # Debug
        
        # Find the game in the database
        all_games = manager.read_games()
        target_game = None
        
        for game in all_games:
            if game.get('title', '').strip().lower() == game_title.strip().lower():
                target_game = game
                break
        
        if not target_game:
            print(f"Game '{game_title}' not found in database")  # Debug
            return jsonify({'success': False, 'message': f'Game "{game_title}" not found in database'})
        
        # Check if already in want to play
        want_to_play_titles = manager.get_want_to_play_game_titles()
        if game_title.strip().lower() in want_to_play_titles:
            return jsonify({'success': False, 'message': f'{game_title} is already in want to play list'})
        
        # Try to add to want to play
        success = manager.add_want_to_play_game(target_game)
        if success:
            print(f"Successfully added '{game_title}' to want to play")  # Debug
            return jsonify({'success': True, 'message': f'{game_title} added to want to play list!'})
        else:
            print(f"Failed to add '{game_title}' to want to play")  # Debug
            return jsonify({'success': False, 'message': 'Failed to add game to want to play list - check file permissions'})
            
    except Exception as e:
        print(f"Exception in mark-want-to-play: {e}")  # Debug
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'})

@app.route('/api/mark-unwant-to-play', methods=['POST'])
def api_mark_unwant_to_play():
    """API endpoint to mark a game as not want to play (remove from want to play list)"""
    data = request.get_json()
    game_title = data.get('title')
    
    if manager.remove_want_to_play_game(game_title):
        return jsonify({'success': True, 'message': f'{game_title} removed from want to play list!'})
    else:
        return jsonify({'success': False, 'message': 'Failed to remove game from want to play list'})

@app.route('/api/search')
def api_search():
    """API endpoint for game search"""
    search_term = request.args.get('q', '')
    
    if not search_term:
        return jsonify({'success': False, 'message': 'Search term required'})
    
    matches = manager.search_games(search_term)
    
    return jsonify({
        'success': True,
        'matches': matches,
        'count': len(matches)
    })

@app.route('/stats')
def stats():
    """Statistics page"""
    stats_data = manager.get_stats()
    return render_template('stats.html', stats=stats_data)

@app.route('/api/refresh-galaxy', methods=['POST'])
def api_refresh_galaxy():
    """Refresh game database from Galaxy export"""
    try:
        success = manager.refresh_from_galaxy()
        if success:
            return jsonify({
                'success': True,
                'message': 'Galaxy database refreshed successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to refresh from Galaxy export'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

# New rating endpoints
@app.route('/api/rate-game', methods=['POST'])
def api_rate_game():
    """Update the personal rating for a game"""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        rating = data.get('rating')
        
        if not title:
            return jsonify({
                'success': False,
                'message': 'Game title is required'
            })
        
        # Validate rating
        if rating is not None:
            try:
                rating_num = int(rating)
                if not (0 <= rating_num <= 100):
                    return jsonify({
                        'success': False,
                        'message': 'Rating must be between 0 and 100'
                    })
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Rating must be a valid number'
                })
        
        success = manager.update_game_rating(title, rating)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Rating updated successfully!' if rating is not None else 'Rating cleared successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to update rating'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/api/game-details/<path:game_title>')
def api_game_details(game_title):
    """Get detailed information for a specific game"""
    try:
        game = manager.get_game_details(game_title)
        
        if game:
            # Format game data for display
            game_data = {
                'title': game.get('title', 'Unknown'),
                'platform': game.get('platformList', 'Unknown'),
                'genre': game.get('genres', 'Unknown'),
                'developer': game.get('developers', 'Unknown'),
                'publisher': game.get('publishers', 'Unknown'),
                'summary': game.get('summary', 'No description available.'),
                'vertical_cover': game.get('verticalCover', ''),
                'square_icon': game.get('squareIcon', ''),
                'background_image': game.get('backgroundImage', ''),
                'release_date': game.get('releaseDate', 'Unknown'),
                'my_rating': game.get('myRating', ''),
                'critics_score': game.get('criticsScore', ''),
                'formatted_rating': game.get('formatted_rating', 'Not Rated'),
                'formatted_critic_score': game.get('formatted_critic_score', 'No Score'),
                'themes': game.get('themes', ''),
                'tags': game.get('tags', '')
            }
            
            return jsonify({
                'success': True,
                'game': game_data
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Game not found'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

if __name__ == '__main__':
    print("🌐 Starting Web Game Manager...")
    print("📂 Game database:", "Found" if os.path.exists("gameDB.csv") else "Not found")
    print("🎮 Opening web interface at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 