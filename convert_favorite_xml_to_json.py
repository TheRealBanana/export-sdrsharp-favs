import os, os.path, json
import xml.etree.ElementTree as ET

filepath = "./Frequencies.xml"
outfolder = "./jsonout/"

#List index is the type id for SDR++ json
#Text is the DetectorType in SDRsharp xml
SDRPP_DEMOD_TYPE_LIST = [
    "NFM",
    "WFM",
    "AM",
    "DSB",
    "USB",
    "CW",
    "LSB",
    "RAW"
]

def startparse():
    #For funzies
    totalfavs = 0
    #First lets make sure this is a valid frequency list from sdrsharp's frequency manager
    #We expect the first root tag to be "ArrayOfMemoryEntry"
    tree = ET.parse(filepath)
    root = tree.getroot()
    if root.tag != "ArrayOfMemoryEntry":
        raise(Exception("XML file was not of the expected structure. Canceling operation."))
    
    #Ok Now we know this is a good favorites file, we can start to process the file one entry at a time.
    #SDRSharp separates lists into groups, similar to SDR++. However SDR++ only lets you import or export a single
    #group at a time. To work around this we will save each group into its own json file, and the end user
    #will just create a new group before importing that separate json file.
    
    #Lucky for us the mode type names in SDR++ and SDRSharp are identical!  \o/
    
    favorites = {}
    for mement in root: 
        tmpdata = {}
        #Each MemoryEntry has our information we need in it.
        #Start parsing the tags for this favorite entry
        for datatag in mement:
            tmpdata[datatag.tag] = datatag.text
        
        #For brevity
        grp = tmpdata["GroupName"]
        favname = tmpdata["Name"]
        
        if grp not in favorites:
            favorites[grp] = {}
        
        if favname in favorites[grp]: #Skip duplicate
            print("Found a duplicate entry in the group %s for the favorite named: '%s'" % (grp, favname))
            continue
        else:
            favorites[grp][favname] = {}
            
        #Ok we have a good parse on a favorite and we can save that into our favorites dict
        favorites[grp][favname] = tmpdata
        totalfavs += 1
        
    createjson(favorites, totalfavs)
    
def createjson(favoritesdict, totalfavs):
    #Now we have all our favorites in a nice data format we can save that data into a json file(s) for later importation
    #The json format makes this soooo easy, we just have to arrange our dictionary in the correct way.
    #Each SDR++ favorites json dict starts with the key "bookmarks"
    #Then each subkey from "bookmarks" is the name of the favorite and its data is the information
    #The data keys are:
    # ['bandwidth', 'frequency', 'mode']
    
    # SDR++     /  SDRSharp
    #------------------------------
    # bandwidth = FilterBandwidth
    # frequency = Frequency
    # mode = DetectorType
    
    #Check output folder exists or create it
    if not os.path.exists(outfolder):
        print("Output folder '%s' does not exist, creating it..." % outfolder)
        try:
            os.mkdir(outfolder)
        except:
            raise(Exception("Couldn't find the output folder '%s' and couldn't make a new one. Make sure the path is valid and has proper user permissions." % outfolder))
    
    os.chdir(outfolder)
    for GROUP in favoritesdict:
        #This will blow up if any group names contain invalid filename characters just fyi
        outfilename = "%s.json" % GROUP
        outdict = {}
        outdict["bookmarks"] = {}
        bm = outdict["bookmarks"] #more brevity
        for FAVNAME in favoritesdict[GROUP]:
            favdata = favoritesdict[GROUP][FAVNAME]
            bm[FAVNAME] = {
                'bandwidth': float(favdata["FilterBandwidth"]), #SDR++ expects these two to be floats
                'frequency': float(favdata["Frequency"]),
                'mode': SDRPP_DEMOD_TYPE_LIST.index(favdata["DetectorType"])
            }
        
        with open(outfilename, 'w') as outjson:
            outjson.write(json.dumps(outdict))
        
        print("Wrote out favorites file: %s" % outfilename)
    print("\n\nFinished processing Frequencies.xml. Found a total of %s favorite frequencies" % totalfavs)
    

if __name__ == "__main__":
    startparse()
    
