# Youtube-music-downloader
YouTube Music Downloader is a Python script that allows you to download audio from YouTube videos and save them as MP3 files. 
The script utilizes the Selenium and PyTube libraries to automate the process of accessing YouTube videos, 
extracting audio streams, and saving them in your desired directory.

## Features

- Download audio from YouTube videos as MP3 files.
- Automatically accept YouTube's cookie consent.
- Name downloaded mp3 files to songs' names.
- Handle exceptions during the download process.

## Prerequisites

- Python 3.x
- Chrome WebDriver (compatible with your Chrome browser version)
- Your public playlist of videos
- For more see
```bash
requirements.txt
```

## Usage

1. Run the script by executing the following command:
```bash
python main.py
```

2. The script will prompt you to enter the URL of the YouTube playlist you want to download from.
3. It will also prompt you to provide the destination folder where you want to save the MP3 files. If you leave it blank, the files will be saved in the current directory.
4. After all downloads are completed, the program will exit, and a "Program is ending" message will be displayed.

## Notes

- This script is designed to run in non-headless mode due to an issue related to the "Permissions-Policy" header that can cause errors in headless mode. The error message "Error with Permissions-Policy header: Unrecognized feature: 'ch-ua-form-factor'" might be encountered. As a workaround, it is recommended to run the script without headless mode until the issue is resolved.
- Please keep in mind that this limitation might impact the script's performance or user experience while the browser is in non-headless mode.

