#!/usr/bin/python

# Import the csv and ETE tree module
import csv
from ete2 import Tree


# Define function to read a column and return list of unique values
def colreader(n):
	# Define input file and reader
	ifile = open('/Users/cdoorenweerd/Desktop/systematictree/Final_dataset_CD1.csv','rU')
	reader = csv.reader(ifile)# create empty lists and starting point
	taxonlist = []
	purgedtaxonlist = []
	parentmap = {}
	rownum = 0
	# start reading the values from the column
    	for row in reader:
        	# add value of column n to a list
        	taxonlist.append(row[n])
        	# there are no parents for the first column, so don't try to find them
        	if n == 0:
        		rownum += 1
        	else:
        		# create a parent dictionary with child(key):parent(value)
        		parentmap.update({row[n]:row[n-1]})
        		rownum += 1
	# show resulting list
	# /print taxonlist
	# show resulting parentmap
	# /print taxonmap
	# get unique taxonvalues only by converting to a set
	taxonset = set(taxonlist)
	# /print taxonset
	# convert back to a list to make it usable further on
	purgedtaxonlist = list(taxonset)
	# /print purgedtaxonlist	 
	# return purgedtaxonlist for use outside function 
	return purgedtaxonlist, parentmap

# Create an empty tree to populate
t = Tree()
taxonmap = {}
	
# Create tree backbone
backbone, parentmap = colreader(0)
# print backbone
for taxon in backbone:
	# create map with taxa and function to add children
	taxonmap.update({taxon:t.add_child(name=(taxon))})

# print t


# Add children for level 1
purgedtaxonlist, parentmap = colreader(1)	
for taxon in purgedtaxonlist:
	parentname = parentmap[taxon]
	parent = taxonmap[parentname]
	taxonmap.update({taxon:parent.add_child(name=(taxon))})

# print t.get_ascii(show_internal=True)


# Add children for level 2
purgedtaxonlist, parentmap = colreader(2)	
for taxon in purgedtaxonlist:
	parentname = parentmap[taxon]
	parent = taxonmap[parentname]
	taxonmap.update({taxon:parent.add_child(name=(taxon))})

# print t.get_ascii(show_internal=True)


# Add children for level 3
purgedtaxonlist, parentmap = colreader(3)	
for taxon in purgedtaxonlist:
	parentname = parentmap[taxon]
	parent = taxonmap[parentname]
	taxonmap.update({taxon:parent.add_child(name=(taxon))})

# print t.get_ascii(show_internal=True)

# Add children for level 4
purgedtaxonlist, parentmap = colreader(4)	
for taxon in purgedtaxonlist:
	parentname = parentmap[taxon]
	parent = taxonmap[parentname]
	taxonmap.update({taxon:parent.add_child(name=(taxon))})

print t.get_ascii(show_internal=True)

# Add children for level 5
# purgedtaxonlist, parentmap = colreader(5)	
# for taxon in purgedtaxonlist:
#	parentname = parentmap[taxon]
#	parent = taxonmap[parentname]
#	taxonmap.update({taxon:parent.add_child(name=(taxon))})
#
# print t.get_ascii(show_internal=True)



# Output tree files
# write tree into a newick file with internal node values
t.write(format=1, outfile="/Users/cdoorenweerd/Desktop/systematictree/final_tree_internalnodes.nwk")
# and one without internal node values
t.write(format=0, outfile="/Users/cdoorenweerd/Desktop/systematictree/final_tree.nwk")
