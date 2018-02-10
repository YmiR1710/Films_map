def coordinates_detector(place):
    """
    str -> tuple
    Function returns coordinates of some place
    """
    try:
        import geopy
        from geopy.geocoders import Nominatim
        geolocator = Nominatim()
        location = geolocator.geocode(place)
        return location.latitude, location.longitude
    except:
        return None

def place_type_detector(place):
    """
    str -> str
    Function returns type of some place
    """
    try:
        import geopy
        from geopy.geocoders import Nominatim
        geolocator = Nominatim()
        location = geolocator.geocode(place)
        return location.raw.get("type")
    except:
        return None

def location_list(path):
    """
    str -> list
    Function creates list according to this format: [film name, film year, place]
    """
    try:
        f = open(path)
        loc_lst = []
        for line in f:
            if line.startswith('"'):
                lst = ["", "", ""]
                indicator = 0
                if "{" in line:
                    for i in line:
                        if i == "(":
                            indicator = 1
                        if i == ")":
                            indicator = 2
                        if i == "}":
                            indicator = 3
                        if indicator == 0:
                            lst[0]+=i
                        if indicator == 1:
                            lst[1]+=i
                        if indicator == 2:
                            k = 0
                        if indicator == 3:
                            lst[2]+=i
                    lst[0] = lst[0].strip()
                    lst[1] = lst[1][:5]
                    lst[1] = lst[1][1:]
                    lst[2] = lst[2][1:].strip()
                else:
                    for i in line:
                        if i == "(":
                            indicator = 1
                        if i == ")":
                            indicator = 2
                        if indicator == 0:
                            lst[0]+=i
                        if indicator == 1:
                            lst[1]+=i
                        if indicator == 2:
                            lst[2]+=i
                    lst[0] = lst[0].strip()
                    lst[1] = lst[1][1:].strip()
                    lst[2] = lst[2][1:].strip()
                loc_lst.append(lst)
        return loc_lst
    except:
        return None

def map_creator(year, type_layer):
    """
    str, str -> None
    Main Function
    """
    try:
        import folium
        map_list = []
        map = folium.Map()
        for i in location_list("location.list"):
            if i[1] == year:
                map_list.append(i)
        tp = folium.FeatureGroup()
        dm = folium.FeatureGroup(​)
        for i in map_list:
            dm.add_child(folium.Marker(location = coordinates_detector(i[3]),
            popup = i[0]))
            tp.add_child(folium.Marker(location = coordinates_detector(i[3]),
            popup = i[0] + " is" + place_type_detector(i[2])))
        if type_layer == "+":
            map.add_child(tp)
            map.add_child(dm)
        else:
            map.add_child(dm)
        map.save('Film_map.html')
    except:
        return None

year = input("print the year of films creation ")
type_ind = input("do you want to add type layer? print '+' if yes and '-' if no ")
map_creator(year, type_ind)
