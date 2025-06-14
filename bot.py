import instaloader
import requests
import os
import glob
import schedule
import time
import hashlib
import traceback
from logger import logger
from config import TARGET_USERNAME, DISCORD_WEBHOOK_URL, YOUR_USERNAME, DOWNLOAD_DIR, SENT_FILE, STORY_DOWNLOAD_INTERVAL_MINUTES, CHECKSUM_CLEANUP_INTERVAL_MINUTES


def clean_directory(path):
    logger.info("Cleaning dir " + path + "...")
    files = glob.glob(path + '/*')
    for f in files:
        os.remove(f)


def clean_sent_hashes():
    with open(SENT_FILE, "w") as f:
        pass  # svuota il file riscrivendolo vuoto
    logger.debug("Checksum cleaning done, list is now resetted.")


def format_filename(item):
    timestamp = item.date_utc.strftime("%Y-%m-%d_%H-%M-%S_UTC")
    ext = ".mp4" if item.is_video else ".jpg"
    return os.path.join(DOWNLOAD_DIR, f"{timestamp}{ext}")


def file_checksum(path):
    hash_sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def job():
    logger.info("Starting job. Checking for stories...")
    clean_directory(DOWNLOAD_DIR)
    # Carica hash già inviati
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r") as f:
            sent_hashes = set(line.strip() for line in f)
    else:
        sent_hashes = set()

    for story in L.get_stories(userids=[profile.userid]):
        for item in story.get_items():
            success = L.download_storyitem(item, target=DOWNLOAD_DIR)
            if not success:
                logger.error(f"Error downloading story {item.mediaid}")
                continue

            fpath = format_filename(item)
            if os.path.exists(fpath):
                checksum = file_checksum(fpath)
                if checksum in sent_hashes:
                    logger.debug(f"Story with checksum {checksum} already sent. Skipping.")
                    continue

                with open(fpath, "rb") as f:
                    response = requests.post(
                        DISCORD_WEBHOOK_URL,
                        files={"file": (os.path.basename(fpath), f)},
                        data={"content": f"📸 @everyone New story from **{TARGET_USERNAME}**"},
                    )
                    logger.debug(f"Sent story {item.mediaid} -> {response.status_code}")

                with open(SENT_FILE, "a") as f:
                    f.write(checksum + "\n")
                    sent_hashes.add(checksum)
            else:
                logger.info(f"File not found: {fpath}")
    logger.info("Ending job.")


schedule.every(STORY_DOWNLOAD_INTERVAL_MINUTES).minutes.do(job)
schedule.every(CHECKSUM_CLEANUP_INTERVAL_MINUTES).minutes.do(clean_sent_hashes)

try:
    logger.info("Scheduler started. CTRL+C to stop.")
    L = instaloader.Instaloader(dirname_pattern=DOWNLOAD_DIR)
    L.load_session_from_file(YOUR_USERNAME)
    profile = instaloader.Profile.from_username(L.context, TARGET_USERNAME)
    job()
except Exception as e:
    error_trace = traceback.format_exc()
    logger.error(f"Error during job execution:\n{error_trace}")
    raise e

while True:
    schedule.run_pending()
    time.sleep(1)
