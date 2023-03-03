# Spotify Downloader
A python script that takes a spotify playlist, downloads music from youtube and uploads it into an s3 bucket.

This script downloads songs from a Spotify playlist using the [spotdl](https://github.com/ritiek/spotify-downloader) library, compresses them into a zip file, and uploads the zip file to an AWS S3 bucket. The user can set the update time (in minutes) to automatically download and upload the playlist at a specific interval.

## Dependencies
- Python 3.7+
- `spotdl`
- `boto3`

## Setup
0. #### WARNING: This code will download, zip and KEEP the files on your bot-running machine, uncomment lines 27-30 to avoid deleting them and they will be downloaded every time the script runs, in an infinite loop of wasting bandwidth and probably generating an expensive cloud-provider bill, the default behavior could potentially fill your hd if you're not careful, but won't incur in extra charges, delete the mp3 files periodically.

1. Install the required packages: `pip install -r requirements.txt`
2. Create an [AWS S3](https://aws.amazon.com/s3/) bucket to upload the zip file.
3. Create a `config.json` file with the following information:
    ```
    {
        "s3_access_key": "YOUR_S3_ACCESS_KEY",
        "s3_secret_key": "YOUR_S3_SECRET_KEY",
        "s3_bucket_name": "YOUR_BUCKET_NAME",
        "playlist_url": "SPOTIFY_PLAYLIST_URL",
        "update_time": UPDATE_TIME_IN_MINUTES
    }
    ```
    - `s3_access_key`: Your AWS access key ID.
    - `s3_secret_key`: Your AWS secret access key.
    - `s3_bucket_name`: The name of the S3 bucket you created in step 2.
    - `playlist_url`: The URL of the Spotify playlist you want to download.
    - `update_time`: The time (in minutes) between updates.

4. Run the script: `python bot.py`

Fire and forget into a cloud instance, any changes you make to that spotify playlist will be downloaded and uploaded to your S3 bucket.
Remember to change your bucket policy to be public.

