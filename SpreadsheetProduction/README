An Eclipse/PyDev project with scripts for final spreadsheet production 
within the NESCent project "Metadata for Frans Plooij's Gombe chimp recordings". 

Copyright 2011 National Evolutionary Synthesis Center (NESCent).

This code comes as is, with no support, promises, guarantees, or claims of suitability for a particular purpose.  
Free to use for any purpose, at your own risk. 

                      -------------------------

CombineCSVs/src/gombe/combine/run_production.py -- combines multiple CSV files with observation logs into one CSV. 
  The date is read from the name of each input file and is transformed into year, month, day columns in the output. 
  
CombineCSVs/src/loadextract/loadextract.py  run_production()  -- cleans and transforms raw audio, observations, and biography 
   spreadsheets from the previous steps into (1) spreadsheets suitable for a repository deposition and (2) a metadata 
   spreadsheet for the Macaulay deposition of the audio recordings. 
   As an intermediate step, the data is loaded into an SQLite database.
   
To run either of these, open in Eclipse, adjust the hard-wired file paths, and run from within Eclipse. 

Developed with Python 2.5, requires simplejson 2.1.5 