# Imports
import numpy as np
import pandas as pd
from shapely.geometry import Point, MultiPoint, LineString, Polygon
import geopandas as gpd


def extract_coordinates(line: str) -> tuple:
    """
    Function used to extract coordinates from a string in the form x,y\n read from a txt file
    1. Convert the line into a list using the split method
    2. Select the first element in the list (which should be the x coordinate) and convert it into a float type
    3. Select the second element in the list (which should be the y coordinate), slice it until the last element (-1 - \n)
    and convert it into a float number

    The function returns a tuple in the form (x,y)
    """
    pair = line.split(",")
    x = float(pair[0])
    y = float(pair[1][:-1])
    coordinates = (x, y)
    return coordinates


def txt_to_vector_layer(txt_filepath: str, dst_filepath: str = None, driver: str = None, geom_type="Point",
                        epsg=4326) -> gpd.GeoDataFrame:
    """
    Function created to convert a txt file to a simple vector layer

    :param txt_filepath: Filepath to the txt file
    :param dst_filepath: None The vector layer's output filepath in case of saving
    :param driver: None The vector layer's driver in case of saving
    :param geom_type: Point The geometry type of the vector layer
    :param epsg: 4326 The Coordinate Reference System of the layer
    :return: GeoPandas GeoDataFrame of and output file
    """
    # Open the txt file
    with open(txt_filepath) as txt_file:
        lines = txt_file.readlines()
        txt_file.close()

    coords_list = []  # empty list

    for line in lines:
        coord_pair = extract_coordinates(line)
        coords_list.append(coord_pair)

    if geom_type == "Point":  # Point geometry vector layer

        geometry = pd.Series(coords_list).apply(Point)
        df = pd.DataFrame({"geometry": geometry})
        gdf = gpd.GeoDataFrame(df, crs=epsg)

        return gdf.to_file(dst_filepath, driver=driver) if dst_filepath else gdf

    elif geom_type == "MultiPoint":  # MultiPoint geometry vector layer

        geometry = MultiPoint(coords_list)
        df = pd.DataFrame({"geometry": [geometry]})
        gdf = gpd.GeoDataFrame(df, crs=epsg)

        return gdf.to_file(dst_filepath, driver=driver) if dst_filepath else gdf

    elif geom_type == "LineString":  # LineString geometry vector layer

        geometry = LineString(coords_list)
        df = pd.DataFrame({"geometry": [geometry]})
        gdf = gpd.GeoDataFrame(df, crs=epsg)

        return gdf.to_file(dst_filepath, driver=driver) if dst_filepath else gdf

    elif geom_type == "Polygon":  # Poygon geometry vector layer

        if coords_list[0] == coords_list[-1]:
            geometry = Polygon(coords_list)
            df = pd.DataFrame({"geometry": [geometry]})
            gdf = gpd.GeoDataFrame(df, crs=epsg)

            return gdf.to_file(dst_filepath, driver=driver) if dst_filepath else gdf

        else:
            raise Exception("To construct a Polygon geometry, make sure the first and last point are identical")


def csv_to_vector_layer(csv_filepath: str, x_column: str, y_column: str, dst_filepath=None, driver=None,
                        geom_type="Point", epsg=4326):

    """
    Function to create a vector layer from a csv file.
    :param csv_filepath: path corresponding to the csv file
    :param x_column: column containing longitude values
    :param y_column: column containing latitude values
    :param dst_filepath: If wanted, path to export the file
    :param driver: driver to export the file
    :param geom_type: geometry type
    :param epsg: EPSG code of the geometry
    :return:
    """
    if geom_type == "Point":
        df = pd.read_csv(csv_filepath)
        geometry = gpd.points_from_xy(df[x_column], df[y_column], crs=epsg)
        gdf = gpd.GeoDataFrame(df, geometry=geometry)

        return gdf

    elif geom_type == "LineString":
        df = pd.read_csv(csv_filepath)
        geometry = gpd.points_from_xy(df[x_column], df[y_column], crs=epsg) # GeometryArray 1D
        geometry = LineString(geometry)

        gdf = gpd.GeoDataFrame({"tipo":["cuenca"], "geometry":[geometry]})

        return gdf

# txt_to_vector_layer(
#     txt_filepath="C:\\Users\\orden\\Desktop\\Codigo\\data\\Cuenca_Parana.txt",
#     dst_filepath="C:\\Users\\orden\\Desktop\\Codigo\\data\\Polygon_Cuenca_Parana.shp",
#     driver="Shapefile",
#     geom_type="Polygon"
# )

gdf = csv_to_vector_layer("C:\\Users\\orden\\Desktop\\Codigo\\data\\Cuenca_Parana.csv", "Longitud", "Latitud", geom_type="LineString")

print(gdf)

# df_cuenca_parana_point["geometry"] = df_cuenca_parana_point["geometry"].apply(Point)
#
# gdf_cuenca_parana_point = gpd.GeoDataFrame(df_cuenca_parana_point, geometry="geometry", crs=4326)

# POLYLINE (LINESTRING)

# 1° opcion
# df_cuenca_parana_line = pd.DataFrame({"nombre":"Cuenca Paraná", "geometry":[cuenca_parana]})
# df_cuenca_parana_line["geometry"] = df_cuenca_parana_line["geometry"].apply(LineString)

# 2° opcion
# cca_parana_linestring = LineString(cuenca_parana)
# df_cuenca_parana_line = pd.DataFrame({"nombre":"Cuenca Paraná", "geometry":[cca_parana_linestring]})

# gdf_cuenca_parana_line = gpd.GeoDataFrame(df_cuenca_parana_line, geometry="geometry", crs=4326)
# gdf_cuenca_parana_line.to_file("C:/Users/Orden/Downloads/Cuenca_Parana.shp")

# POLYGON

# 1° opcion
# df_cuenca_parana_polyg = pd.DataFrame({"nombre":"Cuenca Paraná", "geometry":[cuenca_parana]})
# df_cuenca_parana_polyg["geometry"] = df_cuenca_parana_polyg["geometry"].apply(Polygon)

# 2° opcion
# cca_parana_polyg = Polygon(cuenca_parana)
# df_cuenca_parana_polyg = pd.DataFrame({"nombre":"Cuenca Paraná", "geometry":[cca_parana_polyg]})

# gdf_cuenca_parana_polyg = gpd.GeoDataFrame(df_cuenca_parana_polyg, geometry="geometry", crs=4326)
# gdf_cuenca_parana_polyg.to_file("C:/Users/Orden/Downloads/Cuenca_Parana_Polyg.shp")
