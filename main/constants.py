# All choices available for the room color combobox
COLOR_CHOICES = (
    (1, 'Grey'),
    (2, 'DarkGrey'),
    (3, 'Blue'),
    (4, 'Navy'),
    (5, 'DarkGreen'),
    (6, 'Green'),
    (7, 'Yellow'),
    (8, 'Orange'),
    (9, 'Red'),
)

# Possible display types for data page
DISPLAY_TYPES = ["Room 1", "Room 2", "Both"]

# color_map and bright_colors prolly only need to be in base.html
# Map color index (see main/models.py) to hex color
COLOR_MAP = ["#808080", "#A9A9A9", "#3c4874", "#000080", "#006400",
    "#008000", "#FFFF00", "#FFA500", "#FF0000"]

# These colors are considered as bright
BRIGHT_COLORS = ["#808080", "#FFFFFF", "#FFFF00", "#FFA500"]

# Possible log intervals
LOG_INTERVALS = ["DISABLE", "5 MIN", "10 MIN", "15 MIN", "30 MIN", "60 MIN"]

# Map log interval choices to seconds
INTERVAL_MAP = {0: 0, 1: 300, 2: 600, 3: 900, 4: 1800, 5: 3600}

# it's not nice that SENSOR_TYPES misses analog
SENSOR_TYPES = ["part", "press", "flow", "hum", "temp"]