# Bad Apple
A script to make Bad Apple (and other videos) with Minecraft's chiseled bookshelves

# Requirements
- [ffmpeg](https://ffmpeg.org/download.html) (or any other tool to convert a video into individual frames)
- at least 100 MB of storage (or more for long videos)
- at least 2-3 GB of RAM to allocate to Minecraft (long videos require more RAM, 2 GB will not be enough in that case)
- a video in 480x360 resolution
- Python 3.6 or newer with PIL (pillow) installed
- Minecraft: Java Edition 22w46a+

# Usage
- Install Pillow with the command `pip install pillow` (in a terminal) if you haven't already
- Put the frames of your video in the `frames` folder (create it first). If you're using ffmpeg:
  - Run `<ffmpeg> -i <your video> -r <desired framerate> <path to script>/frames/%d.jpg`, where:
    - `ffmpeg` is the path to your ffmpeg installation, if it's not installed globally
    - `your video` is the path to the source video
    - `desired framerate` makes ffmpeg skip some frames, giving you only so much frames per second. Can be used to adjust the speed of the video. With the default settings, higher values make the video slower, lower values make it faster. 20 gives the normal speed.
    - `path to script` is the path to the folder where you put the script
    - The rest of the command should not be changed
  - Adjust the settings in the script. They're the values after the words in all caps:
    - `FRAME_COUNT` is how much frames you got after converting, or something smaller (in which case the video will cut off early)
    - `STEP_SKIP` is how much frames to step over when generating the datapack. Use this to adjust the framerate of the video. The default value gives 20 FPS, the maximum possible.
    - `SPEED` is the speed of the video. Use this to slow down or speed up the video together with the `desired framerate` used before. The default value gives you the speed of (20/`desired framerate`) x normal speed.
    - All of these should be whole numbers and at least 1.
  - Run the script and wait until it finishes.
  - Add the generated datapack to your world upon creation (or later, if you've enabled the 1.20 features before) and enable cheats
  - Run `/function video:start` to play the video. It will appear around the coordinates 20 110 0
  - Use `/function video:stop` to stop the video.
  - Enjoy!