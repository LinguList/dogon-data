import folium
import pickle
from collections import defaultdict
from lingpy.convert.html import colorRange
from lingpy import *
import sys

def addpoly(feature, color, where, lon, lat, group, radius=5):
    print(feature, color, where, lon, lat)
    coords = float(lat), float(lon)
    folium.RegularPolygonMarker(coords,
            number_of_sides=6,
            fill_color=color,
            radius=radius,
            color=color,
            popup=feature + ' ('+group+')',
            ).add_to(where)

groups = {}
languages = csv2list('Dogon-Borrow.tsv', strip_lines=False)

colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c",
        "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928" ] + colorRange(11) + [ "red", "purple", "cornflowerblue", "yellow", "#008000",
                "Orange"][::-1]
#colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c",
#        "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", '#040404', '#F6E3CE',
#        '#81F79F', '#8A0808', '#FA58F4', '#0489B1', '#088A08'] + colorRange(11)

colorbygroup = []
for row in languages[1:]:
    rows = dict(zip(languages[0], row))
    groups[rows['NAME']] = rows
    colorbygroup += [rows['SUBGROUP']]

colorbygroup = sorted(set(colorbygroup))
colorit = {}
for i, group in enumerate(colorbygroup):
    colorit[group] = colors[i]


worldmap = folium.Map(tiles="stamenwatercolor")
for lang, vals in groups.items():
    addpoly(lang, colorit[vals['SUBGROUP']], worldmap,
            vals['LON'], vals['LAT'],vals['SUBGROUP'], radius=10)
            
worldmap.save('map.html')
