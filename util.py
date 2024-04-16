import numpy as np
import ujson

class Qtable(dict):
    """
    dictionary-like object
    All keys have default value 0
    """    
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)
    
    def save(self,filepath):
        json_obj = ujson.dumps(self, indent=4)
        with open(filepath, "w") as outfile:
            outfile.write(json_obj)
            
    def load(self,filepath):
        self.clear()
        with open(filepath, "r") as openfile:
            json_obj = ujson.load(openfile)
        for key in json_obj:
            self[key] = json_obj[key]
    
def randomChoice(arr, Myseed = None):
    if Myseed != None:
        np.random.seed(Myseed)
    return arr[np.random.randint(len(arr))]