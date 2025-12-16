

WIDTH = 800
HEIGHT = 600
FPS = 60
WIN_SCORE = 50 


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
PURPLE = (200, 50, 200)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
ORANGE = (255, 165, 0)
YELLOW = (255, 215, 0)
PORTAL_COLOR = (0, 255, 255)
BG_DARK = (15, 15, 40)
GRID_COLOR = (40, 40, 80)
WALL_COLOR = (20, 20, 60) 

LEVEL_DATA = {
    1: {
        "name": "Level 1: Easy", 
        "speed": 6, 
        "gap": (300, 500), 
        "grav_mod": 1.0
    },
    2: {
        "name": "Level 2: Medium", 
        "speed": 10,                
        "gap": (150, 250),          
        "grav_mod": 1.2
    },
    3: {
        "name": "Level 3: Hard", 
        "speed": 14, 
        "gap": (140, 250), 
        "grav_mod": 1.3
    }
}