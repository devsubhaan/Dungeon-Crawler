# 🗡️ Pygame Top-Down Dungeon Crawler

This is an older project built a while ago, so there are some known bugs. I plan on fixing them in future updates while upgrading core gameplay mechanics.

The main premise of the game is a character using guns to clear out dungeon rooms, gather loot from chests, and defeat a boss at the end.

---

## 🎮 Current Features
* **Authentication & Config:** Login system with customizable settings (fullscreen, audio volume, keybinds)
* **Combat & Movement:** Diagonal 8-way movement with a 360° rotating weapon
* **Database System:** Built-in SQLite database for tracking user stats and high scores
* **Loot & Interactables:** Chests that drop energy, score bonuses, or new weapons
* **Level Design:** Custom tilemaps loaded via Tiled and PyTMX
* **Boss Encounter:** Boss battle at the final room
* **Audio & Visuals:** Custom sound effects and sprite animations

---

## 🗺️ Roadmap & Future Improvements
* [ ] **Procedural Generation:** Replace fixed map layouts with dynamic procedural generation
* [ ] **Better Assets:** Polish visual sprites and animations
* [ ] **Lore building:** Expand the game's lore and overall theme
* [ ] **More weapons:** Including more weapons like melee weapons etc.

---

## 🕹️ Controls
* **WASD / Arrow Keys:** Movement *(rebindable in settings)*
* **Left Mouse Click:** Shoot weapon
* **Spacebar:** Drop active weapon
* **Tab:** Swap weapon

---

## 🛠️ Requirements & Setup

### 1. Install Dependencies
Make sure you have **Python 3.8+** installed, then run:
```bash
pip install -r requirements.txt
