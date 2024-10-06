from arcgis.mapping import WebMap

def find_webmap(p_webmaps, webmap_title_name):
    if len(p_webmaps) == 0:
        wm = None
    #Find webmap
    elif len(p_webmaps) == 1 :
        wm = WebMap(p_webmaps[0])
    else :
        wm = None
        for p_webmap in p_webmaps:
            if p_webmap.title == webmap_title_name and p_webmap.type == "Web Map":
                wm = WebMap(p_webmap)
    return wm