import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

map = folium.Map(location=[39.0997, -94.5786],
                 zoom_start=5, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")
fgp = folium.FeatureGroup(name="population")

html = """
<h4>Volcano Name: TEST </h4>
<a href= "https://www.google.com/search?q=%%22%s%%22" target = "_blank"> %s </a> <br>
Height: %s m
"""


def elevation_color(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation <= 3000:
        return 'orange'
    else:
        return 'red'


fgp.add_child(folium.GeoJson(
    data=open('world.json', 'r', encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] <= 30000000 else 'red'}))

for lt, ln, elv, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (
        name, name, elv), width=175, height=100)
    fgv.add_child(folium.CircleMarker(
        location=[lt, ln], radius=10, color='white', fill=True, fill_color=elevation_color(elv), popup=folium.Popup(iframe), opacity=10, fill_opacity=1))


map.add_child(fgp)
map.add_child(fgv)
map.add_child(folium.LayerControl())
map.save("index.html")
