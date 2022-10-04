import os
import sys
import gdal
from osgeo import ogr
from osgeo import osr

#Get argvs
density = sys.argv[1]
estiasi = sys.argv[2]
parking = sys.argv[3]
pois = sys.argv[4]
transport = sys.argv[5]
uid = sys.argv[6]

#Import gdal_calc
gdal_path = r"C:\OSGeo4W64\apps\Python37\Scripts"
gdal_calc_path = os.path.join(gdal_path, 'gdal_calc.py')

#Import gdal_proximity
gdal_proximity_path = os.path.join(gdal_path, 'gdal_proximity.py')

# Assign workspace - sript dir
workspace = os.path.dirname(os.path.realpath(__file__))

# Inputs rasters workspace
rasters_path = os.path.join(workspace, 'rasters')

#Tiffs public folder workspace
tiffs_path = os.path.join(workspace, 'tiffs')

#New file to store geoTiff
pathGeoTiff = os.path.join(tiffs_path, str(uid))
os.mkdir(pathGeoTiff)

#Raster Calculator inputs
agora_estiasi_raster = os.path.join(rasters_path, '01_AGORA_ESTIASI.tif')
pois_raster = os.path.join(rasters_path, '02_POIS.tif')
pop_density_raster = os.path.join(rasters_path, '03_POP_DENSITY.tif')
parking_raster = os.path.join(rasters_path, '04_PARKING.tif')
transport_raster = os.path.join(rasters_path, '05_TRANSPORT.tif')
result = os.path.join(pathGeoTiff, str(uid) + ".tif")
calc = '"(A*{1})+(B*{3})+(C*{0})+(D*{2})+(E*{4})"'.format(density, estiasi, parking, pois, transport) # weighted data

#Raster calculator command 1 - compine the two rasters to one
gdal_calc = 'python {0} ' \
            '-A {1} ' \
            '-B {2} ' \
            '-C {3} ' \
            '-D {4} ' \
            '-E {5} ' \
            '--outfile={6} ' \
            '--calc={7} ' \
            '--type=Float32 ' \
            '--overwrite'.format(gdal_calc_path, agora_estiasi_raster, pois_raster, pop_density_raster, parking_raster, transport_raster, result, calc)

#Run raster calculator 1
os.system(gdal_calc)

#Create EPSG:2100 Greek Grid Spatial Reference
sr = osr.SpatialReference()
sr.ImportFromEPSG(2100)

# open raster in writing mode
ds = gdal.Open(result, 1)

# set spatial reference
ds.SetProjection(sr.ExportToWkt())

# save raster
ds = None

#Cliped raster
result_cliped = os.path.join(pathGeoTiff, str(uid) + "_wgs84.tif")

#Boundary of AOI for clip
#boundary_shp = os.path.join(shp_path, 'boundary.shp')

#GDAL Warp - Clip raster to shp
options = gdal.WarpOptions(dstSRS='EPSG:4326')
outBand = gdal.Warp(srcDSOrSrcDSTab=result, destNameOrDestDS=result_cliped, options=options)

outBand= None

#Get max pixel value fron clipped raster
tiff = gdal.Open(result, 1)
tiff_band = tiff.GetRasterBand(1)

stats = tiff_band.GetStatistics(True, True) #max value --> 0 - max gia klimaka plotty

print(stats[1])
