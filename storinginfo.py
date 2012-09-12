
# How to store information

# This code can be considered part of the public domain, for any use by anyone.


# every "information_dict" parameter is a dictionary of key/value information
# "information_list" is a list of values for storage, no keys

# Note that when you open files with the 'w' parameter,
	# you will OVERWRITE the previously written file.
	# to append only, open with 'a'.

# CSV
def store_as_csv(information):
	import csv

	# Note: for opening a file, use 'a' and 'w' as necessary,
	# and keep in mind whether your code will write all the
	# informatoin at once upon opening the file or will open
	# and close it for each line of information


	# For 1 and 2, need to be careful that if using ','.join, quoted
	# strings won't be escaped

	#option 1:
	with open('outfile.csv', 'a') as outfile:
		outfile.write(','.join(information_list))

	#option 2: writing lines one at a time
	outfile = open('outfile.csv', 'a')
	outfile.write(','.join(information_list)) # must take list
	outfile.close()

	# option 3 and 4 are better, since they take care of everything for you

	# option 3
	w = csv.writer(open('outfile.csv', 'w'))
	w.writerow(information_list) # must take a list!

	# option 4, csv takes care of headers and order
	w = csv.DictWriter(open('outfile.csv', 'w'),
			fieldnames=['field1', 'field2', 'myfield'])
	w.writerow(information_dict)

def store_as_JSON(information):
	import json

	# must be done all at once due to the nature of storing
	# JSON; can't be appended the way CSVs are--if want to append,
	# must load the whole file, parse the JSON, add the information,
	# and store back again
	with open('outfile.json', 'w') as outfile:
		outfile.write(json.dumps(information))

def store_as_mongodb(information):

	# if you're using your local copy of MongoDB, make sure that
	# you start your copy ahead of time by running
	# 	...\bin\mongod.exe
	# can access the shell with ...\bin\mongo.exe

	# http://www.mongodb.org/display/DOCS/Tutorial

	# for my tutorial, I'm using a free MongoLab account

	import mongoengine

	mongoengine.connect('test_collection',
		host='mongodb://pennapps:pennapps1@ds037617-a.mongolab.com:37617/data_scraping')

	# if we're doing it locally, can just do:
	# mongoengine.connect('test_collection')


	# Store specific information
	class MyDataItem(mongoengine.Document):
		email = mongoengine.EmailField(required=True)
		first_name = mongoengine.StringField(max_length=50)
    	last_name = mongoengine.StringField(max_length=50)
    	phones = mongoengine.ListField(mongoengine.StringField(), default=[])

    item = MyDataItem(email='you@sas.upenn.edu',
    				first_name='John')

    # whoops! forgot last name
    item.last_name = 'Feinman'

    # save it!
    item.save()

    # Store any random informatoin we have coming in
    class MyUnknownDataItem(mongoengine.DynamicDocument):
    	data_id = mongoengine.StringField(primary_key=True)

    item = MyUnknownDataItem(**information) # no matter what we pass it, kwargs stores it!
    item.save()

def get_mongo_information():

	# querying: http://mongoengine-odm.readthedocs.org/en/latest/guide/querying.html

	class MyDataItem(mongoengine.Document):
		email = mongoengine.StringField(required=True)
		first_name = mongoengine.StringField(max_length=50)
    	last_name = mongoengine.StringField(max_length=50)
    	phones = mongoengine.ListField(mongoengine.StringField(), default=[])

    users = MyDataItem.objects()
    #filter on name, greater than "J" (field + '__gte')
    users = MyDataItem.objects(first_name__gte='J')
    #etc.