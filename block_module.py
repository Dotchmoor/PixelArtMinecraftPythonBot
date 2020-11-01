import json, os, random, cv2

class json_manager():
    def __init__(self, datapath):
        self.path = datapath
        self.blockdic = {}

    def create_file(self, block_pic_width, block_pic_height):
        blockpath = os.path.join(self.path, "blocks")

        #data
        if "block_color_values.json" not in os.listdir(self.path):
            jsondata = {}

            with open(os.path.join(self.path, "block_color_values.json"), 'w') as jsonfile:
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
    block_list = []
    linecount = 0

    for line in img_array:
        block_list.append([])
        for pixel in line:
            p_read = pixel[2]
            p_green = pixel[1]
            p_blue = pixel[0]

            matchingblock = None
            possible_matching = {}
            
            #alle bei denen die Werte um maximal 10 schwanken werden in possible matching gepackt
            for key, value in block_color_values.items():    
                if value["color"][0] > p_read-50 and value["color"][0] < p_read+50 and value["color"][1] > p_green-50 and value["color"][1] < p_green+50 and value["color"][1] > p_blue-50 and value["color"][1] < p_blue+50:
                    possible_matching[key] = value["pixels"]

            print(possible_matching)
            last = 0
            for key, value in possible_matching.items():
                if value > last:
                    matchingblock = key
                
            
            block_list[linecount].append(matchingblock)
        linecount += 1
        
    
    return block_list
