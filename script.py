from PIL import Image
import os
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

# =====================
# SETTINGS
FRAME_COUNT = 4383  # The amount of frames in your video. Must be at most (the number of frames you have)-1
STEP_SKIP = 1  # Makes the framerate 20/STEP by skipping some frames. Higher value = lower video FPS = lower file size and system requirements
SPEED = 1  # Adjusts the speed of the video. Higher value = slower video. Does not affect the system requirements
# ^ these two above add together resulting if a framerate of (20 / STEP_SKIP) / STEP_TIME
# =====================

dispatch_cmd = []

# Processes an individual image
def process_image(i: int):
    commands = []
    img = Image.open(f"frames/{i}.jpg")
    # Feel free to play around with the numbers
    for x in range(40):
        for y in range(30):
            c1 = str(sum(img.getpixel((479 - (x * 12 + 8), 359 - (y * 12 + 6)))) > 384).lower() # approx
            c2 = str(sum(img.getpixel((479 - (x * 12 + 4), 359 - (y * 12 + 6)))) > 384).lower()
            c3 = str(sum(img.getpixel((479 - (x * 12), 359 - (y * 12 + 6)))) > 384).lower()
            c4 = str(sum(img.getpixel((479 - (x * 12 + 8), 359 - (y * 12)))) > 384).lower()
            c5 = str(sum(img.getpixel((479 - (x * 12 + 4), 359 - (y * 12)))) > 384).lower()
            c6 = str(sum(img.getpixel((479 - (x * 12), 359 - (y * 12)))) > 384).lower()
            commands.append(f"setblock {x} {100 + y} 0 chiseled_bookshelf[slot_0_occupied={c1},slot_1_occupied={c2},slot_2_occupied={c3},slot_3_occupied={c4},slot_4_occupied={c5},slot_5_occupied={c6}]\n")
    with open(f"generated_datapack/data/video/functions/{i}.mcfunction", "w") as file:
        file.writelines(commands)
    print("Finished frame", i, "/", FRAME_COUNT)

if __name__ == "__main__":
    # Create the folder structure of the datapack
    try:
        os.makedirs("generated_datapack/data/minecraft/tags/functions")
    except FileExistsError:
        pass
    try:
        os.makedirs("generated_datapack/data/video/functions")
    except FileExistsError:
        pass

    # Process the images to create the functions
    with Pool() as pool:
        results = pool.imap_unordered(process_image, list(range(1, FRAME_COUNT+1, STEP_SKIP)), chunksize=16)

        for _ in results: pass  # needed to actually run this

    # The dispatch command (chooses what frame to show depending on the tick value)
    for i in range(1, FRAME_COUNT+1, STEP_SKIP):
        dispatch_cmd.append(f"execute if score tick video matches {i*SPEED} run function video:{i}\n")
    dispatch_cmd.append("execute if score tick video matches 1.. run scoreboard players add tick video 1\n")

    with open("generated_datapack/data/video/functions/dispatch.mcfunction", "w") as file:
        file.writelines(dispatch_cmd)

    # The video:load function (what initializes the datapack)
    with open("generated_datapack/data/video/functions/load.mcfunction", "w") as file:
        file.writelines([
            "scoreboard objectives add video dummy\n",
            "scoreboard players set tick video 0"
        ])

    # The video:start function
    with open("generated_datapack/data/video/functions/start.mcfunction", "w") as file:
        file.writelines([
            "scoreboard players set tick video 1"
        ])

    # The video:stop function
    with open("generated_datapack/data/video/functions/stop.mcfunction", "w") as file:
        file.writelines([
            "scoreboard players set tick video 0\n",
            "fill 0 100 0 39 129 0 chiseled_bookshelf"
        ])

    # The functions to be run after the world loads
    with open("generated_datapack/data/minecraft/tags/functions/load.json", "w") as file:
        file.write('{"values": ["video:load"]}')

    # The functions to be run every tick
    with open("generated_datapack/data/minecraft/tags/functions/tick.json", "w") as file:
        file.write('{"values": ["video:dispatch"]}')

    # The pack.mcmeta file for the pack to be recognized by the game
    with open("generated_datapack/pack.mcmeta", "w") as file:
        file.write('{"pack": {"pack_format": 10, "description": "Plays a video with chiseled bookshelves"}, "features": {"enabled": ["update_1_20"]}}')
    print("done")
