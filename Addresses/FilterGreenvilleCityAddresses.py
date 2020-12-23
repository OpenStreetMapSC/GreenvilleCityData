'''
A translation function for Greenville SC City shp address data (Addresses.*). 

GIS Dictionary:

FULLADDRES: Housenumber + street; Unit Type and Unit shown  in separate fields
UNITTYPE:Type of unit if applicable (Apt, Basement, Clubhouse, Half, Lobby, Office, Room, Suite Unit)
UNIT:Unit character if applicable
ZIPCODE:Zipcode
FEAT_CODE:Address type (Accessory, ATM, Billboard, Cell Tower, Comm/Industrial, 
  Group Quarters, Mixed Use, Other, Park, Parking Lot, Parking Structure, Residential, 
  Residential-Multi, School, Temporary, Unknown, Utility  Structure)
STATUS:Address status  (Active, Temp)



STATUS=temp addresses are dropped

The following fields are used:    

Field           Used For            Reason

addr:street taken from -
FULLADDRES     addr:housenumber + addr:street

UNIT            addr:unit
ZIPCODE         addr:postcode


Fixed field assignment:

addr:city       Greenville    // Because these addresses are limited to the city of greenville
addr:state      SC

'''

import re

def translateName(rawname,warn):
    '''
    A general purpose name expander.
    '''
    suffixlookup = {
    'Aly':'Alley',
    'Anx':'Annex',
    'Ave':'Avenue',
    'Av':'Avenue',
    'Br':'Branch',
    'Blf':'Bluff',
    'Commons':'Commons',
    'Trace':'Trace',
    'Hollow':'Hollow',
    'Springs':'Springs',
    'East':'East',
    'West':'West',
    'Hill':'Hill',
    'Acres':'Acres',
    'Farms':'Farms',
    'Dipper':'Dipper',
    'South':'South',
    'Shed':'Shed',
    'Road':'Road',
    'Promenade':'Promenade',
    'Town':'Town',
    'Hillcrest':'Hillcrest',
    'Byp':'Bypass',
    'Rd':'Road',
    'Hts':'Heights',
    'St':'Street',
    'Pl':'Place',
    'Hl':'Hill',
    'Holw':'Hollow',
    'Pk':'Park',
    'Cres':'Crescent',
    'Blvd':'Boulevard',
    'Dr':'Drive',
    'Dwns':'Downs',
    'Ext':'Extension',
    'Ext.':'Extension',
    'Pkwy':'Parkway',
    'Pky':'Parkway',
    'Lndg':'Landing',
    'Xing':'Crossing',
    'Lane':'Lane',
    'Cv':'Cove',
    'Crt':'Court',
    'Trl':'Trail',
    'Tr':'Trail',
    'Ter':'Terrace',
    'Terr':'Terrace',
    'Trac':'Trace',
    'Trc':'Trace',
    'Trce':'Trace',
    'Vly':'Valley',
    'Xovr':'Crossover',
    'Gr':'Grove',
    'Grv':'Grove',
    'Ln':'Lane',
    'Lk':'Lake',
    'Cl':'Close',
    'Cv':'Cove',
    'Cir':'Circle',
    'Ct':'Court',
    'Est':'Estate',
    'Rl':'Real',
    'Rdg':'Ridge',
    'Plz':'Plaza',
    'Pne':'Pine',
    'Pte':'Pointe',
    'Pnes':'Pines',
    'Pt':'Point',
    'Ctr':'Center',
    'Rwy':'Railway',
    'Div':'Diversion',
    'Mnr':'Manor',
    'Hwy':'Highway',
    'Hwy':'Highway',
    'Conn': 'Connector',
    'Chase': 'Chase',
    'Vw': 'View',
    'View': 'View',
    'Cliff': 'Cliff',
    'Walk': 'Walk',
    'Knob': 'Knob',
    'Gate': 'Gate',
    'Grove': 'Grove',
    'Path': 'Path',
    'Trail': 'Trail',
    'Place': 'Place',
    'Real': 'Realignment',
    'Pass': 'Pass',
    'Row': 'Row',
    'Way': 'Way',
    'Farm': 'Farm',
    'Run': 'Run',
    'Drive': 'Drive',
    'Loop': 'Loop',
    'Line': 'Line',
    'Sq': 'Square',
    'Pointe': 'Pointe',
    'Greene': 'Greene',
    'Ridge': 'Ridge',
    'Park': 'Park',
    'Yard': 'Yard',
    'End': 'End',
    'Gln': 'Glen',
    'E':'East',
    'S':'South',
    'N':'North',
    'W':'West'}
	
    newName = ''
    for partName in rawname.split():
        trns = suffixlookup.get(partName,partName)
        if (trns == partName):
            if (partName not in suffixlookup) and (not partName.isnumeric()):
                if warn:
                    print ('Unknown suffix translation - ', partName)
        newName = newName + ' ' + trns

    return newName.strip()


# Only apply translation to first and last word
def translateFullName(rawname):
    newName = ''
    nameParts = rawname.split()
    for idx, partName in enumerate(nameParts):
        if idx == 0:
            partName = translatePrefix(partName)
        elif idx == (len(nameParts)-1):
            partName = translateName(partName,True)
        newName = newName + ' ' + partName

    return newName.strip()


def translatePrefix(rawname):
    '''
    Directional name expander.
    '''
    prefixLookup = {
        'O':'Old',
        'N':'New',
        'NW':'NorthWest',
        'NE':'NorthEast',
        'SE':'SouthEast',
        'SW':'SouthWest',
        'E':'East',
        'S':'South',
        'N':'North',
        'W':'West'}

    newName = ''
    for partName in rawname.split():
        newName = newName + ' ' + prefixLookup.get(partName,partName)

    return newName.strip()


# Convert from 22Nd to 22nd
def CorrectNumberedCapitalization(rawname):
    newName = ''
    for partName in rawname.split():
        word = partName
        if (word[0].isdigit()):
            word = word.lower()
        newName = newName + ' ' + word

    return newName.strip()

#see if type was apecified in both base STREETNAME and on type
#For example Oak Street Street
def CheckDoubleType(rawName):
    newName = rawName
    nameParts = rawName.split()
    numberOfParts = len(nameParts)
    if numberOfParts >= 3:
        testSuffix = translateName(nameParts[numberOfParts-2],False)
        lastWord = nameParts[numberOfParts-1]
        if (lastWord == testSuffix):
            del nameParts[-1]  # remove last element
            nameParts[numberOfParts-2] = testSuffix # replace last word with expanded word
            newName = ' '.join(nameParts)

    return newName.strip()


    
def filterTags(attrs):

    if not attrs:
        return

    tags = {}
    
    if 'STATUS' in attrs:
        status = attrs['STATUS'].strip()
        if status == 'TEMP':
            return tags;

    if 'FULLADDRES' in attrs:
        fulladdress = attrs['FULLADDRES'].strip()  # housenumber + street
        nameParts = fulladdress.split()
        numberOfParts = len(nameParts)
        if numberOfParts >= 2:
            housenumber = nameParts[0]
            #print (' housenumber - ', housenumber)
            if housenumber == '0':
                return  tags # Placeholder address?

            tags['addr:housenumber'] = housenumber
            nameParts.pop(0)  # remove housenumber
            roadName = ' '.join(nameParts)
            roadName = translateFullName(roadName.title())
            roadName = roadName.strip()
            roadName = CorrectNumberedCapitalization(roadName)
            roadName = re.sub("\s\s+", " ", roadName)  # Remove multiple spaces
            roadName = CheckDoubleType(roadName)
            if roadName != '':
                tags['addr:street'] = roadName
        
        
    if 'UNIT' in attrs:
        unit  = attrs['UNIT'].strip()
        unit = re.sub("\s\s+", " ", unit)  # Remove multiple spaces
        if unit != "":
            tags['addr:unit'] = unit

    if 'ZIPCODE' in attrs:
        zip = attrs['ZIPCODE'].strip()
        if zip != '':
            tags['addr:postcode'] = zip

    tags['addr:city'] = 'Greenville'
    tags['addr:state'] = 'SC'

    return tags
