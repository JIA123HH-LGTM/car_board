import json
import time
from .getPublicData import *

def getBaseData():
    cars = list(getAllCars())
    sumCar = len(cars)
    topCar = cars[0].carName
    hightVolume = cars[0].saleVolume
    #车型
    carModels = {}
    maxModel= 0
    mostModel = ''
    for i in cars:
        if carModels.get(i.carModel,-1) == -1:
            carModels[str(i.carModel)] = 1
        else:
            carModels[str(i.carModel)] += 1
    carModels = sorted(carModels.items(), key=lambda x: x[1], reverse=True)
    mostModel = carModels[0][0]
    #品牌
    carBrands = {}
    maxBrand = 0
    mostBrand = ''
    for i in cars:
        if carBrands.get(i.brand,-1) == -1:
            carBrands[str(i.brand)] = 1
        else:
            carBrands[str(i.brand)] += 1
    for k,v  in carBrands.items():
        if v > maxBrand:
            maxBrand = v
            mostBrand = k
    #价格
    carPrice = {}
    averagePrice = 0
    sumPrice = 0
    for i in cars:
        x = json.loads(i.price)[0] + json.loads(i.price)[1]
        sumPrice += x
        averagePrice = sumPrice / (sumCar * 2)
        averagePrice = round(averagePrice, 2)
    return sumCar,topCar,hightVolume,mostModel,mostBrand,averagePrice

def getRollData():
    cars = list(getAllCars())
    #品牌
    carBrands = {}
    for i in cars:
        if carBrands.get(i.brand,-1) == -1:
            carBrands[str(i.brand)] = 1
        else:
            carBrands[str(i.brand)] += 1
    brandList = [(value,key) for key,value in carBrands.items()]
    brandList.sort(reverse=True)
    brandList = brandList[:10]
    sortDict = {i[1]: i[0] for i in brandList}
    lastSortList = []
    for k,v in sortDict.items():
        lastSortList.append({
            'name' : k,
            'value' :v
        })
    return lastSortList

def getTypeRate():
    cars = list(getAllCars())
    carTypes = {}
    #能源类型
    for i in cars:
        if carTypes.get(i.energyType,-1) == -1:
            carTypes[str(i.energyType)] = 1
        else:
            carTypes[str(i.energyType)] += 1
    oilRate = round(carTypes['汽油'] / len(cars) * 100,2)
    electricRate = round(carTypes['纯电动'] / len(cars) * 100,2)
    otherRate = round(((len(cars) - carTypes['汽油']-carTypes['纯电动']) / len(cars) * 100),2)
    return oilRate,electricRate,otherRate
