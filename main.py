from selenium import webdriver
import time
import pyautogui
from PIL import ImageGrab
import numpy as np

GAME_URL = 'https://elgoog.im/dinosaur-game/'

HIT_BOX_TOP = 680
HIT_BOX_BOTTOM = 770
HIT_BOX_LEFT = 350
HIT_BOX_RIGHT_START = 450
HIT_BOX_RIGHT_MAX = 900

NIGHT_PIXEL_LOCATION = (100, 400, 101, 401)
NIGHT_THRESHOLD = 200

DAY_HIT_THRESHOLD = 253
NIGHT_HIT_THRESHOLD = 27

HIT_BOX_EXPANSION_TIME = 2.5   # seconds
HIT_BOX_EXPANSION_PIXELS = 10

# Create the Chrome WebDriver and navigate to the Dinosaur Game
driver = webdriver.Chrome()
driver.get(GAME_URL)
driver.maximize_window()

# Wait for the page to load and then press space to start the game
time.sleep(5)
pyautogui.press('space')
time.sleep(2)

# Initialize variables to be used in the game loop
start = time.time()
hit_box_right = HIT_BOX_RIGHT_START
moving_timeout = 5
moving_timer_start = time.time()
last_hit_box_mean = 0
hit_box_mean = 0

# Game loop
while True:
    # Grab parts of the screen for hit box and night detection information
    night_detection_img = ImageGrab.grab(bbox=NIGHT_PIXEL_LOCATION)
    night = np.array(night_detection_img)[0][0][0] < NIGHT_THRESHOLD
    hit_box_img = ImageGrab.grab(bbox=(HIT_BOX_LEFT, HIT_BOX_TOP, hit_box_right, HIT_BOX_BOTTOM))
    hit_box_mean = np.mean(np.array(hit_box_img))

    # Detect objects in hit box and jump (press space) if needed
    if (hit_box_mean < DAY_HIT_THRESHOLD and not night) or (hit_box_mean > NIGHT_HIT_THRESHOLD and night):
        pyautogui.press('space')

    # Expand the hit box periodically
    if time.time() - start > HIT_BOX_EXPANSION_TIME and hit_box_right < HIT_BOX_RIGHT_MAX:
        hit_box_right += HIT_BOX_EXPANSION_PIXELS
        start = time.time()

    # Check for Game Over and restart if needed
    if abs(hit_box_mean - last_hit_box_mean) > 1:
        moving_timer_start = time.time()
    last_hit_box_mean = hit_box_mean
    if time.time() - moving_timer_start > moving_timeout:
        hit_box_right = HIT_BOX_RIGHT_START
        moving_timer_start = time.time()
        pyautogui.press('space')
