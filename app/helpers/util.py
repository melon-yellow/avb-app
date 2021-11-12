
#################################################################################################################################################

# Imports
import os
import json

#################################################################################################################################################

# Get File-Paths
fileDir = os.path.dirname(os.path.abspath(__file__))
path = os.path.abspath(os.path.join(fileDir, './util.json'))

#################################################################################################################################################

# Write Util
def write(data):
    json.dump(data, open(path, 'w'))

#################################################################################################################################################

# Read Util
class read:

    # Util Laminador
    def laminador():
        r = dict()
        default = [None, None]
        gets = json.load(open(path, 'r'))
        time = gets.get('mill', default)[0]
        util = gets.get('mill', default)[1]
        c = time != None and util != None
        r['UTIL'] = util / (time if time > 0 else 1) if c else None
        r['TEMPO_PARADO'] = ((time - util) / 60) if c else None
        return r

    #################################################################################################################################################
    
    # Util Trefila
    def trefila():
        # Open File
        default = [None, None, None, None, None, None]
        gets: dict = json.load(open(path, 'r'))
        time = gets.get('trf', default)[0]
        # Parse Util
        def parseUtil(mq):
            r = dict()
            util = gets.get('trf', default)[mq]
            c = time != None and util != None
            r['UTIL'] = util / (time if time > 0 else 1) if c else None
            r['TEMPO_PARADO'] = ((time - util) / 60) if c else None
            return r
        # Return Util Dictionary
        return {
            'SEC': time,
            'm01': parseUtil(1),
            'm02': parseUtil(2),
            'm03': parseUtil(3),
            'm04': parseUtil(4),
            'm05': parseUtil(5),
        }

#################################################################################################################################################
