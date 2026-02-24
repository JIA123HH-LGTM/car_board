import json
from .getPublicData import *


def getCarModelData():
    cars = list(getAllCars())
    # 用于累加各车型类别的销量
    modelVolume = {}

    for car in cars:
        model = car.carModel  # 车型类别，如"中型SUV"
        volume = int(car.saleVolume)

        if modelVolume.get(model, -1) == -1:
            modelVolume[model] = volume
        else:
            modelVolume[model] += volume

    # 转换为两个数组
    modelList = []  # 车型类别数组
    volumeList = []  # 销量数组

    for model, volume in modelVolume.items():
        modelList.append(model)
        volumeList.append(volume)

    return modelList, volumeList