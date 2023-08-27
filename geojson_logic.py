import io
import math
import random
import cv2
import numpy as np
import geopandas as gpd
from shapely.geometry import MultiPolygon
from geojson import Polygon, Feature, dump


geojson_path = "test2.geojson"
gdf = gpd.read_file(geojson_path)


def load_contour_by_NAME_JA(name: str) -> np.ndarray:
    polygon = gdf[gdf["NAME_JA"] == name].iloc[0]["geometry"]
    if type(polygon) == MultiPolygon:
        polygons = polygon.geoms
        polygon = max(polygons, key=lambda p: p.area)
    return np.array(polygon.exterior.coords)

def get_rondom_country_data():
    random_index = random.randint(0, len(gdf) - 1)
    random_record = gdf.iloc[random_index]
    return random_record

def get_country_polygon(NAME_JA: str):
    country_contour = load_contour_by_NAME_JA(NAME_JA)
    feature = Feature(
        geometry=Polygon(coordinates=[country_contour.tolist()]), properties={}
    )
    string_buffer = io.StringIO()
    dump(feature, string_buffer)
    geojson_str = string_buffer.getvalue()
    string_buffer.close()
    return geojson_str


def compare_contour(name_ja1, name_ja2):
    country1_contour = load_contour_by_NAME_JA(name_ja1)
    country2_contour = load_contour_by_NAME_JA(name_ja2)
    similarity_score = cv2.matchShapes(
        country1_contour, country2_contour, cv2.CONTOURS_MATCH_I1, 0
    )
    return math.floor((100 - similarity_score) * 100)


# トルクメニスタン、ウズベキスタン、アフガニスタン、パキスタンの比較はわかりやすいかも
# country1_contour = load_contour_by_NAME_JA("オーストラリア")
# country2_contour = load_contour_by_NAME_JA("トルクメニスタン")

# similarity_score = cv2.matchShapes(
#     country1_contour, country2_contour, cv2.CONTOURS_MATCH_I1, 0
# )
# print(similarity_score)

# feature = Feature(
#     geometry=Polygon(coordinates=[country1_contour.tolist()]), properties={}
# )
# with open("output.geojson", "w") as f:
#     dump(feature, f, indent=2)
