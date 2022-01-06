# Filename: AponteKenneth_016_p3.py

### ADD YOUR NAME, STUDENT ID AND SECTION NUMBER BELOW ###
# NAME: Kenneth R. Aponte Mendez
# STUDENT ID: 802 19 9075
# SECTION: 016

"""Parse the contents of an HTML file and output the internal resources used.

We are looking for tags of interest: a, script, link, img, audio, video, and form.
Within each tag of interest we're looking for a particular attribute of
interest (href for a & link, src for script & img, action for form).
Each tag of interest is to be represented by a dictionary, where the attribute names
will be the dictionary keys and the attribute values will be the dictionary values.
A list is created for each type of tag, storing all of the internal
resources referenced by tags of that type.
Finally, the results are stored in an output file.

Input:  The file index.html will be used as an input file
Output: The results will be stored in a file named index_resources.txt
"""

# CONSTANTS

INPUTFILE = 'index2.html'
OUTPUTFILE = 'index_resources.txt'
# We'll use a dictionary where the keys are the tags of interest and the values
# are the corresponding attributes of interest.  That way we can process the HTML
# file using this dictionary without having to look for specific tags or attributes.
DICTOFINTEREST = {'a':'href','link':'href','form':'action',
                  'img':'src','script':'src','audio':'src','video':'src'}


def load_data():
	"""Returns the contents of the input file as a list of lines, or None if an error occurs."""
	try:
		fh = open(INPUTFILE)
	except:
		linesInFile = None
	else: # Only gets executed if no exception was raised
		linesInFile = fh.readlines()
		fh.close()
	return linesInFile


def get_tag_of_interest(line):
	"""Return a tag of interest if one is found in the line, or None otherwise.

	Parameters:
		line - A single line of text from the HTML file being processed.
	Returns:
		A string with the (opening) tag of interest, if one is found, or None otherwise.
	"""
	# The tags of interest are the keys to the dictionary DICTOFINTEREST.
	for tagName in DICTOFINTEREST:
		# Note that, for a tag to have a resource, it must have a space after the tag name
		openingTag = '<' + tagName + ' '
		if openingTag in line: # Found it!
			posTagBegin = line.find(openingTag)
			# Make sure we don't just find any '>', but the next one after the start of the tag.
			posTagEnd = line.find('>', posTagBegin)
			return line[posTagBegin:posTagEnd + 1]
	# If we're still in the function, then we didn't find any tags of interest.
	return None


def get_attr_of_interest(tag):
	"""Return value of attribute of interest if one is in the tag, or None otherwise.

	Parameters:
		tag - A tag (as a dict) within which we'll look for the attribute of interest.
		      Attribute names are the dict keys and attribute values are the dict values.
		      The tag name can be found as the value of the 'tagName' key.
	Returns:
		A string representing the value of the attribute of interest for the tag received,
		or None if either the attribute is absent or if the resource is external.
	"""
	tagName = tag['tagName']
	tagNamesValue = DICTOFINTEREST[tagName]#the value that should be looked for in that specific tagName
	attribute = tag.get(tagNamesValue,0)#if attribute of interest is not found then attribute = 0...

	if attribute == 0:#if it had no attr of int
		return None

	if not attribute.startswith('http'):#if it does not start with http or https(not local)
		return attribute


def write_results(dictOfResources):
	"""Write all of the resources to an output file.

	Parameters:
		dictOfResources - Dictionary of resources to be saved in the output file.
		                  The keys are the tags of interest and each value is a
		                  list of all of the resouces for that type of tag.
	"""
	fh = open(OUTPUTFILE, 'w')#only openned once(before the loop starts)
	for tagName, list in sorted(dictOfResources.items()): #keys and values in the dict
		if len(list) != 0:#if the list is not empty, AKA the file had tags of interest from that specific tagName
			fh.write(tagName + '\n')
			for attribute in list:#takes ever item(attribute) in the list and writes it
				fh.write('\t' + attribute + '\n')#\t is used in order to give some indentation
	fh.close()#only closed once the loop is done


def tag_as_dict(openingTag):
	"""Convert an opening HTML tag into a dictionary.

	The attribute names will be the keys of the dictionary and the attribute values
	will be the values of those keys.  In the case of boolean attributes (the ones
	that don't have a value assigned to them), the value will be set to True.
	The dictionary will also have the special key 'tagName' to store the tag name
	(e.g. img, audio).
	NOTE: We assume attribute values DO NOT have spaces, and that the only spaces
	in the tag are to separate attributes.

	Parameters:
		openingTag - The opening HTML tag to be converted into a dictionary.
	Returns:
		A dictionary representation of the tag, as detailed above.
	"""
	dict = {}
	list = openingTag.split(' ')
	for item in list: #looping through every item in the list...
		if item.startswith('<'): #filtering the attribute(finding the tagName)
			tagName = item[1:]
			dict['tagName'] = tagName
			continue #if the item was the tag name it will re loop with the other item in the list

		if '=' not in item:#then the item is a boolean attribute
			boolean_attribute = item[:-1] #this is done to remove the > from the end of the item
			dict[boolean_attribute] = True
			continue

		quotepos1 = item.find('=') + 1
		quote_type = item[quotepos1]#can be ' or "(though we could assume it was only ")
		quotepos2 = item.find(quote_type, quotepos1 + 1)
		#now that we have all the positions and the type of quote we can find the attribute(and the attribute name)
		attribute = item[quotepos1 + 1:quotepos2]
		attribute_name = item[:quotepos1 - 1]
		#now it adds the attribute and its name to the dictionary
		dict[attribute_name] = attribute
	return dict


def main():
	lstOfLines = load_data()
	if lstOfLines is None:
		print('ERROR: Could not open {}!'.format(INPUTFILE))
		exit()

	# The following dictionary will store all of the tags with resources, using the
	# tag name as the keys and a list of tags as the value.
	resourcesDict = dict()
	#the following are the lists
	alist = []
	imglist = []
	linklist = []
	formlist = []
	scriptlist= []
	audiolist= []
	videolist= []

	for line in lstOfLines:
		tag = get_tag_of_interest(line)
		if tag is not None:
			tag = tag_as_dict(tag)
			attrVal = get_attr_of_interest(tag)
			if attrVal is not None:
				#appending every value on to the actual list
				tagName = tag['tagName']#The tag name for the current tag
				if tagName == 'a':
					alist.append(attrVal)
				elif tagName == 'link':
					linklist.append(attrVal)
				elif tagName == 'img':
					imglist.append(attrVal)
				elif tagName == 'script':
					scriptlist.append(attrVal)
				elif tagName == 'form':
					formlist.append(attrVal)
				elif tagName == 'audio':
					audiolist.append(attrVal)
				elif tagName == 'video':
					videolist.append(attrVal)

	#lists for every single tag of interest
	resourcesDict['a'] = alist
	resourcesDict['link'] = linklist
	resourcesDict['img'] = imglist
	resourcesDict['script'] = scriptlist
	resourcesDict['form'] = formlist
	resourcesDict['audio'] = audiolist
	resourcesDict['video'] = videolist

	#calls write results, well, to "write the results" in an output folder
	write_results(resourcesDict)

# This line makes python start the program from the main function
# unless our code is being imported
if __name__ == '__main__':
	main()

#WHOOPS, looks like you've reached the end of my code :(
