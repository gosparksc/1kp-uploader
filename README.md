# 1kp-uploader

Automated pitch uploading in Python using Selenium.

## Prerequisites

1. Place all videos that you want to upload in a separate folder.

1. Install HandBrake (https://handbrake.fr/).

1. Open HandBrake and select the folder containing your source videos.

1. 

1. Copy newly compressed files from folder into `./data/videos`.

## Installation

1. Make sure that you have Firefox (http://firefox.com/) installed on your system.

1. Install dependencies.

    ```bash
    $ pip install -r requirements.txt
    ```

## Usage

1. The recommended directory structure:

    ```
    .
    ├── data
    |   ├── videos
    |   |   └── first_last.mp4
    |   └── video_pitch_data.csv
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    ├── sample_data.csv
    └── uploader.py
    ```

1. `data/video_pitch_data.csv` contains data in the following format:

    ```
    First,Last,netid@usc.edu,"Letters, Arts and Sciences",2019,"Name of Pitch","Research","Description."
    ```
    Newlines act as delimiters between rows. Populate `data/video_pitch_data.csv` with properly formatted data for the current batch of uploads.

1. Videos for the current batch of uploads go in `data/videos`. File names should be formatted `first_last.mp4`. **All videos must be less than 30 MB.**

1. Start upload batch:

    ```
    $ python uploader.py
    ```

    **IMPORTANT**: Makes sure that your data in `data/video_pitch_data.csv` is 100% correct. You will not be given the opportunity to make changes to the data after you commit it.
