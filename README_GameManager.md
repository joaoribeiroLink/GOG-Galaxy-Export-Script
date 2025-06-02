# 🎮 Game Manager

A Python program to manage your game collection! This tool helps you organize your games, pick random games to play, and track which games you've completed. **Integrated with GOG Galaxy Export Script** for seamless collection management.

## Features

- **🎲 Random Game Picker**: Randomly selects a game from your collection
- **➕ Add New Games**: Add new games to your collection (with Galaxy sync warning)
- **📊 Statistics**: View your collection statistics and breakdowns
- **🔍 Search**: Search through your game collection
- **✅ Played Games Tracking**: Move completed games to a separate file
- **🔄 Galaxy Integration**: Refresh your collection from GOG Galaxy while preserving played games
- **📋 Smart Backup**: Automatic backups when refreshing from Galaxy

## How to Use

### Prerequisites
- Python 3.x installed on your system
- Your `gameDB.csv` file in the same directory
- `galaxy_library_export.py` script in the same directory (for refresh functionality)

### Running the Program

1. **Open a terminal/command prompt** in the directory containing your files
2. **Run the program**:
   ```bash
   python game_manager.py
   ```
   
3. **Use the menu** to navigate through options:
   - Option 1: Pick a random game to play
   - Option 2: Add a new game to your collection
   - Option 3: View collection statistics
   - Option 4: Search your games
   - Option 5: Refresh from GOG Galaxy ⭐ **NEW**
   - Option 6: Exit the program

### Features Explained

#### 🎲 Random Game Picker
- Randomly selects a game from your `gameDB.csv`
- Shows game details (title, platform, genre, developer, summary)
- Asks if you want to mark it as "played"
- If confirmed, moves the game to `Played_game.csv` and removes it from your main collection

#### ➕ Add New Game
- Interactive prompts to add a new game
- **Warning**: Manually added games will be overwritten when you refresh from Galaxy
- Recommended: Add games directly in GOG Galaxy instead

#### 📊 Statistics
- Shows total games in collection
- Shows total played games
- Shows when the last backup was created
- Displays top 5 genres and platforms in your collection

#### 🔍 Search Games
- Search by game title, genre, platform, developer, or description
- Case-insensitive search
- Shows all matching results

#### 🔄 Refresh from GOG Galaxy ⭐ **NEW**
- **Automatically runs** `galaxy_library_export.py` to get latest games from your GOG Galaxy library
- **Creates backup** of current database before refresh
- **Preserves played games** - automatically removes them from the fresh export
- **Intelligent sync** - your "played" games won't reappear in your main collection

## Perfect Workflow

### Recommended Usage Pattern:

1. **🆕 New Games**: When you buy new games, they're automatically added to GOG Galaxy
2. **🔄 Refresh**: Use option 5 to refresh your collection from Galaxy (gets new games)
3. **🎲 Play**: Use option 1 to pick a random game from your updated collection
4. **✅ Complete**: Mark games as played - they move to your "completed" list
5. **🔁 Repeat**: The cycle continues seamlessly!

## Files

- **`gameDB.csv`**: Your main game collection (synced from Galaxy)
- **`Played_game.csv`**: Games you've marked as played (preserved across syncs)
- **`gameDB_backup.csv`**: Automatic backup created during Galaxy refresh
- **`game_manager.py`**: The main program
- **`galaxy_library_export.py`**: GOG Galaxy export script (external)

## Important Notes

### 🔄 Galaxy Integration Benefits
✅ **Seamless Sync**: New games from Galaxy are automatically added  
✅ **Smart Preservation**: Played games stay in your completed list  
✅ **Automatic Backup**: Your data is protected during refreshes  
✅ **No Duplicates**: Played games won't reappear in your main collection  

### ⚠️ Important Warnings
🚨 **Manual Additions**: Games added manually (option 2) will be lost when refreshing from Galaxy  
🎯 **Game Removal**: When you mark a game as played, it's moved permanently to the played games file  
📅 **Timestamps**: Played games include a timestamp of when they were marked as played  

### 🔧 Backup & Recovery
- Automatic backups are created before Galaxy refreshes
- Backups are saved as `gameDB_backup.csv`
- You can manually restore from backup if needed

## Example Usage

```
🎮 Welcome to Game Manager!
Manage your game collection with ease!

==================================================
GAME MANAGER MENU
==================================================
1. 🎲 Pick a random game to play
2. ➕ Add a new game to collection
3. 📊 Show collection statistics
4. 🔍 Search games
5. 🔄 Refresh from GOG Galaxy
6. 🚪 Exit
==================================================
Select an option (1-6): 5

--- Refresh from GOG Galaxy ---
📋 Creating backup of current database...
✅ Backup created: gameDB_backup.csv
📝 Found 15 played games to preserve
🔄 Running Galaxy export script...
✅ Galaxy export completed successfully!
🎯 Removing previously played games from fresh export...
✅ Removed 15 previously played games
📊 Current collection: 1,129 games
```

## Perfect Integration

This Game Manager is designed to work **perfectly** with your existing `galaxy_library_export.py` script:

- **Before**: You had to manually avoid played games
- **Now**: The system automatically handles everything
- **Result**: Always have a fresh, up-to-date collection without losing track of completed games

Enjoy your perfectly managed game collection! 🎮🚀 