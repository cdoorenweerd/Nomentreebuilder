#!/usr/bin/python

# Import the csv and ETE tree module
import csv
from ete2 import Tree

# Ask for input file [work in progress]
# ifile = raw_input("Enter filename: ")


# Define function to read a column and return list of unique values
def colreader(n):
	# Define input file and reader
	ifile = open('/Users/cdoorenweerd/Desktop/systematictree/Final_dataset_CD1.csv','rU')
	reader = csv.reader(ifile)
	# create empty lists and starting point
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
	ifile.close()

# Create an empty tree to populate
t = Tree()
taxonmap = {}
	
# Create tree backbone based on the first column
backbone, parentmap = colreader(0)
# print backbone
for taxon in backbone:
	# create map with taxa and function to add children
	taxonmap.update({taxon:t.add_child(name=(taxon))})

# print t

# Determine number of columns in the csv file based on the first row
with open('/Users/cdoorenweerd/Desktop/systematictree/Final_dataset_CD1.csv','rU') as f:
    reader = csv.reader(f, delimiter=',', skipinitialspace=True)
    first_row = next(reader)
    numcols = len(first_row)

# Add children for levels 1-numcols
for level in range (1, numcols):
	purgedtaxonlist, parentmap = colreader(level)	
	for taxon in purgedtaxonlist:
		parentname = parentmap[taxon]
		parent = taxonmap[parentname]
		taxonmap.update({taxon:parent.add_child(name=(taxon))})

print t.get_ascii(show_internal=True)


# Output tree files
# write tree into a newick file with internal node values
t.write(format=1, outfile="/Users/cdoorenweerd/Desktop/systematictree/final_tree_internalnodes2.nwk")
# and one without internal node values
t.write(format=0, outfile="/Users/cdoorenweerd/Desktop/systematictree/final_tree2.nwk")
