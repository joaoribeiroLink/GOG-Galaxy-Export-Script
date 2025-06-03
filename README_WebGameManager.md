# 🌐 Web Game Manager

A beautiful web-based interface for managing your GOG Galaxy game collection!

## ✨ Features

### 🎯 **Dashboard**
- Beautiful overview of your entire collection
- Statistics cards with total, played, unplayed, and favorite games
- Animated progress bars showing completion percentage
- Top genres and platforms visualization
- Quick action buttons

### 🎲 **Random Game Picker**
- Interactive game cards with covers and descriptions
- One-click random selection from unplayed games
- Mark games as played directly from the interface
- Automatic counter of remaining unplayed games
- Beautiful game imagery and metadata display

### ⭐ **Favorites Management**
- Mark your favorite games with a single click
- Dedicated favorites page with filtering and sorting
- View favorite games alongside played/unplayed status
- Remove games from favorites easily
- Track when games were added to favorites

### 🔍 **Smart Search**
- Search across titles, genres, platforms, and developers
- Real-time results with played/unplayed status indicators
- Mark games as played or add to favorites from search results
- Responsive card-based layout

### 📊 **Detailed Statistics**
- Comprehensive collection analytics
- Genre and platform distribution charts
- Completion analysis with progress tracking
- Favorites tracking and statistics
- Achievement-style progress indicators
- System information and sync status

### 🔄 **Galaxy Integration**
- One-click sync with GOG Galaxy
- Automatic backup creation during sync
- Real-time sync status notifications
- Preserves played game history and favorites across syncs

## 🚀 Getting Started

### Quick Start
1. **Launch the web interface:**
   ```
   Double-click: run_web_game_manager.bat
   ```

2. **Open in your browser:**
   ```
   http://localhost:5000
   ```

3. **Start managing your games!**

### Manual Installation
If you prefer to run manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the web server
python web_game_manager.py
```

## 🎮 How to Use

### **Dashboard**
- View your collection statistics at a glance
- Click "Pick Random Game" for instant game selection
- Click "Search Games" to find specific titles
- Use "Sync Galaxy" to refresh your collection

### **Random Game Picker**
- Click "Pick Random Game" to get a random unplayed game
- View game details including platform, genre, and description
- Click "Mark as Played" to add to your completed list
- Click "Pick Another" to get a different random selection

### **Favorites Management**
- Click the star button on any game to add it to favorites
- Visit the "Favorites" page to view all your favorite games
- Filter and sort favorites by title, genre, platform, or added date
- Remove games from favorites using the "Remove Favorite" button
- Track both played and unplayed favorites

### **Search**
- Type any keyword to search your collection
- Search works across all game metadata
- See [PLAYED] or [UNPLAYED] status for each game
- Mark unplayed games as completed directly from results
- Add or remove games from favorites from search results

### **Statistics**
- View detailed collection analytics
- See top genres and platforms
- Track your completion progress
- Monitor system status and last sync time

## 🎨 Beautiful Interface

### **Modern Design**
- Dark theme optimized for gaming
- Bootstrap 5 with custom styling
- Smooth animations and transitions
- Responsive design for all devices

### **Interactive Elements**
- Hover effects on cards and buttons
- Loading spinners and progress animations
- Toast notifications for actions
- Keyboard shortcuts support

### **Game Display**
- High-quality game cover images
- Fallback placeholders for missing images
- Rich metadata display
- Intuitive status indicators

## ⌨️ Keyboard Shortcuts

- **Ctrl+Shift+R**: Refresh from Galaxy
- **/** (Forward Slash): Focus search input
- **Escape**: Clear search focus

## 🔧 Technical Features

### **Flask Web Framework**
- Fast and reliable Python backend
- RESTful API design
- JSON data exchange
- Error handling and logging

### **Modern Frontend**
- Bootstrap 5 UI framework
- Custom CSS animations
- JavaScript interactivity
- Mobile-responsive design

### **Data Management**
- Same robust CSV handling as CLI version
- Automatic backup creation
- Smart filtering for played/unplayed games
- Real-time statistics calculation

## 📁 File Structure

```
├── web_game_manager.py     # Main Flask application
├── templates/              # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Dashboard page
│   ├── random.html        # Random game picker
│   ├── search.html        # Search page
│   └── stats.html         # Statistics page
├── static/                # Static files
│   ├── css/
│   │   └── style.css      # Custom styling
│   └── js/
│       └── app.js         # JavaScript functionality
├── requirements.txt       # Python dependencies
└── run_web_game_manager.bat # Launch script
```

## 🛡️ Data Safety

- **No data loss**: All original files are preserved
- **Automatic backups**: Created during Galaxy sync
- **Read-only operations**: Search and random picker don't modify data
- **Safe played game tracking**: Uses separate played games file

## 🌟 Advantages Over CLI Version

- **Visual**: Beautiful interface with images and charts
- **Interactive**: Click-based navigation and actions
- **Responsive**: Works on desktop, tablet, and mobile
- **Modern**: Contemporary web design and animations
- **Accessible**: No command-line knowledge required
- **Shareable**: Can be accessed by others on your network

## 🔮 Future Enhancements

Potential features for future versions:
- Game rating system
- Wishlist management
- Collection value tracking
- Play time logging
- Achievement tracking
- Social features for sharing collections

## 🆘 Troubleshooting

### Web Server Won't Start
- Ensure Python 3.7+ is installed
- Check that Flask dependencies are installed
- Verify port 5000 is not in use

### Games Not Loading
- Ensure `gameDB.csv` exists in the same directory
- Run Galaxy export to refresh your collection
- Check file permissions

### Images Not Displaying
- This is normal for some games without cover art
- Placeholder icons will be shown instead
- Original functionality is not affected

---

**Enjoy your beautiful new game management experience!** 🎮✨ 