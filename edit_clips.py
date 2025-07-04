from moviepy import *
import os
from moviepy.editor import *
from moviepy.config import change_settings
import cv2
import numpy as np
from crop_detector import VideoCropDetector
# Set ImageMagick path for text rendering
change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})



class EditClips:
    def __init__(self, file_location = "reels/", resolution = (1080, 1920), fps=60, font_name="Arial", video_height=800):
        self.resolution = resolution
        self.fps = fps
        self.video_location = file_location
        self.font_name = font_name
        self.x_offset = 20
        self.y_start = 500
        self.vertical_spacing = 130
        self.space_betweem_number_caption = 50
        self.clip_information = {}
        self.crop_detector = VideoCropDetector(threshold=15, sample_frames=50)
     


        self.video_height = video_height  # New parameter to control vertical length


    
    def get_information(self):
         clip_information = self.get_video_information(location=self.video_location)
         if clip_information:
            print("Information Gathered Succesfully")
         self.clip_information = clip_information

         return 

    def get_video_information(self, location):
        clips = []
        clip_titles = []
        paths = []
        clip_duration = []
        ranks = []

        for filename in os.listdir(location):
            path = os.path.join(location, filename)
            try:
                rank_title = filename.split(".")[0]
                rank = int(rank_title.split(" ")[0])
                title = " ".join(rank_title.split(" ")[1:])
                
                clip = VideoFileClip(path).resize(width=1080)
                
          
                clips.append(clip)
                clip_titles.append(title)
                paths.append(path)
                clip_duration.append(clip.duration)
                ranks.append(rank)
            except Exception as e:
                print(f"❌ Skipping file '{filename}' due to error: {e}")

        if not clips:
            print("⚠️ No valid videos found in the folder.")
            return {
                'ranks': [],
                'titles': [],
                'clips': [],
                'path': [],
                'durations': [],
                'total duration': 0,
                'start times': []
            }
        # ✅ Sort everything by rank in descending order (rank 5 → rank 1)
        combined = list(zip(ranks, clip_titles, clips, paths, clip_duration))
        combined.sort(reverse=True)  # Higher ranks (5) come first
        ranks, clip_titles, clips, paths, clip_duration = zip(*combined)

        # ✅ Recalculate start times after sorting
        starting_times = [0]
        for d in clip_duration[:-1]:
            starting_times.append(starting_times[-1] + d)

        total_duration = sum(clip_duration)

        # ✅ Now store sorted and correct info
        clip_information = {
            'ranks': list(ranks),
            'titles': list(clip_titles),
            'clips': list(clips),
            'path': list(paths),
            'durations': list(clip_duration),
            'total duration': total_duration,
            'start times': starting_times
        }

        return clip_information


   
    # === STATIC TITLE BAR ===
    def create_title_box(self, title, title_font = "Impact", fontsize = 70):

        total_duration = self.clip_information['total duration']

        # ⬇️ Use caption method which supports rich text via Pango
        text_clip = TextClip(
            title,
            fontsize= fontsize,
            font=title_font,
            color='black',  # fallback color
            size=(900, None),
            method='caption',
            align='center'
        ).set_duration(total_duration)

        box_padding = 50
        box_size = (text_clip.w + box_padding, text_clip.h + box_padding)
        box = ColorClip(size=box_size, color=(255, 255, 255), duration=total_duration)

        title_box = CompositeVideoClip([
            box.set_position(("center", "top")),
            text_clip.set_position(("center", "top"))
        ], size=box_size).set_position(("center", 50))

        return title_box

    

    def composite_ranked_clips(self, title_box_height=150):
        """
        Creates a composite video that fits horizontally under the title.
        
        Args:
            title_box_height: Height space reserved for the title at the top
        """
        clips = self.clip_information.get('clips', [])
        total_duration = self.clip_information.get('total duration', 0)

        # ✅ Handle case where no clips are available
        if not clips or total_duration == 0:
            print("⚠️ No clips to composite. Returning blank background.")
            blank = ColorClip(self.resolution, color=(0, 0, 0), duration=1).set_fps(self.fps)
            return blank

        final_clips = []
        for clip in clips:
            # Resize to fit horizontally within the resolution
            clip = clip.resize(width=self.resolution[0])
            
            # Resize to fit within the specified video height while maintaining aspect ratio
            if clip.h > self.video_height:
                clip = clip.resize(height=self.video_height)
            
            # If the clip is now narrower than the screen width, resize to fit width again
            if clip.w < self.resolution[0]:
                clip = clip.resize(width=self.resolution[0])
                # If this makes it too tall, crop from center
                if clip.h > self.video_height:
                    clip = clip.crop(y_center=clip.h//2, height=self.video_height)

            final_clips.append(clip)

        # Create background
        background = ColorClip(self.resolution, color=(0, 0, 0), duration=total_duration).set_fps(self.fps)
        
        # Concatenate video clips
        video = concatenate_videoclips(final_clips).set_duration(total_duration)
        
        # Position the video under the title (centered horizontally)
        video_y_position = title_box_height + 50  # 50px gap below title
        video = video.set_position(("center", video_y_position))

        # Combine background + video
        composite = CompositeVideoClip([video], size=self.resolution)

        return composite


        # # === STATIC NUMBERS ===
    def add_static_numbers(self, fontsize = 40):
        clip_titles = self.clip_information['titles']
        total_duration = self.clip_information['total duration']
        clips = []
        total_clips = len(clip_titles)
        
        for i in range(total_clips):
            intensity = int(100 * (i / max(1, total_clips - 1)))  # Scales from 0 to 100
            r, g, b = 255, intensity, intensity
            color = f"rgb({r},{g},{b})"
            number = TextClip(f"{i+1}.", fontsize=fontsize, color=color, font=self.font_name, stroke_width=2, stroke_color='black').set_duration(total_duration)
            y_pos = self.y_start + i * self.vertical_spacing
            number = number.set_position((self.x_offset, y_pos))
            clips.append(number)
        return clips


    def add_timed_labels(self, fontsize = 40, color = "white"):
        start_times = self.clip_information['start times']
        titles = self.clip_information['titles']
        durations = self.clip_information['durations']
        label_clips = []
        total = len(titles)
        skip_time = 0
        
        for i in range(total):
            skip_time += start_times[i]
            label = TextClip(titles[i], fontsize=fontsize, color=color, font=self.font_name, stroke_color='black', stroke_width=1, method='label').set_duration(sum(durations) - skip_time)
            # Calculate Y position from bottom (i=0 should be at bottom, i=4 at top)
            y_rank = total - i - 1  # This inverts 0→4 into 4→0
            y_pos = self.y_start + y_rank * self.vertical_spacing
            y_adj = y_pos

            label = label.set_position((self.x_offset + self.space_betweem_number_caption, y_adj)).set_start(start_times[i])
            label_clips.append(label)

        return label_clips
    

    