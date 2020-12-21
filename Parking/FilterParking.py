'''
A translation function for Greenville city shp parking data . 

The following fields are used:    

Field           Used For            Reason
FEAT_CODE          -



Constant fields:
amenity=parking
parking=surface  (most are surface, will be changed for parking garage)

'''

import re

    
def filterTags(attrs):
    if not attrs:
        return

    tags = {}

    tags['amenity'] = 'parking'
    tags['parking'] = 'surface'

    return tags