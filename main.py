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
img = cv2.imread(os.path.join(imgpath, random.choice(os.listdir(imgpath))))
json_blockcolors.load_dic()
block_data = json_blockcolors.get_dic()
blocklist = []

blocklist = block_module.get_best_block(block_data, img)

print(len(blocklist), len(blocklist))
toplace = block_module.generate_commands(blocklist)
print(toplace)
print("click in minecraft text")
time.sleep(5)
for entry in toplace:
    if keyboard.is_pressed('q') == False:
        keyboard.write(entry)
        keyboard.press_and_release('enter')
        keyboard.press_and_release('t')
        time.sleep(0.085)

keyboard.press_and_release('esc')