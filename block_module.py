import json, os, random, cv2

class json_manager():
    def __init__(self, datapath):
        self.path = datapath
        self.blockdic = {}

    def create_file(self, block_pic_width, block_pic_height):
        
        #data
        if "block_color_values.json" not in os.listdir(self.path):
            jsondata = {}

            with open(os.path.join(self.path, "block_color_values.json"), 'w') as jsonfile:
                blockpath = os.path.join(self.path, "blocks")
                for block in os.listdir(blockpath):
                    average = {}
                    activeblock = cv2.imread(os.path.join(blockpath, block))
                    
                    for line in activeblock:
                        for pixel in line:
                            if (int(pixel[2]), int(pixel[1]), int(pixel[0])) not in average:
                                average[(int(pixel[2]), int(pixel[1]), int(pixel[0]))] = 1
                            else:
                                average[(int(pixel[2]), int(pixel[1]), int(pixel[0]))] += 1
                    
                    use = None
                    highestnum = 0
                    for key, value in average.items():
                        if value > highestnum:
                            highestnum = value
                            use = key 

                    jsondata[block.split(".")[0].replace("_top", "").replace("_bottom", "")] = {"color":use, "pixels":highestnum}

                self.blockdic = jsondata
                json.dump(jsondata, jsonfile, indent=4)
            
    def load_dic(self):
        with open(os.path.join(self.path, "block_color_values.json"), "r") as file:
            self.blockdic = json.load(file)
    
    def get_dic(self):
        return self.blockdic

def generate_commands(blocklist):
    commands = []
    
    x = 0
    y = -10
    z = 0
    
    for line in blocklist:
        z += 1
        x = 0
        for block in line:
            commands.append(f"/setblock ~{x} ~{y} ~{z} {block}")
            x += 1
        x = 0
    return commands

def compare(tollerance, rgb_list_1, rgb_list_2):
    rv = rgb_list_1[0] - rgb_list_2[0]
    gv = rgb_list_1[1] - rgb_list_2[1]
    bv = rgb_list_1[2] - rgb_list_2[2]

    if rv < 0:
        rv = rv * -1
    if gv < 0:
        gv = gv * -1
    if bv < 0:
        bv = bv * -1
    
    if rv <= tollerance and gv <= tollerance and bv <= tollerance:
        return True
    else:
        return False

def get_best_block(block_color_values, img_array):
    block_list = [[[None] for x in y] for y in img_array]
    
    leftspots = {}

    tollerance = 1

    for line in range(len(img_array)):
        leftspots[line] = {}
        for pixel in range(len(img_array[0])):
            leftspots[line][pixel] = 0

    print(block_color_values)
    for line in range(len(img_array)):
        for pixel in range(len(img_array[0])):
            for block in block_color_values:
                while compare(tollerance, block_color_values[block]["color"], [img_array[line][pixel][2], img_array[line][pixel][1], img_array[line][pixel][0]]) == False:
                    tollerance += 1
                else:
                    block_list[line][pixel][0] = block

    return [[x[0] for x in y] for y in block_list]

    
    
