import requests
from .utils import measureDistance
from .models import ObjAddress

class Controller:
    def __init__(self):
        self.addressList = []

    def addAddress(self, strStreet, strNumber, strCity, strState, strCEP):
        address = ObjAddress(strStreet, strNumber, strCity, strState, strCEP)
        self.addressList.append(address)


    def processAddresses(self):
        strKeyOpenCage = '60a91a7e7e514c2fa9502f125df630ac'
        strKeyOpenRouteService = '5b3ce3597851110001cf624814fa90b79c5e4dc0bc616727d6994085'

        # Obtenção das coordenadas geográficas dos endereços
        for address in self.addressList:
            address.get_location(strKeyOpenCage)

        origin = self.addressList[0]
        destinations = self.addressList[1:]

        orderedAddresses = [origin]

        # Cálculo das distâncias e ordenação dos endereços
        while destinations:
            minDistance = float('inf')
            closestDestination = None

            for destination in destinations:
                distance = measureDistance(origin.latitude, origin.longitude, destination.latitude, destination.longitude,
                                           strKeyOpenRouteService)
                if distance and distance < minDistance:
                    minDistance = distance
                    closestDestination = destination

            if closestDestination:
                orderedAddresses.append(closestDestination)
                origin = closestDestination
                destinations.remove(closestDestination)
            else:
                break

        return orderedAddresses
