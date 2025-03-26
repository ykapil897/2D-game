# 🚀 Space Journey: 2D OpenGL Game

A challenging **2D platformer** built with Python and OpenGL. Navigate through three distinct worlds, collect keys, avoid enemies, and reach the exit door to progress.

---

## 🎮 Features

### 🌍 Multiple Game Maps
- **Jungle** – Navigate through lush grassland terrain
- **River** – Cross dangerous waters using moving stones
- **Space** – Explore a solar system with orbiting planets

### ⚡ Physics-Based Movement
- Charge jumps of varying distances
- Navigate moving platforms
- Escape approaching enemies

### 🎯 Game Mechanics
- **Health & Lives System** – Survive hazards and enemy attacks
- **Key Collection** – Unlock the exit door by collecting **three keys**
- **Environmental Hazards** – Water and space areas drain health if not on a safe platform

### 💾 Save System
- **Auto-save progress** – Continue where you left off

### 🖼️ Immersive Visuals
- **Colorful OpenGL-rendered graphics**
- **Visual HUD** displaying health, lives, and time

---

## 🕹️ Controls

### **Movement**
- `W` – Move **up**
- `A` – Move **left**
- `S` – Move **down**
- `D` – Move **right**

### **Jumping**
- **Hold** `SPACE` – Charge jump
- **Use WASD** – Adjust jump direction while charging
- **Release** `SPACE` – Perform jump (longer charge = longer jump)

### **Game Navigation**
- **Use mouse** to interact with menu buttons

---

## 🎮 Gameplay

### 🔑 Objective
- Collect **three keys** per level
- Reach the **exit door** (red circle in the top-right corner) to progress

### 🛡️ Survival
- Stay on platforms to **avoid damage**
- **Avoid enemies** that drain health on contact
- In **space level**, dodge the **sun** at the center!

### 🏆 Movement Strategy
- **Plan jumps carefully** – charging longer creates longer jumps
- **Time movements** to land safely on platforms
- **Use platforms** to cross hazardous areas

---

## 🛠️ Prerequisites

- **Python** 3.6 or higher
- Required packages: `numpy`, `PyOpenGL`, `glfw`, `imgui`

---

## 🔧 Installation

### Clone this repository:
```sh
git clone <repository-url>
cd <game-directory>
```

### Install dependencies:
```sh
pip install -r requirements.txt
```

### Run the Game:
```sh
python main.py
```

---

## 🎯 Game Tips
✅ Don't stay in **water/space** for too long – your health decreases!  
✅ Collect **all three keys** before reaching the exit door  
✅ **Avoid enemies** – they drain health quickly!  
✅ In the **space level**, planets orbit the sun – **time your jumps carefully**!  
✅ If you **die**, you'll respawn at the entry point with one less life  

---

## 📜 License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

🚀 **Get ready for an interstellar adventure!** 🌌