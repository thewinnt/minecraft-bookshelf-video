from PIL import Image

commands = []
dispatch_cmd = []

for i in range(1, 4384, 4):
    if len(str(i)) == 1:
        name = "00" + str(i)
    elif len(str(i)) == 2:
        name = "0" + str(i)
    else:
        name = i
    img = Image.open(f"frames/{name}.jpg")
    for x in range(40):
        for y in range(22):
            c1 = str(sum(img.getpixel((479 - (x * 12 + 8), 359 - (y * 16 + 8)))) > 375).lower() # approx
            c2 = str(sum(img.getpixel((479 - (x * 12 + 4), 359 - (y * 16 + 8)))) > 375).lower()
            c3 = str(sum(img.getpixel((479 - (x * 12), 359 - (y * 16 + 8)))) > 375).lower()
            c4 = str(sum(img.getpixel((479 - (x * 12 + 8), 359 - (y * 16)))) > 375).lower()
            c5 = str(sum(img.getpixel((479 - (x * 12 + 4), 359 - (y * 16)))) > 375).lower()
            c6 = str(sum(img.getpixel((479 - (x * 12), 359 - (y * 16)))) > 375).lower()
            commands.append(f"setblock {x} {100 + y} 0 chiseled_bookshelf[slot_0_occupied={c1},slot_1_occupied={c2},slot_2_occupied={c3},slot_3_occupied={c4},slot_4_occupied={c5},slot_5_occupied={c6}]\n")
    with open(f"output/{i}.mcfunction", "w+") as file:
        file.writelines(commands)
    commands = []
    dispatch_cmd.append(f"execute if score tick badapple matches {i} run function minecraft:output/{i}\n")
with open("dispatch.mcfunction", "w+") as file:
    file.writelines(dispatch_cmd)