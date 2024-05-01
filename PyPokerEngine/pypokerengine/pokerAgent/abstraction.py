import numpy as np

class Abstraction:
    def tpt_table():
        HR = []
        with open("pypokerengine/pokerAgent/HandRanks.dat", "rb") as fin:
            HR_data = fin.read()
            HR_bytes = np.frombuffer(HR_data, dtype=np.uint32)
            HR[:len(HR_bytes)] = HR_bytes
        
        HR_zip={}
        for i,v in enumerate(HR):
            HR_zip[i]=v    
        return HR_zip           # Hand of the Agent
