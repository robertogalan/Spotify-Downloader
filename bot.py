import os
import time
import json
import zipfile
import subprocess
import boto3

CONFIG_FILE = 'config.json'


def download_songs_from_playlist(playlist_url):
    # download songs from playlist using spotdl
    print("Downloading songs...")
    escaped_url = playlist_url.replace("'", "\\'")
    download_command = f"spotdl '{escaped_url}'"
    subprocess.run(download_command, shell=True)


def compress_files_to_zip():
    # create a zip file of downloaded songs
    print("Compressing files...")
    with zipfile.ZipFile('songs.zip', 'w') as zip_file:
        for filename in os.listdir():
            if filename.endswith('.mp3'):
                zip_file.write(filename)

    # delete mp3 files UNCOMMENT THE FOLLOWING 3 LINES TO DELETE MP3 FILES AFTER DOWNLOAD
    # for filename in os.listdir():
    #    if filename.endswith('.mp3'):
    #        os.remove(filename)


def upload_zip_to_s3(s3_access_key, s3_secret_key, s3_bucket_name):
    try:
        # upload the zip file to S3 using the boto3 library
        print("Uploading file to S3...")
        s3 = boto3.client('s3', aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key)
        s3.upload_file('songs.zip', s3_bucket_name, 'songs.zip')

        # get the download URL
        s3_url = f"https://{s3_bucket_name}.s3.amazonaws.com/songs.zip"
        return s3_url

    except Exception as e:
        print("An error occurred: ", e)
        return None


def download_loop(playlist_url, update_time, s3_access_key, s3_secret_key, s3_bucket_name):
    while True:
        download_songs_from_playlist(playlist_url)
        compress_files_to_zip()
        download_url = upload_zip_to_s3(s3_access_key, s3_secret_key, s3_bucket_name)

        if download_url:
            print(f"Download your music here: {download_url}")
        else:
            print("An error occurred while uploading the file to S3")

        print(f"Next update in {update_time} minutes.")
        time.sleep(update_time * 60)


def load_config():
    if not os.path.isfile(CONFIG_FILE):
        config = {}
        config['s3_access_key'] = input("S3 access key: ")
        config['s3_secret_key'] = input("S3 secret key: ")
        config['s3_bucket_name'] = input("S3 bucket name: ")
        config['playlist_url'] = input("Spotify playlist URL: ")
        config['update_time'] = int(input("Update time (in minutes): "))

        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def main():
    # load config
    config = load_config()

    # start downloading
    print("Starting download loop...")
    download_loop(config['playlist_url'], config['update_time'], config['s3_access_key'], config['s3_secret_key'], config['s3_bucket_name'])


if __name__ == '__main__':
    main()
