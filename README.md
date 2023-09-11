# PowerEdit ⚡

I wanted to make videos, but I also didn't want to learn how to use video editing software. This was my attempt to get around that issue. 

This software lets you make "videos" that just consist of talking over static slides. If you want anything fancier this is not for you.

![image](https://github.com/srush/PowerEdit/assets/35882/73da1e11-c6d7-4a51-9fa9-b7b1e917ed49)


## Setup

Download [Audacity](https://www.audacityteam.org/download/) and turn on mod-script-pipe. This let's you script audacity. 

![image](https://github.com/srush/PowerEdit/assets/35882/50b00ef9-c0a0-4a7a-90e9-a772e0b2cf9e)

Clone this repo and install this repo `requirements.txt`. 

```bash
> apt-get install poppler-utils
> git clone https://github.com/srush/PowerEdit/
> cd PowerEdit; pip install -r requirements.txt
```

## Usage. 

There is an example included in the repo called `Lecture11` Here's how I made it.

1) Make slides using software that lets you export to PDF (beamer, reveal.js, google slides w/o animations, etc)
2) Save Lecture11.pdf to the slides/ directory, and run `python convert.py`
3) Open Audacity and make a new file.
4) Run `python -m streamlit run run.py Lecture11` You should see you first slide.
5) Press "Record" and confirm that audacity starts recording.
 When you are done presenting a slide, press "Next". Audactiy should put in a label with the name of the slide you just finished.
  * If you mess up on a slide then press "Again" and it should reset from the beginning of the slide.
  * If you want to skip a slide, press "Skip" and it will jump to the next slide without putting in a label.
  * Don't worry about silence between slides, that will get deleted automatically.
6) When you are done recording, go through and fix up the sound in audacity, then export the audio as a Lecture11.wav file in audio/. Also export the labels Lecture11.txt.
7) Finally run `python editor.py Lecture11`, this will go through all the images and audio and make a `Lecture11.mp4` file. This normally takes about 30 minutes.
8) Watch the video and check that it looks good.
9) Upload to youtube with [youtube-upload](https://github.com/tokland/youtube-upload). You will need to setup your authentication details the first time. 
