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

                    print(use, highestnum)
                    jsondata[block.split(".")[0].replace("_top", "")] = use

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