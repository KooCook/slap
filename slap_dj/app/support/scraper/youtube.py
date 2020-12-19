from app.support.scraper.base import driver

URL = 'https://music.youtube.com/playlist?list=PLOHoVaTp8R7dfrJW5pumS0iD_dhlXKv17'


def get_youtube_music_playlist_chart(url: str):
    driver.upsert(url)
    for ele in driver.find_elements_by_tag_name('ytmusic-responsive-list-item-renderer'):
        try:
            video_title = ele.find_element_by_xpath('.//*[@class="title-column"]//yt-formatted-string//a"]').text
            video_artist = ele.find_element_by_xpath('.//div//*[@class="secondary-flex-columns"]'
                                                     '//yt-formatted-string//a"]').text
            print(video_title, video_artist)
        except SyntaxError:
            continue
    driver.close()


if __name__ == '__main__':
    get_youtube_music_playlist_chart(URL)
