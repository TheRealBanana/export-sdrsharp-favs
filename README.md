# export-sdrsharp-favs
Python script to export the Frequency Manager favorites in SDR# to a format that can be imported into SDR++

I couldn't find any scripts on the internet that did this job so I made my own. I would have put it into a gist but I don't think those are indexed by Google very well and I want it to be found when searching for how to export sdrsharp favorites.

A couple important points:

First, SDR++ doesn't let you import or export all your groups at once, you can only import or export a single group at a time.
This would have meant that all the favorites would have been jumbled into a single group, which I didn't want. This script saves each group to a separate file. Then in SDR++ you need to create the new group manually before you import the json file into that group.

Second, SDR++ just instantly crashes when the json file has weird data in it, so be warned that if you have special characters in the favorite names they may cause issues. Also if any of the group names in SDRSharp have invalid filename characters in them, that will also break things.

Other than that, all you need to do is put your Frequencies.xml file into the same folder as this script and then run it. On Windows the path to my Frequencies.xml file was:

C:\SDRSharp\Instances\Profile1\Frequencies.xml

If you have multiple profiles you may have to open each Frequencies.xml file until you find the correct one.
