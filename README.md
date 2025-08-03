# 🧨 Minesweeper Game (Python + Tkinter)

A classic **Minesweeper** game built with Python and Tkinter GUI, enhanced with scoring, high scores, difficulty levels, and restart functionality.

---

## 🎮 Features

- Three difficulty levels: Easy, Normal, and Hard
- Classic left-click to reveal, right-click to flag bombs (`🚩`)
- Auto-bomb protection on the first click
- Score tracking based on moves and outcome
- High score saving and display
- Reset/Restart button
- Colorful and user-friendly GUI

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Tkinter** (built-in GUI library)
- File-based storage for high scores (`high_score.txt`)

---

## 🚀 Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/minesweeper-tkinter.git
cd minesweeper-tkinter
```

2. **Run the game**

```bash
python minesweeper.py
```

> ✅ No external libraries needed — works with standard Python installation.

---

## 🧾 Game Rules

- Click on cells to reveal them.
- A number shows how many bombs are around.
- Right-click to flag suspected bombs.
- First click will never be a bomb.
- Game ends when you click on a bomb or clear all non-bomb cells.

---

## 📂 File Structure

```
minesweeper-tkinter/
├── minesweeper.py        # Main game file
├── high_score.txt        # (auto-created) Stores top 5 high scores
└── README.md             # Project description
```

---

## 🏆 Scoring System

- Each safe click: +10 points
- Winning bonus: +50 points
- Losing penalty: Halves your current score
- Top 5 high scores saved in `high_score.txt`

---

## 💡 Future Enhancements

- Timer-based scoring
- Themes or dark mode
- Sound effects
- Leaderboard UI
- Mouse hover effects

---

## 🙋‍♂️ Author

**Nikhil Kadam**

---

## 📝 License

This project is open-source and free to use under the [MIT License](LICENSE).
