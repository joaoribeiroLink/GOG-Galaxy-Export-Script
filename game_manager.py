#!/usr/bin/env python3
"""
Game Manager - A tool to manage your game collection
Features:
- Add new games to your collection
- Randomly select a game to play
- Move played games to a separate file
- Backup and restore played games when refreshing from Galaxy
"""

import csv
import random
import os
import sys
import subprocess
from datetime import datetime

class GameManager:
    def __init__(self, game_db_file="gameDB.csv", played_file="Played_game.csv", backup_file="gameDB_backup.csv"):
        self.game_db_file = game_db_file
        self.played_file = played_file
        self.backup_file = backup_file
        self.headers = []
        
    def load_headers(self):
        """Load the CSV headers from the game database"""
        try:
            with open(self.game_db_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='\t')
                self.headers = next(reader)
                return True
        except FileNotFoundError:
            print(f"Error: {self.game_db_file} not found!")
            return False
        except Exception as e:
            print(f"Error loading headers: {e}")
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
            print(f"Error: {self.game_db_file} not found!")
        except Exception as e:
            print(f"Error reading games: {e}")
        return games
    
    def write_games(self, games):
        """Write games back to the database"""
        try:
            with open(self.game_db_file, 'w', encoding='utf-8', newline='') as file:
                if games:
                    writer = csv.DictWriter(file, fieldnames=self.headers, delimiter='\t')
                    writer.writeheader()
                    writer.writerows(games)
                else:
                    # If no games left, just write headers
                    writer = csv.writer(file, delimiter='\t')
                    writer.writerow(self.headers)
            return True
        except Exception as e:
            print(f"Error writing games: {e}")
            return False
    
    def backup_current_db(self):
        """Create a backup of the current game database"""
        try:
            with open(self.game_db_file, 'r', encoding='utf-8') as src:
                with open(self.backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print(f"[OK] Backup created: {self.backup_file}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to create backup: {e}")
            return False
    
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
                print(f"[WARNING] Could not read played games file: {e}")
        return played_titles
    
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
    
    def refresh_from_galaxy(self):
        """Run the Galaxy export script to refresh the game database"""
        print("\n--- Refresh from GOG Galaxy ---")
        
        # Check if galaxy export script exists
        if not os.path.exists("galaxy_library_export.py"):
            print("[ERROR] galaxy_library_export.py not found in current directory!")
            return False
        
        # Create backup first
        if os.path.exists(self.game_db_file):
            print("[INFO] Creating backup of current database...")
            if not self.backup_current_db():
                return False
        
        # Get played games to preserve them later
        played_games = []
        if os.path.exists(self.played_file):
            try:
                with open(self.played_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter='\t')
                    played_games = list(reader)
                print(f"[INFO] Found {len(played_games)} played games to preserve")
            except Exception as e:
                print(f"[WARNING] Could not read played games file: {e}")
        
        print("[INFO] Running Galaxy export script...")
        try:
            # Run the galaxy export script
            result = subprocess.run([sys.executable, "galaxy_library_export.py"], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("[OK] Galaxy export completed successfully!")
                print(f"[INFO] Fresh collection loaded with all games from Galaxy")
                
                # Note: We don't remove played games from the main collection anymore
                # They stay in gameDB.csv, but the randomizer will filter them out
                if played_games:
                    print(f"[INFO] {len(played_games)} played games will be filtered from random selection")
                
                return True
            else:
                print(f"[ERROR] Galaxy export failed:")
                print(f"Error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("[ERROR] Galaxy export timed out (took longer than 2 minutes)")
            return False
        except Exception as e:
            print(f"[ERROR] Error running Galaxy export: {e}")
            return False
    
    def add_played_game(self, game):
        """Add a game to the played games file (but keep it in main collection)"""
        try:
            file_exists = os.path.exists(self.played_file)
            with open(self.played_file, 'a', encoding='utf-8', newline='') as file:
                # Add a timestamp for when the game was played
                game['playedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                if not file_exists:
                    # Create headers for new file (original headers + playedDate)
                    played_headers = self.headers + ['playedDate']
                    writer = csv.DictWriter(file, fieldnames=played_headers, delimiter='\t')
                    writer.writeheader()
                    writer.writerow(game)
                else:
                    # Just append the game data
                    # Need to get existing headers first
                    with open(self.played_file, 'r', encoding='utf-8') as read_file:
                        reader = csv.reader(read_file, delimiter='\t')
                        existing_headers = next(reader)
                    
                    writer = csv.DictWriter(file, fieldnames=existing_headers, delimiter='\t')
                    writer.writerow(game)
            return True
        except Exception as e:
            print(f"Error adding played game: {e}")
            return False
    
    def add_new_game(self):
        """Interactive function to add a new game"""
        print("\n--- Add New Game ---")
        print("[INFO] Note: Manually added games will be overwritten when you refresh from Galaxy.")
        print("      Consider adding games directly in GOG Galaxy instead.")
        
        confirm = input("Do you still want to add a game manually? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Operation cancelled.")
            return False
        
        # Create a new game entry with basic info
        new_game = {}
        
        # Get essential information
        title = input("Enter game title: ").strip()
        if not title:
            print("Game title is required!")
            return False
        
        new_game['title'] = title
        new_game['originalTitle'] = input(f"Enter original title (or press Enter for '{title}'): ").strip() or title
        new_game['sortingTitle'] = input(f"Enter sorting title (or press Enter for '{title}'): ").strip() or title
        new_game['summary'] = input("Enter game summary/description: ").strip()
        new_game['platformList'] = input("Enter platform(s) (e.g., 'Steam', 'Epic Games Store'): ").strip()
        new_game['genres'] = input("Enter genre(s) (e.g., 'Action', 'Adventure', 'RPG'): ").strip()
        new_game['developers'] = input("Enter developer(s): ").strip()
        new_game['publishers'] = input("Enter publisher(s): ").strip()
        new_game['releaseDate'] = input("Enter release date (YYYY-MM-DD): ").strip()
        new_game['originalReleaseDate'] = new_game['releaseDate']
        
        # Fill in other fields with defaults
        for header in self.headers:
            if header not in new_game:
                new_game[header] = ''
        
        # Load existing games and add new one
        games = self.read_games()
        games.append(new_game)
        
        if self.write_games(games):
            print(f"[OK] Successfully added '{title}' to your game collection!")
            return True
        else:
            print("[ERROR] Failed to add the game.")
            return False
    
    def pick_random_game(self):
        """Pick a random game from unplayed games and mark it as played"""
        unplayed_games = self.get_unplayed_games()
        
        if not unplayed_games:
            total_games = len(self.read_games())
            played_games = len(self.get_played_game_titles())
            print("[COMPLETE] Congratulations! You've played all games in your collection!")
            print(f"Total games: {total_games}")
            print(f"Played games: {played_games}")
            print("You can refresh from Galaxy to get new games, or replay some games!")
            return False
        
        print(f"\n--- Random Game Picker ---")
        total_games = len(self.read_games())
        played_count = len(self.get_played_game_titles())
        print(f"Total games in collection: {total_games}")
        print(f"Unplayed games available: {len(unplayed_games)}")
        print(f"Already played: {played_count}")
        
        # Pick a random game from unplayed games
        random_game = random.choice(unplayed_games)
        
        print(f"\n[SELECTED] Randomly selected game:")
        print(f"Title: {random_game.get('title', 'Unknown')}")
        print(f"Platform: {random_game.get('platformList', 'Unknown')}")
        print(f"Genre: {random_game.get('genres', 'Unknown')}")
        print(f"Developer: {random_game.get('developers', 'Unknown')}")
        if random_game.get('summary'):
            # Show first 200 characters of summary
            summary = random_game['summary'][:200] + "..." if len(random_game['summary']) > 200 else random_game['summary']
            print(f"Summary: {summary}")
        
        # Confirm if user wants to mark this as played
        choice = input(f"\nDo you want to mark '{random_game['title']}' as played? (y/n): ").strip().lower()
        
        if choice == 'y' or choice == 'yes':
            # Add to played games (but keep in main collection)
            if self.add_played_game(random_game):
                print(f"[OK] '{random_game['title']}' has been marked as played!")
                print(f"[INFO] Game remains in your collection but won't be selected again")
                print(f"Unplayed games remaining: {len(unplayed_games) - 1}")
                return True
            else:
                print("[ERROR] Failed to mark game as played.")
                return False
        else:
            print("Game selection cancelled.")
            return False
    
    def show_stats(self):
        """Show statistics about the game collection"""
        all_games = self.read_games()
        played_titles = self.get_played_game_titles()
        unplayed_games = self.get_unplayed_games()
        
        print(f"\n--- Game Collection Statistics ---")
        print(f"Total games in collection: {len(all_games)}")
        print(f"Played games: {len(played_titles)}")
        print(f"Unplayed games: {len(unplayed_games)}")
        
        if len(all_games) > 0:
            completion_percentage = (len(played_titles) / len(all_games)) * 100
            print(f"Collection completion: {completion_percentage:.1f}%")
        
        # Show backup info
        if os.path.exists(self.backup_file):
            backup_time = datetime.fromtimestamp(os.path.getmtime(self.backup_file))
            print(f"Last backup: {backup_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if all_games:
            # Show genre distribution (for all games)
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
            
            if genres:
                print(f"\nTop 5 genres in collection:")
                sorted_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)[:5]
                for genre, count in sorted_genres:
                    print(f"  {genre}: {count}")
            
            if platforms:
                print(f"\nTop 5 platforms in collection:")
                sorted_platforms = sorted(platforms.items(), key=lambda x: x[1], reverse=True)[:5]
                for platform, count in sorted_platforms:
                    print(f"  {platform}: {count}")
    
    def search_games(self):
        """Search for games in the collection"""
        all_games = self.read_games()
        played_titles = self.get_played_game_titles()
        
        if not all_games:
            print("[ERROR] No games in your collection!")
            return
        
        search_term = input("\nEnter search term (title, genre, platform, etc.): ").strip().lower()
        
        if not search_term:
            print("[ERROR] Search term cannot be empty!")
            return
        
        matches = []
        for game in all_games:
            # Search in multiple fields
            searchable_text = f"{game.get('title', '')} {game.get('genres', '')} {game.get('platformList', '')} {game.get('developers', '')} {game.get('summary', '')}".lower()
            if search_term in searchable_text:
                matches.append(game)
        
        if matches:
            print(f"\n[FOUND] Found {len(matches)} matching games:")
            for i, game in enumerate(matches, 1):
                title = game.get('title', 'Unknown')
                platform = game.get('platformList', 'Unknown')
                
                # Check if this game has been played
                is_played = title.lower() in played_titles
                status = "[PLAYED]" if is_played else "[UNPLAYED]"
                
                print(f"{i}. {title} ({platform}) - {status}")
                if game.get('genres'):
                    print(f"   Genres: {game.get('genres')}")
        else:
            print(f"[NOT FOUND] No games found matching '{search_term}'")

def main():
    """Main program loop"""
    game_manager = GameManager()
    
    # Load headers
    if not game_manager.load_headers():
        print("Failed to load game database. Please make sure gameDB.csv exists.")
        print("You can create it by running: python galaxy_library_export.py")
        sys.exit(1)
    
    print("*** GAME MANAGER ***")
    print("Manage your game collection with ease!")
    
    while True:
        print("\n" + "="*50)
        print("GAME MANAGER MENU")
        print("="*50)
        print("1. [RANDOM] Pick a random game to play")
        print("2. [ADD] Add a new game to collection")
        print("3. [STATS] Show collection statistics")
        print("4. [SEARCH] Search games")
        print("5. [REFRESH] Refresh from GOG Galaxy")
        print("6. [EXIT] Exit")
        print("="*50)
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            game_manager.pick_random_game()
        elif choice == '2':
            game_manager.add_new_game()
        elif choice == '3':
            game_manager.show_stats()
        elif choice == '4':
            game_manager.search_games()
        elif choice == '5':
            game_manager.refresh_from_galaxy()
        elif choice == '6':
            print("Thanks for using Game Manager! Happy gaming!")
            break
        else:
            print("[ERROR] Invalid option. Please select 1-6.")

if __name__ == "__main__":
    main() 