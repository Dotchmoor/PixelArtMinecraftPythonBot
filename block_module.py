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

def get_best_block(block_color_values, img_array):
    block_list = [[[None] for x in y] for y in img_array]
    touse = {}

    
    for y in range(len(img_array)):
        touse[y] = {}
        for x in range(len(img_array[0])):
            touse[y][x] = 0

    tollerance = 1

    for line in range(len(img_array)):
        for pixel in range(len(img_array[line])):
            if block_list[line][pixel][0] == None:
                matchingblock = None
                possible_matching = {}
                p_read = img_array[line][pixel][2]
                p_green = img_array[line][pixel][1]
                p_blue = img_array[line][pixel][0]

                for key, value in block_color_values.items():    
                    if value["color"][0] > p_read-tollerance and value["color"][0] < p_read+tollerance and value["color"][1] > p_green-tollerance and value["color"][1] < p_green+tollerance and value["color"][1] > p_blue-tollerance and value["color"][1] < p_blue+tollerance:
                        possible_matching[key] = value["pixels"]
                print(f"{line}, {pixel}")
                print(touse[line])
                del touse[line][pixel]
                if len(touse[line]) < 1:
                    del touse[line]

                last = 0
                for key, value in possible_matching.items():
                    if value > last:
                        matchingblock = key
            block_list[line][pixel].append(matchingblock)

    
    while len(touse) > 0:
        tollerance += 15
        if line in touse:
            for line in range(len(img_array)):
                if pixel in touse[line]:
                    for pixel in range(len(img_array[line])):
                        if block_list[line][pixel][0] == None:
                            matchingblock = None
                            possible_matching = {}
                            p_read = img_array[line][pixel][2]
                            p_green = img_array[line][pixel][1]
                            p_blue = img_array[line][pixel][0]

                            print(p_read)

                            for key, value in block_color_values.items():    
                                if value["color"][0] > p_read-tollerance and value["color"][0] < p_read+tollerance and value["color"][1] > p_green-tollerance and value["color"][1] < p_green+tollerance and value["color"][1] > p_blue-tollerance and value["color"][1] < p_blue+tollerance:
                                    possible_matching[key] = value["pixels"]
                                    print(f"{line}, {pixel}")
                                    del touse[line][pixel]
                                    if len(touse[line]) < 1:
                                        del touse[line]

                            last = 0
                            for key, value in possible_matching.items():
                                if value > last:
                                    matchingblock = key
                        block_list[line][pixel].append(matchingblock)
                    print(line)
            
    return [[x[0] for x in y] for y in block_list]
