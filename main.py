import time
import pandas as pd
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

from selenium import webdriver
from selenium.webdriver.common.by import By


def get_ytgaming_trending(type=None):
    # define the main url
    url_ytgaming = "https://www.youtube.com/gaming"
    
    # logic to access the page in the browser
    if type == "live":
        # set webdriver (using Mozilla Firefox for this time)
        driver = webdriver.Firefox()
        output_filename = "trending_live"
        url_trending_live = url_ytgaming + "/games"
        driver.get(url_trending_live)
    elif type == "video":
        # set webdriver (using Mozilla Firefox for this time)
        driver = webdriver.Firefox()
        output_filename = "trending_video"
        url_trending_video = url_ytgaming + "/trending"
        driver.get(url_trending_video)
    else:
        output_filename = None
        print("The choices only for live streams or videos")
        # break
    
    i = 0
    # scroll down the page
    while i<10:
        driver.execute_script("window.scrollTo(0, window.scrollMaxY)")
        time.sleep(3)
        i += 1
        print("Scrolling down the page")

    # define some variables
    update_at = datetime.now().timestamp()
    new_array = []

    # logic for scraping pages by its type
    if type == "live":
        resp_game_title = driver.find_elements(by=By.XPATH, value='//yt-formatted-string[@id="title" and @class="style-scope ytd-game-details-renderer"]')
        resp_game_views = driver.find_elements(by=By.XPATH, value='//yt-formatted-string[@id="live-viewers-count" and @class="style-scope ytd-game-details-renderer"]')

        for i, (column1, column2) in enumerate(zip(resp_game_title, resp_game_views)):
            try:
                game_title = column1.text
                game_view = column2.find_element(by=By.TAG_NAME, value="span").text
                if 'K' in game_view:
                    game_view = int(float(game_view[:-1])*1000)
                else:
                    game_view = int(game_view)
                new_dict = {"update_at": update_at, "game_title": game_title, "live_views": game_view}
                new_array.append(new_dict)
            except:
                break
    elif type == "video":
        resp_channel_names = driver.find_elements(by=By.XPATH, value='//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]')
        resp_video_titles = driver.find_elements(by=By.XPATH, value='//a[@id="video-title" and @class="yt-simple-endpoint style-scope ytd-grid-video-renderer"]')
        resp_video_views = driver.find_elements(by=By.XPATH, value='//div[@id="metadata-line" and @class="style-scope ytd-grid-video-renderer"]')

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

                new_dict = {"update_at": update_at, "channel_name": channel_name, "video_title": video_title, "video_views": video_views, "video_url": video_url}
                new_array.append(new_dict)
            except:
                break
    else:
        print("The choices only for live streams or videos")
        # break

    # make a dataframe and save it to a csv file 
    df = pd.DataFrame(new_array)
    df.to_csv(f'./output/output_{output_filename}.csv', index=False)

    # close the browser
    driver.close()

if __name__ == '__main__':
    with ProcessPoolExecutor() as executor:
        trending_types = ["live", "video"]
        results = [executor.submit(get_ytgaming_trending, trending_type) for trending_type in trending_types]