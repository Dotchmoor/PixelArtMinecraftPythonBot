import cv2, os, random, keyboard, time
import block_module

#paths
mainpath = os.path.dirname(__file__)
datapath = os.path.join(mainpath, "data")
imgpath = os.path.join(datapath, "images")

#block width and height
blockwidth = 16
blockheight = 16

#data
json_blockcolors = block_module.json_manager(datapath)
json_blockcolors.create_file(blockwidth, blockheight)

#img array
chosenimg = random.choice(os.listdir(imgpath))
img = cv2.imread(os.path.join(imgpath, chosenimg)) 

print(chosenimg)
print(img)

json_blockcolors.load_dic()
block_data = json_blockcolors.get_dic()
blocklist = []
linecount = 0

for line in img:
    blocklist.append([])
    for pixel in line:
        for key, value in block_data.items():
            if pixel[2]-value[0] <= 30 and pixel[1]-value[1] <= 30 and pixel[0]-value[2] <= 30:
                blocklist[linecount].append(key)
                break

    linecount += 1

print(blocklist)

toplace = block_module.generate_commands(blocklist)

print("click in minecraft text")
time.sleep(5)
for entry in toplace:
    if keyboard.is_pressed('q') == False:
        keyboard.write(entry)
        keyboard.press_and_release('enter')
        keyboard.press_and_release('t')
        time.sleep(0.1)
