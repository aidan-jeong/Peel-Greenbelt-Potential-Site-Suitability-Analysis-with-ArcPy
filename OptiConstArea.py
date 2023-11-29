# -*- coding: utf-8 -*-
# ---------------------------------------------------------------
# opti_const_area.py
# Created on: 2022-11-23
# Description: This script is used for the execution of the
# Optimal Constructible Area Analyzer Tool
# ---------------------------------------------------------------

#  **************************** Imports ***************************************
import arcpy
# ************************* Variable Setup ************************************

# Manually sets the workspace to the default workspace (gdb) of the project.
user_workspace = arcpy.env.scratchWorkspace
arcpy.env.workspace = user_workspace

# To allow overwriting outputs, change overwriteOutput option to True
arcpy.env.overwriteOutput = True

# Gets Area of Interest Input (Polygon Layer)
area_of_interest = arcpy.GetParameterAsText(0)

# Gets Area to be erased from the area of interest (Vector Data)
area_to_be_erased = arcpy.GetParameterAsText(1)

# Gets the DEM (Raster Layer)
dem_layer = arcpy.GetParameterAsText(2)

# Gets the preferred slope to be used for the analysis from the user.
preferred_slope = arcpy.GetParameterAsText(3)

# Gets the road network (Vector data)
road_network = arcpy.GetParameterAsText(4)

# Gets the preferred distance from roads to be used for the analysis from the user.
distance_from_roads = arcpy.GetParameterAsText(5)

# Gets the facilities (Vector data)
points_of_interest = arcpy.GetParameterAsText(6)

# Gets the preferred distance from facilities to be used for the analysis from the user.
distance_from_facilities = arcpy.GetParameterAsText(7)

# Gets the location where the output feature class (Raster Layer) should go from the user
output_layer = arcpy.GetParameterAsText(8)

# **************************** Analysis ***************************************

# Step 1: Erases unsuitable area from area of interest
if arcpy.Exists(area_to_be_erased):
    erased_area =  arcpy.analysis.Erase(in_features= area_of_interest, erase_features= area_to_be_erased, out_feature_class= user_workspace, cluster_tolerance= "")
else: 
    erased_area = area_of_interest
arcpy.AddMessage("Step 1: AOI Erase Complete. (1/9)")

# Step 2: Uses Extract by mask to make the DEM to be the extent of the area of interest
extracted_DEM = arcpy.sa.ExtractByMask(in_raster= dem_layer, in_mask_data= erased_area, extraction_area= "INSIDE", analysis_extent= "")
arcpy.AddMessage("Step 2: DEM EbM Complete. (2/9)")

# Step 3: Calculates the slope of the extracted dem
slope_Raster = arcpy.sa.Slope(in_raster= extracted_DEM, output_measurement="PERCENT_RISE", z_factor=1, method="GEODESIC", z_unit="METER")
arcpy.AddMessage("Step 3: Slope Complete. (3/9)")

# Step 4: Calculates the good cells in the slope raster using con tool.
slope_con_raster = arcpy.sa.Con(in_conditional_raster= slope_Raster, in_true_raster_or_constant= 1, in_false_raster_or_constant= 0, where_clause="VALUE <= {0}".format(str(preferred_slope)))
arcpy.AddMessage("Step 4: Slope-Con Complete. (4/9)")

# Step 5: Performs Euclidean distance on the point layer
POI_Euclidean = arcpy.CreateScratchName("", "", "featureclass", user_workspace)
with arcpy.EnvManager(extent= extracted_DEM, snapRaster=extracted_DEM):
    Euclidean_Distance_POI = arcpy.sa.EucDistance(in_source_data= points_of_interest, maximum_distance=None, cell_size= extracted_DEM, out_direction_raster= "", distance_method="GEODESIC", in_barrier_data="", out_back_direction_raster= "")
    Euclidean_Distance_POI.save(POI_Euclidean)
arcpy.AddMessage("Step 5: POI EUC Complete. (5/9)")

# Step 6: Does Con analysis for the facilities point layer
facility_con_layer = arcpy.sa.Con(in_conditional_raster= POI_Euclidean, in_true_raster_or_constant= 1, in_false_raster_or_constant= 0, where_clause="VALUE <= {0}".format(str(distance_from_facilities)))
arcpy.AddMessage("Step 6: POI EUC-CON Complete. (6/9)")

# Step 7: Performs Euclidean distance on the road layer.
Road_Euclidean = arcpy.CreateScratchName("", "", "featureclass", user_workspace)
with arcpy.EnvManager(extent= extracted_DEM, snapRaster= extracted_DEM):
    Euclidean_Distance_Road = arcpy.sa.EucDistance(in_source_data= road_network, maximum_distance=None, cell_size= extracted_DEM, out_direction_raster= "", distance_method="GEODESIC", in_barrier_data="", out_back_direction_raster= "")
    Euclidean_Distance_Road.save(Road_Euclidean)
arcpy.AddMessage("Step 7: Road EUC Complete. (7/9)")

# Step 8: Does Con analysis for the road layer
road_con_layer = arcpy.sa.Con(in_conditional_raster= Road_Euclidean, in_true_raster_or_constant= 1, in_false_raster_or_constant= 0, where_clause="VALUE <= {0}".format(str(distance_from_roads)))
arcpy.AddMessage("Step 8: Road EUC-CON Complete. (8/9)")

# Step 9: Gets the final layer after intersecting all the layers using raster calculator
Raster_Calculator = arcpy.CreateScratchName("", "", "featureclass", user_workspace)
Raster_Calculator = slope_con_raster *  facility_con_layer *  road_con_layer
Raster_Calculator.save(output_layer)
arcpy.AddMessage("Step 9: Raster Calc. Complete. (9/9)")

# *************************** Temporary files removal **************************

# Deletes the temporary point features created from the workspace
removal_list = [erased_area, extracted_DEM, slope_Raster, slope_con_raster, Euclidean_Distance_POI, POI_Euclidean, Road_Euclidean, facility_con_layer, Euclidean_Distance_Road, road_con_layer]
for file in removal_list:
    if arcpy.Exists(file):
        arcpy.management.Delete(file)

# Updates the user that temporary files have been deleted.
arcpy.AddMessage("Deleted Temporary files")

# Updates the user that the process was completed successfully.
arcpy.AddMessage("Processing completed successfully.")