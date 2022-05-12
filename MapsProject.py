import os.path
import requests
from requests import get
import json
import numpy
import time
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing

FILE_NAME="destination.txt"
key="9F4XPc6uXF6WmrQYRJYAgLrxITlCGF48"
google_key="AIzaSyDOGZGtIwI5wgeDVBTHJ7biV-CEmh-hQPk"

class Coordinates:
    def __init__(self,lat,long):
        self.lat=lat
        self.long=long

    def __repr__(self):
        return " '% s-% s'" % (self.lat, self.long)

def print_matrix(matrix):
    for i in matrix:
        print(i)

def get_data():
    file=open(FILE_NAME)
    if not os.path.isfile(FILE_NAME):
        print('File does not exist.')
    else:
        with open(FILE_NAME) as f:
            content = f.read().splitlines()
    tappe=[]
    for line in content:
        tappe.append(line)
    return tappe

def place_to_LatLong(tappe):
    start=time.time()
    print("Converto i luoghi in coordinate")
    lat_long_tappe=[]
    for t in tappe:
        url = "https://www.mapquestapi.com/geocoding/v1/address?key="+key+"&inFormat=kvp&outFormat=json&location="+t+"&thumbMaps=false"
        response = get(url)
        response=response.json()
        lat_long=Coordinates(response["results"][0]["locations"][0]["displayLatLng"]["lat"],response["results"][0]["locations"][0]["displayLatLng"]["lng"])
        lat_long_tappe.append(lat_long)

    end=time.time()
    print("Processo terminato,tempo richiesto:"+str(end-start))
    print()
    return lat_long_tappe

def coordinates_to_string(latLng):
    source="from="
    source+=str(latLng[0].lat)+","+str(latLng[0].long)
    #print(source)

    dest=""
    for i in latLng[1:]:
        dest+="&to="
        dest+=str(i.lat)+","+str(i.long)
        #print(dest)

    return source,dest

def crete_matrix(source,dest):
    start=time.time()
    print("Creo la matrice di distanze")
    url="http://www.mapquestapi.com/directions/v2/routematrix?key=9F4XPc6uXF6WmrQYRJYAgLrxITlCGF48&ambiguities=ignore&doReverseGeocode=false&outFormat=json&routeType=fastest&unit=k&allToAll=true&"+source+dest
    #print(url)
    r = requests.get(url)
    x = r.json()
    #print(x)
    matrix=[]
    if(x["info"]["statuscode"]==0):
        for i in x["distance"]:
            row=[]
            for j in i:
                row.append(float(j))
            matrix.append(row)
        #print_matrix(matrix)
    else:
        print(x["info"]["statuscode"])
        print(x["info"]["messages"])

    end=time.time()
    print("Processo terminato,tempo richiesto:"+str(end-start))
    print()
    return matrix

def print_permutation(permutation,steps):
    print("Il percorso migliore è:")
    n=len(permutation)
    for i in permutation[0:n-1]:
        print(steps[i]+"->",end='')
    print(str(steps[permutation[n-1]]))

taps=get_data()
#print(taps)
latLng_taps=place_to_LatLong(taps)
#print(latLng_taps)
source,dest=coordinates_to_string(latLng_taps)
matrix=crete_matrix(source,dest)
#print_matrix(matrix)
dist_matrix=numpy.array([numpy.array(xi) for xi in matrix])

print("Calcolo il percorso migliore")
start=time.time()
permutation, distance = solve_tsp_dynamic_programming(dist_matrix)
print_permutation(permutation,taps)
end=time.time()
print("Tempo rischiesto:"+str(end-start))
print()

print("Calcolo il percorso migliore in modo euristico")
strat=time.time()
permutation_he, distance_he = solve_tsp_simulated_annealing(dist_matrix)
print_permutation(permutation_he,taps)
end=time.time()
print("Tempo rischiesto:"+str(end-start))
