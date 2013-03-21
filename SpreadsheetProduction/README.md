Archiving and metadata extraction for F. Plooij's chimp audio recordings
---------

An Eclipse/PyDev project with scripts for final spreadsheet production. 

* ``CombineCSVs/src/gombe/combine/run_production.py`` combines multiple CSV files with observation logs into one CSV. 
  The date is read from the name of each input file and is transformed into year, month, day columns in the output. 
  
* ``CombineCSVs/src/loadextract/loadextract.py run_production()`` cleans and transforms raw audio, observations, and biography 
   spreadsheets from the previous steps into
  1. spreadsheets suitable for a repository deposition and
  2. a metadata spreadsheet for the Macaulay deposition of the audio recordings. As an intermediate step, the data is loaded into an SQLite database.
   
To run either of these, open in Eclipse, adjust the hard-wired file paths, and run from within Eclipse. 

Developed with Python 2.5, requires simplejson 2.1.5 

Copying and license
===================

> Scripts and code for archiving Frans Plooij's collection of audio-recordings and field notes of developmental chimpanzee vocal communication 

> Written in 2011 by Vladimir Gapeyev <vladimir.gapeyev@acm.org>

> To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this software to the public domain worldwide. This software is distributed without any warranty.
You should have received a copy of the CC0 Public Domain Dedication along with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
