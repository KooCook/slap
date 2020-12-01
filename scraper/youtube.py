import csv
import time
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from dirs import ROOT_DIR


class Video:
    def __init__(self):
        self.video_title = ""
        self.video_id = ""
        self.channel_name = ""
        self.view_count = ""

    def __repr__(self):
        return f"title={self.video_title}, url={self.video_id}, ch_name={self.channel_name}, v={self.view_count}\n"


driver = webdriver.Chrome()
# YouTube: id (video_id), title, genre, artist (channel), lyrics, publishedAt, duration, viewCount, likeCount, dislikeCount, favoriteCount, commentCount, localization, defaultLanguage


def scrape_feed_page(url: str) -> Dict[str, Video]:
    driver.get(url)
    videos: Dict[str, Video] = {}
    it = 0
    LIMIT = 500
    VIEW_LIMIT = '10M'
    while it <= LIMIT:
        last_view_count = 0
        for ele in driver.find_elements_by_tag_name('ytd-video-renderer'):
            video_link = ele.find_element_by_xpath(".//div//ytd-thumbnail//a").get_attribute("href").replace("https://www.youtube.com/watch?v=", "")
            video_title = ele.find_element_by_xpath('''.//div//div//*[@id="meta"]//*[@id="title-wrapper"]
            //h3//*[@id="video-title"]//yt-formatted-string''').text
            # channel_name = ele.find_element_by_xpath('''.//div//div//*[@id="meta"]//ytd-video-meta-block
            #     //*[@id="metadata"]//*[@id="byline-container"]//ytd-channel-name
            #     //*[@id="container"]//*[@id="text-container"]//yt-formatted-string
            #     //a''').text
            channel_name = ele.find_element_by_xpath('''.//div//div//*[@id="channel-info"]//ytd-channel-name
                //*[@id="container"]//*[@id="text-container"]//yt-formatted-string//a''').text
            view_count = ele.find_element_by_xpath('''.//div//div//*[@id="meta"]//ytd-video-meta-block
                  //*[@id="metadata"]//*[@id="metadata-line"]//span''').text
            vid = Video()
            vid.video_title = video_title
            vid.video_id = video_link
            vid.channel_name = channel_name
            vid.view_count = view_count.replace(" views", "")
            last_view_count = vid.view_count
            videos[vid.video_id] = vid
            if last_view_count == VIEW_LIMIT:
                break
        if last_view_count == VIEW_LIMIT:
            break
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        print(videos)
        it += 1
        print(f"===== {it} ===== `{last_view_count}`")
    # driver.quit()
    return videos


def write_scraped_to_csv(videos: Dict[str, Video]):
    with open(ROOT_DIR / f'tests/data/youtube/scraped_most_viewed_music_us.csv', 'w',
              newline='') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['id', 'title', 'channelTitle', 'viewCount'])
        for video in videos.values():
            writer.writerow([video.video_id, video.video_title, video.channel_name, video.view_count])


# Trending page URL: "https://www.youtube.com/feed/trending?bp=4gIuCggvbS8wNHJsZhIiUExGZ3F1TG5MNTlhbkJodVBsX3k3d1k1MGtiMGh5WW16bw%3D%3D&gl=US"
if __name__ == '__main__':
    vids = scrape_feed_page("https://www.youtube.com/results?search_query=music&sp=CAM%253D&persist_gl=1&gl=US")
    write_scraped_to_csv(vids)
