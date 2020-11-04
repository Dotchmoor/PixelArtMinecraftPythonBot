import json, os, random, cv2

class block_manager():
    def __init__(self, folder_with_blocks):
        self.block_path = folder_with_blocks
        self.block_dic = {}

        #data
        if "block_color_values.json" not in os.listdir(self.block_path):
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

                    jsondata[block.split(".")[0].replace("_top", "").replace("_bottom", "").replace("_side", "").replace("_inside", "")] = {"color":use, "pixels":highestnum}

                self.blockdic = jsondata
                json.dump(jsondata, jsonfile, indent=4)
        
        with open(os.path.join(self.block_path, "block_color_values.json"), "r") as file:
            self.blockdic = json.load(file)
    
    def get_data(self):
        return self.blockdic

class pixel_img:
    def __init__(self, img_list, block_color_values):
        self.blocks_to_img = self.__get_best_suiting_block(block_color_values, img_list)
        print(self.blocks_to_img)
        self.command_list = self.__generate_commands(self.blocks_to_img)
    
    def get_command_list(self):
        return self.command_list
    
    def __get_best_suiting_block(self, block_color_values, img_list):
        block_list = [[[None] for x in y] for y in img_list]
        
        leftspots = {}
        for line in range(len(img_list)):
            leftspots[line] = {}
            for pixel in range(len(img_list[0])):
                leftspots[line][pixel] = 0

        print(leftspots)

        print(block_color_values)
        tollerance = 1 
        while len(leftspots) > 0:
            
            for line in range(len(img_list)):
                print(line, pixel, "new line")
                if line in leftspots:
                    for pixel in range(len(img_list[0])):   
                        print(line, pixel, "new pixel")
                        try:
                            if pixel in leftspots[line]:   
                                for block in block_color_values:
                                    if self.__compare(tollerance, block_color_values[block]["color"], [img_list[line][pixel][2], img_list[line][pixel][1], img_list[line][pixel][0]]) == True:
                                        block_list[line][pixel][0] = block
                                        del leftspots[line][pixel]
                                        if len(leftspots[line]) < 1:
                                            del leftspots[line]
                                        print(img_list[line][pixel], block_color_values[block]["color"])
                                        break
                        except KeyError:
                            print(leftspots)
                            print("Key Error", line, pixel)
                            print(KeyError)
            tollerance += 10
            print(tollerance)

        return [[x[0] for x in y] for y in block_list]

    def __compare(self, tollerance, rgb_list_1, rgb_list_2):
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

    def __generate_commands(self, blocklist):
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
