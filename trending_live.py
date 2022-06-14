import time
import pandas as pd
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

url_ytgaming = "https://www.youtube.com/gaming"
url_trending_live = url_ytgaming + "/games"
url_trending_video = url_ytgaming + "/trending"

driver = webdriver.Firefox()
driver.get(url_trending_live)

i = 0
# Scroll page to get all game cards
while i<10:
    driver.execute_script("window.scrollTo(0, window.scrollMaxY)")
    time.sleep(3)
    i += 1
    print("Scrolling down the page")


resp_game_title = driver.find_elements(by=By.XPATH, value='//yt-formatted-string[@id="title" and @class="style-scope ytd-game-details-renderer"]')
resp_game_views = driver.find_elements(by=By.XPATH, value='//yt-formatted-string[@id="live-viewers-count" and @class="style-scope ytd-game-details-renderer"]')

update_at = datetime.now() 
new_array = []

for i, (column1, column2) in enumerate(zip(resp_game_title, resp_game_views)):
    try:
        game_title = column1.text
        game_view = column2.find_element(by=By.TAG_NAME, value="span").text
        if 'K' in game_view:
            game_view = int(float(game_view[:-1])*1000)
        else:
            game_view = int(game_view)
        new_dict = {"update_at": update_at.timestamp(), "game_title": game_title, "live_views": game_view}
        new_array.append(new_dict)
    except:
        break

df = pd.DataFrame(new_array)
df.to_csv('./output/trending_live.csv', index=False)

driver.close()