from PIL import Image
import os

# =====================
# SETTINGS
FRAME_COUNT = 4384  # The amount of frames in your video. Must not be larger than what you have in the frames folder.
STEP_SKIP = 1  # Makes the framerate 20/STEP by skipping some frames. Higher value = lower video FPS = lower file size and system requirements
SPEED = 1  # Adjusts the speed of the video. Higher value = slower video
# ^ these two above add together resulting if a framerate of (20 / STEP_SKIP) / STEP_TIME
# =====================

commands = []
dispatch_cmd = []

try:
    os.makedirs("generated_datapack/data/minecraft/tags/functions")
except FileExistsError:
    pass
try:
    os.makedirs("generated_datapack/data/video/functions")
except FileExistsError:
    pass

for i in range(1, FRAME_COUNT, STEP_SKIP):
    img = Image.open(f"frames/{i}.jpg")
    # Feel free to play around with the numbers
    for x in range(40):
        for y in range(22):
            c1 = str(sum(img.getpixel((479 - (x * 12 + 8), 359 - (y * 16 + 8)))) > 375).lower() # approx
            c2 = str(sum(img.getpixel((479 - (x * 12 + 4), 359 - (y * 16 + 8)))) > 375).lower()
            c3 = str(sum(img.getpixel((479 - (x * 12), 359 - (y * 16 + 8)))) > 375).lower()
            c4 = str(sum(img.getpixel((479 - (x * 12 + 8), 359 - (y * 16)))) > 375).lower()
            c5 = str(sum(img.getpixel((479 - (x * 12 + 4), 359 - (y * 16)))) > 375).lower()
            c6 = str(sum(img.getpixel((479 - (x * 12), 359 - (y * 16)))) > 375).lower()
            commands.append(f"setblock {x} {100 + y} 0 chiseled_bookshelf[slot_0_occupied={c1},slot_1_occupied={c2},slot_2_occupied={c3},slot_3_occupied={c4},slot_4_occupied={c5},slot_5_occupied={c6}]\n")
    with open(f"generated_datapack/data/video/functions/{i}.mcfunction", "w") as file:
        file.writelines(commands)
    commands = []
    dispatch_cmd.append(f"execute if score tick video matches {i*SPEED} run function video:{i}\n")
    print("Finished frame", i, "/", FRAME_COUNT)

with open("generated_datapack/data/video/functions/dispatch.mcfunction", "w") as file:
    dispatch_cmd.append("execute if score tick video matches 1.. run scoreboard players add tick video 1\n")
    file.writelines(dispatch_cmd)

with open("generated_datapack/data/video/functions/load.mcfunction", "w") as file:
    file.writelines([
        "scoreboard objectives add video dummy\n",
        "scoreboard players set tick video 0"
    ])

with open("generated_datapack/data/video/functions/start.mcfunction", "w") as file:
    file.writelines([
        "scoreboard players set tick video 1"
    ])

with open("generated_datapack/data/video/functions/stop.mcfunction", "w") as file:
    file.writelines([
        "scoreboard players set tick video 0\n",
        "fill 0 100 0 39 121 0 chiseled_bookshelf"
    ])

with open("generated_datapack/data/minecraft/tags/functions/load.json", "w") as file:
    file.write('{"values": ["video:load"]}')

with open("generated_datapack/data/minecraft/tags/functions/tick.json", "w") as file:
    file.write('{"values": ["video:dispatch"]}')

with open("generated_datapack/pack.mcmeta", "w") as file:
    file.write('{"pack": {"pack_format": 10, "description": "Plays a video with chiseled bookshelves"}, "features": {"enabled": ["update_1_20"]}}')
