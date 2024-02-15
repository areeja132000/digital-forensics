import exifread
import sys

def GPS_converter(GPSLatLong):
  temp = str(GPSLatLong)[1:-1]
  temp_list = temp.split(", ")
  index_for_division = temp_list[2].find("/")
  return int(temp_list[0]), float(temp_list[1]), int(temp_list[2][:index_for_division])/int(temp_list[2][index_for_division+1:])

filename = ''
if len(sys.argv) > 1:
  filename = sys.argv[1]
else:
  print("Error! - No Image File Specified!")
  exit()

# Open image file for reading (binary mode)
try:
  f = open(filename, 'rb')
except IOError:
  print("Error! - File Not Found!")
  exit()

# Return Exif tags
tags = exifread.process_file(f)
print("Source File: {}".format(filename))
print("Make: {}".format(tags['Image Make']))
print("Model: {}".format(tags['Image Model']))
print("Original Date/Time: {}".format(tags['Image DateTime']))
lat_degs, lat_mins, lat_secs = GPS_converter(tags['GPS GPSLatitude'])
if (str(tags['GPS GPSLatitudeRef']) != 'N'):
  lat_degs = lat_degs*-1
print("Latitude: {} degrees, {} minutes, {} seconds".format(lat_degs, lat_mins, lat_secs))
long_degs, long_mins, long_secs = GPS_converter(tags['GPS GPSLongitude'])
if (str(tags['GPS GPSLongitudeRef']) != 'E'):
  long_degs = long_degs*-1
print("Longitude: {} degrees, {} minutes, {} seconds".format(long_degs, long_mins, long_secs))