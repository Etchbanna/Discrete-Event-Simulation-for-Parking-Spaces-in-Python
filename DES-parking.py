import numpy as np
import pandas as pd
import random
import simpy
import math
import time


header=['occupancy','slot_id']

df=pd.DataFrame(columns=header)
df.to_csv('parkings_s.csv',index=False)
CARS_IN_PARKING=0
CLOSEST_SPACES={"A1":["NONE",0],"A2":["NONE",0],"A3":["NONE",0],"A4":["NONE",0],"A5":["NONE",0],"A6":["NONE",0],"A7":["NONE",0],"A8":["NONE",0],"A9":["NONE",0],"A10":["NONE",0],"B1":["NONE",0],"B2":["NONE",0],
"B3":["NONE",0],"B4":["NONE",0],"B5":["NONE",0],"B6":["NONE",0],"B7":["NONE",0],"B8":["NONE",0],"B9":["NONE",0],"B10":["NONE",0]}
no_of_arrivals=3




def Generate_Car(env):
    global CARS_IN_PARKING
    while True:
        next_car = int(random.gauss(4,1))
        yield env.timeout(next_car)
        name=random.randint(1,25)
        CARS_IN_PARKING+=1
        for key in CLOSEST_SPACES.keys():
            if CLOSEST_SPACES[key][0]=="NONE":
                CLOSEST_SPACES[key][0]=name
                CLOSEST_SPACES[key][1]=1
                break
            else:
                continue
        print(CLOSEST_SPACES)
        env.process(Depart_Car(env,name))
    


def Depart_Car(env,name):
    global CARS_IN_PARKING
    yield env.timeout(int(random.gauss(50,10)))
    CARS_IN_PARKING-=1
    for key in CLOSEST_SPACES.keys():
        if CLOSEST_SPACES[key][0]==name:
            CLOSEST_SPACES[key][0]="NONE"
            CLOSEST_SPACES[key][1]=0
            break
    print(CLOSEST_SPACES)

def UpdateRecords(env):
    while True:
        for key in CLOSEST_SPACES.keys():
            data= {
                'occupancy':CLOSEST_SPACES[key][1],
                'slot_id':key


            }
            df=pd.DataFrame([data])
            df.to_csv('parkings_s.csv', mode='a', index = False,header=False)
        yield env.timeout(1)




random.seed(1000)



env = simpy.Environment()
env.process(Generate_Car(env))
env.process(UpdateRecords(env))

env.run()

