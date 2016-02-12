from pydub import AudioSegment
import time
import moviepy.editor as mp

sound = AudioSegment.from_file("audio/01.mp3")
sound.export("audio/output_1.wav", format="wav")
seconds = (len(sound) / 1000)

print time.strftime("%H:%M:%S", time.gmtime(seconds))

clip = mp.AudioFileClip('audio/output_1.wav').subclip(0, 10)
clip.write_audiofile("audio/ot.wav")


# playlist_length = len(playlist) / (1000*60)
