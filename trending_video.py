import time
import pandas as pd
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

url_ytgaming = "https://www.youtube.com/gaming"
url_trending_live = url_ytgaming + "/games"
url_trending_video = url_ytgaming + "/trending"

driver = webdriver.Firefox()
driver.get(url_trending_video)

i = 0
# Scroll page to get all game cards
while i<10:
    driver.execute_script("window.scrollTo(0, window.scrollMaxY)")
    time.sleep(3)
    i += 1
    print("Scrolling down the page")

resp_channel_names = driver.find_elements(by=By.XPATH, value='//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]')
resp_video_titles = driver.find_elements(by=By.XPATH, value='//a[@id="video-title" and @class="yt-simple-endpoint style-scope ytd-grid-video-renderer"]')
resp_video_views = driver.find_elements(by=By.XPATH, value='//div[@id="metadata-line" and @class="style-scope ytd-grid-video-renderer"]')

update_at = datetime.now() 
new_array = []

for i, (column1, column2, column3) in enumerate(zip(resp_channel_names, resp_video_titles, resp_video_views)):
    try:
        channel_name = column1.text
        video_title = column2.text
        video_views = column3.find_element(by=By.TAG_NAME, value="span").text.split(" ")[0]
        video_url = column2.get_attribute("href")

        if 'M' in video_views:
            video_views = int(float(video_views[:-1])*1000000)
        elif 'K' in video_views:
            video_views = int(float(video_views[:-1])*1000)
        else:
            video_views = int(video_views)

        new_dict = {"update_at": update_at.timestamp(), "channel_name": channel_name, "video_title": video_title, "video_views": video_views, "video_url": video_url}
        new_array.append(new_dict)
    except:
        break
    
df = pd.DataFrame(new_array)
df.to_csv('./output/trending_video.csv', index=False)

driver.close()