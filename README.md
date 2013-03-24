Archiving and metadata extraction for F. Plooij's chimp audio recordings
---------

This repository contains scripts and other code developed in support of Frans Plooij's NESCent project "Translation of field notes for developmental study of chimpanzee vocal communication". 

NESCent Project
===============

Many researchers are interested in chimpanzee vocal communication, both as an important aspect of chimpanzee social behavior and as a source of insights into the evolution of human language. Nonetheless, very little is known about how chimpanzee vocal communication develops from infancy to adulthood. The largest dataset of recordings from free-living immature chimpanzees was recorded by the late Dr. Hetty van de Rijt-Plooij and Dr. Frans Plooij (International Research-institute on Infant Studies) at Gombe National Park, Tanzania (1971-73), but as these recordings were collected along with a large amount of other data, they have not yet been analyzed. In order to make this dataset available to more researchers, Dr. Plooij spent a short-term sabbatical fellowship at NESCent from March-April 2010, with the goal to translate and transcribe the original field notes on the contexts of the calls from Dutch into English.

The audio recordings were deposited by Dr Plooj with [Cornell Lab of Ornithology's MacAulay Library](http://macaulaylibrary.org/) in 2004, and in 2010 have begun to be digitized there. The contextual field notes by Dr. Plooij are key to other researchers' ability to properly reuse the recordings. The goal of this support project is to extract the translated field notes corresponding to each audio recording and associate them with the respective recording, together with other pertinent metadata. For archiving these at the MacAulay Library the metadata have to packaged into more generic metadata fields, because the metadata structures offered there for describing audio recordings are geared towards ornithology, and does accommodate the full structure of the chimp communication metadata.

Content
=======

* [Scripts used for initial file massaging](./FileMassaging/), developed using Mac OSX Automator workflow and Python 2.5 
* [Scripts for semi-automated parsing of text from observation files into CSV files](./ObservationParsing/), developed in Python 2.5 
* [Scripts for final spreadsheet production](./SpreadsheetProduction/), developed using Eclipse, PyDev, and Python 2.5

Copying and license
===================

> Scripts and code for archiving Frans Plooij's collection of audio-recordings and field notes of developmental chimpanzee vocal communication 

> Written in 2011 by Vladimir Gapeyev <vladimir.gapeyev@acm.org>

> To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this software to the public domain worldwide. This software is distributed without any warranty.
You should have received a copy of the CC0 Public Domain Dedication along with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
