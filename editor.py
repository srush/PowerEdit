import math
import moviepy
from moviepy.editor import *
import sys


# Iterate over audio to find the non-silent parts. Outputs a list of
# (speaking_start, speaking_end) intervals.
# Args:
#  window_size: (in seconds) hunt for silence in windows of this size
#  volume_threshold: volume below this threshold is considered to be silence
#  ease_in: (in seconds) add this much silence around speaking intervals
def find_speaking(audio_clip, window_size=0.1, volume_threshold=0.01, ease_in=0.25):
    # First, iterate over audio to find all silent windows.
    num_windows = math.floor(audio_clip.end/window_size)
    window_is_silent = []
    for i in range(num_windows):
        s = audio_clip.subclip(i * window_size, (i + 1) * window_size)
        v = s.max_volume()
        window_is_silent.append(v < volume_threshold)
    window_is_silent.append(True)
    # Find speaking intervals.
    speaking_start = 0
    speaking_end = 0
    speaking_intervals = []
    for i in range(1, len(window_is_silent)):
        e1 = window_is_silent[i - 1]
        e2 = window_is_silent[i]
        # silence -> speaking
        if e1 and not e2:
            speaking_start = i * window_size
        # speaking -> silence, now have a speaking interval
        if not e1 and e2:
            speaking_end = i * window_size
            new_speaking_interval = [max(0, speaking_start - ease_in), speaking_end + ease_in]
            # With tiny windows, this can sometimes overlap the previous window, so merge.
            need_to_merge = len(speaking_intervals) > 0 and speaking_intervals[-1][1] > new_speaking_interval[0]
            if need_to_merge:
                merged_interval = [max(0, speaking_intervals[-1][0]), new_speaking_interval[1]]
                speaking_intervals[-1] = merged_interval
            else:
                speaking_intervals.append(new_speaking_interval)

    return speaking_intervals


def main():
    name = sys.argv[1]
    aclip = AudioFileClip(f"audio/{name}.wav")
    d = []
    for l in open(f"audio/{name}.txt"):
        time, _, lname = l.split()
        d.append((float(time), lname))

    d.sort()
    slides = []
    last = 0.0
    for t, n in d:
        if t > aclip.duration:
            print("drop", t, n)
            continue
        slides.append((n, last, t))
        last = t
        
    images = []
    sound = []
    for i in range(len(slides)):
        x = slides[i]
        clip2 = aclip.subclip(x[1], x[2])
        intervals_to_keep = find_speaking(clip2)
        keep_clips = [clip2.subclip(start, end) for [start, end] in intervals_to_keep]
        assert(len(keep_clips) > 0)
        clip2 = concatenate_audioclips(keep_clips)
        sound.append(clip2)
        assert clip2.duration > 0, str(intervals_to_keep)
        print(x[0], clip2.duration)
        clip = ImageClip(x[0]).set_duration(clip2.duration)
        images.append(clip)


    video = concatenate_videoclips(images, method="compose")
    print(video.duration)
    audio = concatenate_audioclips(sound)
    print(audio.duration)
    video.audio = audio
    video.write_videofile(f"{name}.mp4", fps=24)

if __name__ == "__main__":
    main()
    


