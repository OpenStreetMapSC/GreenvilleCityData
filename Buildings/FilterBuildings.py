'''
A translation function for Greenville city shp building footprint data . 

The following fields are used:    

Field           Used For            Reason
FEATCODE:Type of building = (
          20 yes Comm/Industrial ** Catch-all, 
          21 apartments Residential-Multi,  
          22 detached Residential,
          23 yes Mixed Use, 
          24 school School, 
          25 yes Parking Structure, 
          26 yes Courtyard,   *** Garage / utility shed?
          27 yes Future LUCA,   ** Construction
          ?? yes Group Quarters,
          28 yes Other,  ?? Other tiny structure such as kiosk
          ?? yes Temporary,  ?? Used?
          30 yes Under Construction)

FAC_LABEL:Label for building purpose when applicable - Not used
HEIGHT: Estimated heights of building in meters (Estimate methodology uses either 
                Pictometry tools or number of stories indicated on permit)
                ** Not usable since it uses mixed feet and meter values with no units



Constant fields:

Translation:
source       tags
HEIGHT       Height in meters (1 decimal)


'''

import re

    
def filterTags(attrs):
    if not attrs:
        return

    tags = {}

    buildingType='yes'
    if 'FEATCODE' in attrs:
        featureCode = attrs['FEATCODE'].strip()
        if featureCode == '21':
            buildingType = 'apartments'
        elif featureCode == '22':
            buildingType = 'detached'
        elif featureCode == '24':
            buildingType = 'school'
    tags['building'] = buildingType

    if 'HEIGHT' in attrs:
        height = attrs['HEIGHT'].strip()
        # tags['height'] = height   ** Not useful; mixed feet and meters

    return tags
