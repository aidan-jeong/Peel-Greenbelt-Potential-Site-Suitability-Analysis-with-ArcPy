# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-11-26 21:34:45
"""
import arcpy

def PeelRegionClip():  # Peel Region Clip

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    GREENBELT_OUTER_BOUNDARY = "GREENBELT_OUTER_BOUNDARY"
    RegionOfPeelBoundary = "RegionOfPeelBoundary"

    # Process: Clip (Clip) (analysis)
    InAOI = "C:\\Users\\coolm\\Documents\\UOFT\\2022,2023 Fall\\GGR321 Geographical Information Processing\\GGR321 Group Project\\Group Project.gdb\\InAOI"
    with arcpy.EnvManager(extent="-80.1440925245988 43.4813674915032 -79.5393300562071 43.9897619327103 GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]", outputCoordinateSystem="PROJCS["NAD_1983_UTM_Zone_17N",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-81.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]"):
        arcpy.analysis.Clip(in_features=GREENBELT_OUTER_BOUNDARY, clip_features=RegionOfPeelBoundary, out_feature_class=InAOI, cluster_tolerance="")

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\Users\coolm\Documents\UOFT\2022,2023 Fall\GGR321 Geographical Information Processing\GGR321 Group Project\Group Project.gdb", workspace=r"C:\Users\coolm\Documents\UOFT\2022,2023 Fall\GGR321 Geographical Information Processing\GGR321 Group Project\Group Project.gdb"):
        PeelRegionClip()
