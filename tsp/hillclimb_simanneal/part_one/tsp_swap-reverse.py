# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 11:39:06 2018

@author: T901
"""
import math
import random
from PIL import Image, ImageFont, ImageDraw

'''http://www.psychicorigami.com/2007/04/17/tackling-the-travelling-salesman-problem-part-one/'''
def cartesian_matrix(coords):
    '''create a distance matrix for the city coords
      that uses straight line distance'''
    matrix={}
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            dx,dy=x1-x2,y1-y2
            dist=math.sqrt(dx*dx + dy*dy)
            matrix[i,j]=dist
    return matrix

def read_coords(coord_file):
    coords=[]
    for line in coord_file:
        x,y=line.strip().split(',')
        coords.append((float(x),float(y)))
    return coords

def tour_length(matrix,tour):
    total=0
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        total+=matrix[city_i,city_j]
    return total

def all_pairs(size,shuffle=random.shuffle):
    '''generate all pairings of the numbers 
    from 0 to size as (i,j) tuples in a random order'''
    r1=list(range(size))
    r2=list(range(size))
    if shuffle:
        shuffle(r1)
        shuffle(r2)
    for i in r1:
        for j in r2:
            yield (i,j)
            
def swapped_cities(tour):
    '''generator to create all possible variations
      where two cities have been swapped'''
    for i,j in all_pairs(len(tour)):
        if i < j:
            copy=tour[:]
            copy[i],copy[j]=tour[j],tour[i]
            yield copy

def reversed_sections(tour):
    '''generator to return all possible variations 
      where the section between two cities are swapped'''
    for i,j in all_pairs(len(tour)):
        if i != j:
            copy=tour[:]
            if i < j:
                copy[i:j+1]=reversed(tour[i:j+1])
            else:
                copy[i+1:]=reversed(tour[:j])
                copy[:j]=reversed(tour[i+1:])
            if copy != tour: # no point returning the same tour
                yield copy
                
for tour in swapped_cities([1, 2, 3]):
    print(tour)
print('')
for tour in reversed_sections([1, 2, 3]):
    print(tour)
                
def write_tour_to_img(coords,tour,img_file):
    padding=20
    # shift all coords in a bit
    coords=[(x+padding,y+padding) for (x,y) in coords]
    maxx,maxy=0,0
    for x,y in coords:
        maxx=max(x,maxx)
        maxy=max(y,maxy)
    maxx+=padding
    maxy+=padding
    img=Image.new("RGB",(int(maxx),int(maxy)),color=(255,255,255))
    
    font=ImageFont.load_default()
    d=ImageDraw.Draw(img);
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        x1,y1=coords[city_i]
        x2,y2=coords[city_j]
        d.line((int(x1),int(y1),int(x2),int(y2)),fill=(0,0,0))
        d.text((int(x1)+7,int(y1)-5),str(i),font=font,fill=(32,32,32))
    
    
    for x,y in coords:
        x,y=int(x),int(y)
        d.ellipse((x-5,y-5,x+5,y+5),outline=(0,0,0),fill=(196,196,196))
    del d
    img.save(img_file, "PNG")
    
coords = [(0, 0), (1,0), (1, 1), (2, 3), (0, 5), (7, 5)]
scale = 20
coords = [(x*scale, y*scale) for x, y in coords]
write_tour_to_img(coords, [0, 1, 2, 3, 4], 'tsp_swap-reverse.png')

'''http://www.psychicorigami.com/2007/05/12/tackling-the-travelling-salesman-problem-hill-climbing/'''
