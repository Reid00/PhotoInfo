import requests
from pathlib import Path
import exifread

class GetPhotoInfo:
    def __init__(self,photo):
        self.photo=photo    
        # 百度地图ak
        self.ak='Ary6REVjBQvxnOndpt2XzqwLXzn4A689'
        self.location=self.get_photo_info()

    def get_photo_info(self):
        with open(self.photo,'rb') as f:
            tags=exifread.process_file(f)

        try:
            # print basic info
            print(f'拍摄时间: {tags["EXIF DateTimeOriginal"]}')
            print(f'照相机制造商: {tags["Image Make"]}')
            print(f'照相机型号: {tags["Image Model"]}')
            print(f'照片尺寸: {tags["EXIF ExifImageWidth"], tags["EXIF ExifImageLength"]}')

            #geolocation lat
            lat_ref=tags['GPS GPSLatitudeRef'].printable
            lat=tags['GPS GPSLatitude'].printable[1:-1].replace(' ','').replace('/',',').split(',')
            lat=float(lat[0]) + float(lat[1])/60 + float(lat[2])/ float(lat[3])/3600
            if lat_ref !='N':
                lat=lat * (-1)

            #geolocation lon
            lon_ref=tags['GPS GPSLongitudeRef'].printable
            lon=tags['GPS GPSLongitude'].printable[1:-1].replace(' ','').replace('/',',').split(',')
            lon=float(lon[0]) + float(lon[1])/60 + float(lon[2])/ float(lon[3])/3600
            if lon_ref !='E':
                lon=lon * (-1)

        except KeyError:
            return 'ERROR:请确保照片包含经纬度等EXIF信息。'
        else:
            print(f'lat,lon: {lat},{lon}')
            return lat,lon

    def get_location(self):
        url='http://api.map.baidu.com/reverse_geocoding/v3/?ak={}&output=json&coordtype=wgs84ll&location={},{}'.format(self.ak, *self.location)
        res = requests.get(url).json()

        status= res['status']
        if status ==0:
            address  = res['result']['formatted_address']
            print(f'detailed address:　{address}')
        else:
            print('baidu_map error happened ')


if __name__ == "__main__":
    photo=Path(r'D:\python\GitRepository\PhotoInfo\photos/632477919.jpg')
    Main=GetPhotoInfo(photo)
    Main.get_location()
