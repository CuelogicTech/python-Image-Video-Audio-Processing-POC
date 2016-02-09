# For extracting audio from video:
# Install the moviepy first before running this code:
# In Terminal run the command: (sudo) pip install moviepy

# https://github.com/imageio/imageio-binaries/raw/master/ffmpeg/ffmpeg.linux64

import moviepy.editor as mp
clip = mp.VideoFileClip("WorldStores.mp4").subclip(0, 5)
clip.audio.write_audiofile("audio.wav")
