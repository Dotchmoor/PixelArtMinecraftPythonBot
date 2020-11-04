import cv2, os, random, keyboard, time
import twod_block_module

#paths
mainpath = os.path.dirname(__file__)
datapath = os.path.join(mainpath, "data")
imgpath = os.path.join(datapath, "images")

#block width and height
blockwidth = 16
blockheight = 16

#data
json_blockcolors = twod_block_module.block_manager(datapath)

#img array
img = cv2.imread(os.path.join(imgpath, random.choice(os.listdir(imgpath))))
twod_pixel_map = twod_block_module.pixel_img(img, json_blockcolors.get_data())
com_list = twod_pixel_map.get_command_list()

print("click in minecraft text")
time.sleep(5)
for entry in com_list:
    if keyboard.is_pressed('q') == False:
        keyboard.write(entry)
        keyboard.press_and_release('enter')
        keyboard.press_and_release('t')
        time.sleep(0.085)

keyboard.press_and_release('esc')
