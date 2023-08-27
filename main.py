import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pytube import YouTube
import re
import os


class YoutubeDownloader:
    def __init__(self, playlist_url):
        self.playlist_url = playlist_url

        self.options = Options()
        # self.options.add_argument("--headless")
        # self.options.add_argument("--disable-gpu")
        # working in headless returns "Error with Permissions-Policy header: Unrecognized feature:'ch-ua-form-factor'"
        self.options.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(playlist_url)
    
    def get_name(self) -> str:
        """It scrapes video name, deletes text in parethesis like (Official video), 
        substitutes not allowed symbols in file name.
        """
        video_name = self.driver.find_element(By.XPATH, value='//*[@id="title"]/h1/yt-formatted-string').text
        new_video_name = re.sub(r'\([^)]*\)', '', video_name).strip()
        cleaned_name = re.sub(r'[\\/:*?"<>|]', '-', new_video_name).strip()
        return cleaned_name

    def get_destination(self) -> str:
        destination = str(input("Enter the destination or leave blank for current directory: ")) or "."
        while not os.path.exists(destination):
            destination = str(input("Your input is not valid! Type valid destination or leave blank: ")) or "."
        return destination

    def get_mp3(self, desired_video_name: str, destination: str):
        """It downloads Youtube video and saves it in your local
        directory under video's name.
        """
        yt_url = YouTube(str(self.driver.current_url))
        video = yt_url.streams.filter(only_audio=True).first()
                
        try: 
            out_file = video.download(output_path=destination)
            new_file = os.path.join(destination, desired_video_name + '.mp3')
            os.rename(out_file, new_file)
            print(f"{desired_video_name}.mp3 has been successfully downloaded.")
        except Exception as e:
            print(f"There is a problem with downloading or renaming: {desired_video_name}, {e}")
            if os.path.exists(out_file):
                os.remove(out_file)

    def download_playlist(self):
        """It accepts cookie dialog and starts to download music.
        """
        # wait until cookie dialog is visible
        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="dialog"]')))

        # accept cookie
        self.driver.find_element(
            by=By.XPATH, 
            value='//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button'
            ).click()
        time.sleep(2)

        # get number of total videos in the playlist
        path_number = '//*[@id="publisher-container"]/div/yt-formatted-string/span[3]'
        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, path_number)))
        number_of_videos = self.driver.find_element(By.XPATH, value=path_number).text

        destination = self.get_destination()
        # parse videos one by one and get its url link
        for _ in range(int(number_of_videos)):
            time.sleep(1)
            video_name = self.get_name()
            
            try:
                self.get_mp3(video_name, destination)
            except Exception as e:
                print(f"Error occured {e}")

            time.sleep(2)

            # shortcut SHIFT + N is used to watch next video
            ActionChains(self.driver)\
                .key_down(Keys.SHIFT)\
                .send_keys("n")\
                .perform()
            time.sleep(2)
        print("Program is ending...")
        self.driver.quit()


if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=AG-erEMhumc&list=PLsMADWRMH3Ejf6ezUFFBxq32mke6J-ynI"
    downloader = YoutubeDownloader(test_url)
    downloader.download_playlist()