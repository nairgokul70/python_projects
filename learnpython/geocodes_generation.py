__author__ = 'gokul.nair'
import urllib
import simplejson
import csv
import time

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'

def get_coordinates(query):
    params = {
        'address': query
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
    else:
        latitude, longitude = None, None
        print query, "<no results>"
    return latitude,longitude


with open('C:\\development\\talend\\workspace\\geocodes_customer.csv') as geocodes_csv:
     reader = csv.reader(geocodes_csv,delimiter=';')
     #headers = reader.next()
     for row1,row2,row3 in reader:
         time.sleep(1)
         latitude = get_coordinates(row2)[0]
         longitude = get_coordinates(row2)[1]
         geocodesvalue = row1+'',row2+'',row3+'',str(latitude)+'',str(longitude)+''
         with open('C:\\development\\talend\workspace\\geocodes.csv','a') as geocodes_output:
                writer = csv.writer(geocodes_output,delimiter=';',lineterminator='\n')
                writer.writerow(geocodesvalue)