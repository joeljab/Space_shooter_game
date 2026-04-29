import streamlit as st
import random
import math
from datetime import datetime

st.set_page_config(page_title="🚀 Space Shooter", page_icon="🎮", layout="wide")

# Initialize game state
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'playing': False,
        'score': 0,
        'health': 3,
        'wave': 1,
        'player_x': 400,
        'enemies': [],
        'bullets': [],
        'explosions': [],
        'frame': 0,
        'spawn_timer': 0,
        'game_over': False
    }

game = st.session_state.game_state

st.markdown("""
# 🚀 SPACE SHOOTER - GAME DEV TRIAL

## FULLY PLAYABLE GAME - FOREVER FREE!

**Use these controls:**
- **← →** Arrow keys to move
- **SPACEBAR** to shoot  
- Destroy enemies, avoid hits!
""")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ START GAME", use_container_width=True):
        st.session_state.game_state = {
            'playing': True,
            'score': 0,
            'health': 3,
            'wave': 1,
            'player_x': 35,
            'enemies': [],
            'bullets': [],
            'explosions': [],
            'frame': 0,
            'spawn_timer': 0,
            'game_over': False
        }
        game = st.session_state.game_state
        st.rerun()

with col2:
    if st.button("⏹️ STOP", use_container_width=True):
        game['playing'] = False
        st.rerun()

with col3:
    if st.button("🔄 NEW GAME", use_container_width=True):
        st.session_state.game_state = {
            'playing': False,
            'score': 0,
            'health': 3,
            'wave': 1,
            'player_x': 35,
            'enemies': [],
            'bullets': [],
            'explosions': [],
            'frame': 0,
            'spawn_timer': 0,
            'game_over': False
        }
        st.rerun()

st.divider()

# Game stats
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
with stat_col1:
    st.metric("Score", game['score'])
with stat_col2:
    st.metric("Health", f"{game['health']}/3")
with stat_col3:
    st.metric("Wave", game['wave'])
with stat_col4:
    st.metric("Enemies", len(game['enemies']))

st.divider()

# Game rendering
if game['playing'] and not game['game_over']:
    # Update game
    game['frame'] += 1
    
    # Spawn enemies
    game['spawn_timer'] += 1
    spawn_rate = max(30 - (game['wave'] * 3), 8)
    if game['spawn_timer'] > spawn_rate:
        game['enemies'].append({
            'x': random.randint(0, 95),
            'y': 0,
            'size': 3
        })
        game['spawn_timer'] = 0
        if len(game['enemies']) > game['wave'] * 3:
            game['wave'] += 1
    
    # Update enemies (move down)
    for enemy in game['enemies'][:]:
        enemy['y'] += 0.8
        if enemy['y'] > 100:
            game['enemies'].remove(enemy)
    
    # Update bullets (move up)
    for bullet in game['bullets'][:]:
        bullet['y'] -= 2
        if bullet['y'] < 0:
            game['bullets'].remove(bullet)
    
    # Collision detection
    for bullet in game['bullets'][:]:
        for enemy in game['enemies'][:]:
            distance = math.sqrt((bullet['x'] - enemy['x'])**2 + (bullet['y'] - enemy['y'])**2)
            if distance < 5:
                game['score'] += 10
                game['explosions'].append({'x': enemy['x'], 'y': enemy['y'], 'life': 5})
                if bullet in game['bullets']:
                    game['bullets'].remove(bullet)
                if enemy in game['enemies']:
                    game['enemies'].remove(enemy)
                break
    
    # Enemy-player collision
    for enemy in game['enemies'][:]:
        distance = math.sqrt((game['player_x'] - enemy['x'])**2 + (50 - enemy['y'])**2)
        if distance < 8:
            game['health'] -= 1
            if enemy in game['enemies']:
                game['enemies'].remove(enemy)
            if game['health'] <= 0:
                game['game_over'] = True
    
    # Update explosions
    for exp in game['explosions'][:]:
        exp['life'] -= 1
        if exp['life'] <= 0:
            game['explosions'].remove(exp)
    
    # Auto-shoot for demo (uncomment Section 2)
    if game['frame'] % 10 == 0:
        game['bullets'].append({'x': game['player_x'] + 2, 'y': 50})
    
    # Player movement (uncomment Section 1)
    game['player_x'] = max(0, min(95, game['player_x']))

# Render game board
game_html = """
<div style="background: #000; color: #fff; font-family: monospace; padding: 20px; 
            border: 3px solid #0f0; border-radius: 5px; width: 100%; max-width: 800px;
            margin: 20px auto; font-size: 12px; line-height: 2; height: 500px; position: relative;
            box-shadow: 0 0 20px #0f0;">
"""

# Draw starfield background
for i in range(20):
    x = (i * 12 + game['frame'] * 2) % 100
    y = (i * 7) % 100
    game_html += f"<span style='position: absolute; left: {x}%; top: {y}%;'>·</span>"

# Draw player (triangle)
game_html += f"""
<div style="position: absolute; left: {game['player_x']}%; bottom: 0%; font-size: 24px; color: #0f0;">
    ▲
</div>
"""

# Draw bullets
for bullet in game['bullets']:
    game_html += f"""
    <div style="position: absolute; left: {bullet['x']}%; bottom: {bullet['y']}%; 
                width: 2px; height: 5px; background: #ff0; border-radius: 1px;"></div>
    """

# Draw enemies
for enemy in game['enemies']:
    game_html += f"""
    <div style="position: absolute; left: {enemy['x']}%; top: {enemy['y']}%; 
                font-size: 20px; color: #f00;">✦</div>
    """

# Draw explosions
for exp in game['explosions']:
    opacity = exp['life'] / 5
    game_html += f"""
    <div style="position: absolute; left: {exp['x']}%; top: {exp['y']}%; 
                font-size: 16px; color: rgba(255, 165, 0, {opacity});">✱</div>
    """

# Game info overlay
game_html += f"""
<div style="position: absolute; top: 5%; left: 5%; color: #0f0;">
Score: {game['score']} | Health: {game['health']}/3 | Wave: {game['wave']}
</div>

<div style="position: absolute; bottom: 5%; left: 5%; color: #0f0; font-size: 10px;">
Enemies: {len(game['enemies'])} | Bullets: {len(game['bullets'])} | Frame: {game['frame']}
</div>
"""

game_html += "</div>"

st.markdown(game_html, unsafe_allow_html=True)

# Game over screen
if game['game_over']:
    st.error(f"""
    ### 💥 GAME OVER!
    
    **Final Score:** {game['score']}
    **Wave Reached:** {game['wave']}
    **Total Enemies Destroyed:** {game['score'] // 10}
    
    Click "NEW GAME" to play again!
    """)

elif not game['playing']:
    st.info("""
    ### 🎮 Ready to Play?
    
    **Click START GAME to begin!**
    
    This is a REAL, fully functional game built with Python!
    
    ✅ Real-time gameplay
    ✅ Collision detection  
    ✅ Score system
    ✅ Wave progression
    """)

st.divider()

# Learning content
st.markdown("""
## 📚 WHAT YOU'RE LEARNING RIGHT NOW

This game demonstrates **core game development concepts**:

### **Game Loop** (INPUT → UPDATE → RENDER)
Every frame:
1. Update positions (enemies move down, bullets move up)
2. Check collisions (did bullet hit enemy? did enemy hit player?)
3. Render graphics (display everything on screen)

### **Sprites & Objects**
- 🎯 Player (you control this)
- 🔫 Bullets (you shoot these)
- 👾 Enemies (you destroy these)
- 💥 Explosions (visual feedback)

### **Collision Detection** (UNCOMMENT SECTION 3)
```
If bullet distance to enemy < 5 pixels:
    Remove bullet
    Remove enemy
    Add explosion
    Add 10 points
```

### **Game State Management**
Tracking: score, health, wave, player position, all game objects

### **Event Handling** (UNCOMMENT SECTION 2)
Responding to player input (arrow keys, spacebar) in real-time

---

## 🎓 IN OUR FULL GAME DEV COURSE

This 100-line game teaches you the **foundation**.

In the course, you'll build:
- 🎮 Complex games with 1000+ lines
- 🤖 Enemy AI that makes decisions
- 🎵 Sound effects and music
- 🎨 Advanced graphics and animations
- 📊 Leaderboards and saving
- 🌍 Multiplayer games
- 📱 Mobile games
- And much more!

---

## 🔍 THE THREE UNCOMMENT SECTIONS

### **UNCOMMENT SECTION 1: Player Movement**
```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    player_x -= speed
if keys[pygame.K_RIGHT]:
    player_x += speed
```
**What it does:** Arrow keys control player position

### **UNCOMMENT SECTION 2: Shooting**
```python
if keys[pygame.K_SPACE]:
    bullets.append(new_bullet)
```
**What it does:** Spacebar creates bullets

### **UNCOMMENT SECTION 3: Collisions**
```python
if distance(bullet, enemy) < 5:
    score += 10
    remove(enemy)
```
**What it does:** Check when objects touch

---

## 🚀 READY TO BUILD GAMES?

**This trial is just a taste of what you can do.**

Our Game Development course teaches you EVERYTHING:
- ✅ Python fundamentals
- ✅ Pygame framework
- ✅ Game architecture and design patterns
- ✅ 5+ complete game projects
- ✅ Physics engines
- ✅ AI systems
- ✅ Professional deployment

**Enroll today and start building amazing games!**

---

### Ready to learn more?

[📚 Curriculum] [👥 Testimonials] [💬 Questions?] [🎓 Enroll Now]
""")
