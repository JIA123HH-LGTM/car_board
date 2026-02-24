from django.http import JsonResponse
from django.shortcuts import render
from .utils import getPublicData
from .utils import getCenterData
from .utils import getCenterLeftData
from .utils import getBottomLeftData
from .utils import getCenterRightData
from .utils import getCenterChangeData
from .utils import getBottomRightData
from .utils import getCenterLeft2Data

# Create your views here.

def center(request):
    if request.method == 'GET':
        sumCar,topCar,hightVolume,mostModel,mostBrand,averagePrice = getCenterData.getBaseData()
        lastSortList = getCenterData.getRollData()
        oilRate,electricRate,otherRate = getCenterData.getTypeRate()
        return JsonResponse({
            'sumCar':sumCar,
            'topCar':topCar,
            'hightVolume':hightVolume,
            'mostModel':mostModel,
            'mostBrand':mostBrand,
            'averagePrice':averagePrice,
            'lastSortList':lastSortList,
            'oilRate':oilRate,
            'electricRate':electricRate,
            'otherRate':otherRate
        })

def centerLeft(request):
    if request.method == 'GET':
        SortList = getCenterLeftData.getPieBrandData()
        return JsonResponse({
            'SortList':SortList,
        })

def bottomLeft(request):
    if request.method == 'GET':
        brandList, volumeList, priceList = getBottomLeftData.getSquareData()
        return JsonResponse({
            'brandList':brandList,
            'volumeList':volumeList,
            'priceList':priceList
        })

def centerLeft2(request):
    if request.method == 'GET':
        modelList, volumeList = getCenterLeft2Data.getCarModelData()
        return JsonResponse({
            'modelList':modelList,
            'volumeList':volumeList,
        })


def centerRight(request):
    if request.method == 'GET':
        realData = getCenterRightData.getPriceSortData()
        return JsonResponse({
            'realData':realData
        })

def centerRightChange(request,energyType):
    if request.method == 'GET':
        oilData, electricData = getCenterChangeData.getCircleData()
        realData = []
        if energyType == 1:
            realData = oilData
        else:
            realData = electricData
        return JsonResponse({
            'realData':realData
        })

def bottomRight(request):
    if request.method == 'GET':
        carData = getBottomRightData.getRankData()
        return JsonResponse({
            'carData':carData
        })