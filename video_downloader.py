import instaloader
import os
import shutil
import yt_dlp


class InstaVideoDownloader:
    def __init__(self, username=None, password=None):
        pass
        # self.temp_folder = "temp_download"
        # self.output_folder = "Reels"
        # os.makedirs(self.output_folder, exist_ok=True)

        # self.loader = instaloader.Instaloader(
        #     download_comments=False,
        #     download_geotags=False,
        #     download_pictures=False,
        #     download_video_thumbnails=False,
        #     save_metadata=False,
        #     dirname_pattern=self.temp_folder
        # )

        # if username and password:
        #     try:
        #         print("🔐 Logging into Instagram...")
        #         self.loader.login(username, password)
        #         self.loader.save_session_to_file()
        #         print("✅ Login successful!")
        #     except Exception as e:
        #         print(f"❌ Login failed: {e}")

    def download(self, url, title):
        # shortcode = url.strip("/").split("/")[-1]

        # try:
        #     print(f"📥 Downloading: {shortcode}")
        #     post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
        #     self.loader.download_post(post, target=self.temp_folder)

        #     for fname in os.listdir(self.temp_folder):
        #         if fname.endswith(".mp4"):
        #             src = os.path.join(self.temp_folder, fname)
        #             dst = os.path.join(self.output_folder, f"{title}.mp4")
        #             shutil.move(src, dst)
        #             print(f"✅ Saved: {dst}")
        #             break

        #     shutil.rmtree(self.temp_folder)

        # except Exception as e:
        #     print(f"❌ Error during download: {e}")

        output_path = "reels/%(title)s.%(ext)s"
        ydl_opts = {
        'outtmpl': output_path,
        'format': 'mp4',
        'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])