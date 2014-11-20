python-homegate
===============

python-homegate (https://github.com/arteria/python-homegate) is a python library used to interact with Homegate (http://www.homegate.ch) using the IDX3.01 
API. python-homegate implements the official IDX3.01 API but is not an official library by Homegate. For all non python-homegate related issues, contracts, 
credentials, question regarding Homegate, etc. please contact Homegate AG directly! 

Use the issue tracking system for all pyhton-homegate related issues, bug reports, feature request, etc. 

Installation
============

If you want the latest stable version of python-homegate from PyPi, install using

	pip install homegate

Or, if you prefer to install the latest and greates commit from GitHub, install using

	pip install -e git+https://github.com/arteria/python-homegate.git#egg=homegate

You should know what you do by choosing the second option. ;-)


Usage
=====

NOT WORKING CURRENTLY - WORK IN PROGRESS!

Connect to Homegate

	>>> from homegate.homegate import Homegate, IdxRecord
	>>> hg = Homegate(MY_AGENCY_ID, HOST, USERNAME, PASSWORD)

Create an empty record and set/update data
	
	>>> rec = IdxRecord()
	>>> rec.update({'object_city':'Basel', 'object_country':'CH'})
	>>> rec.update({'picture_1_filename': '/Users/phi/Desktop/country-house.jpg', 'picture_1_title': 'Country house front view'}) 

Publish (push) to Homegate and disconnect

	>>> hg.push(rec)
	>>> del hg
	good bye
	>>>

Options
-------

Define a prefix for IdxRcords. This allows to have unique filenames for the FTP processing. The process is triggered 
three times a day (at 6h00, 12h00 and 18h00).	

	>>> rec_1234 = IdxRecord(prefix='1234-')
	
To push multiple records at once, pass a list of records.

	>>> rec_2345 = IdxRecord(prefix='2345-')
	>>> rec_3465 = IdxRecord(prefix='3456-')
	>>> hg.push([rec_1234, rec_2345, rec_3465])
 

Contribution
============

1. Fork the python-homegate repository
2. Make your well commented and clean commits to the repository
3. Send a pull request (https://help.github.com/articles/using-pull-requests)


TODO
====

* WIP: Type and length validation for each field
* 

Changelog
=========

0.0.2
-----

* Added convert to X functions for automatic type and length conversion of fields in an IDX record.
* 

0.0.1
-----

arteria GmbH open sourced the initial working version of [python-homegate](https://github.com/arteria/python-homegate) allowing to push real estate objects and property to Homegate using the IDX3.01 API.
