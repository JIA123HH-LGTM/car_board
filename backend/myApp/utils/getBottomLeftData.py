import json
import time
import re
from .getPublicData import *

def getSquareData():
    cars = list(getAllCars())
    carsVolume = {}
    for i in cars:
        if carsVolume.get(i.carName,-1) == -1:
            carsVolume[i.carName] = int(i.saleVolume)
        else:
            carsVolume[i.carName] += int(i.saleVolume)
    sorted_carsVolume = sorted(carsVolume.items(), key=lambda item: item[1], reverse=True)[:15]
    brandList = []
    volumeList = []
    priceList = []
    for i in sorted_carsVolume:
        brandList.append(i[0])
        volumeList.append(i[1])
    for j in cars[:15]:
        j.price = re.findall('\d+\.\d+', j.price)
        j.price = j.price[0]
        priceList.append(float(j.price))
    return brandList, volumeList, priceList
