!/usr/bin/python
#
# Import the csv and ETE tree module
import csv
from ete2 import Tree


# Ask for input file [work in progress, will use argparser]
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
        # there are no parents for the first column, so don't try
        # to find them
        if n == 0:
            rownum += 1
        else:
            # create a parent dictionary with
            # child(key):parent(value)
            parentmap.update({row[n]:row[n-1]})
            rownum += 1
    # get unique taxonvalues only by converting to a set
    taxonset = set(taxonlist)
    # convert back to a list to make it usable further on
    purgedtaxonlist = list(taxonset)
    # close the input file and return purgedtaxonlist and parent
    # dictionary for use outside function
    return purgedtaxonlist, parentmap
    ifile.close()

# Define function to select nodes with a given number of leaves, size
def search_by_size(node, size):
    matches = []
    for n in node.traverse("preorder"):
        if len(n) == size: matches.append(n)
    # return the matches
    return matches


# Create an empty tree to populate
t = Tree()
taxonmap = {}

# Count number of columns in the csv file based on the first row
with open('/Users/cdoorenweerd/Desktop/systematictree/Benthos_datasetred.csv','rU') as f:
    reader = csv.reader(f, delimiter=',',skipinitialspace=True)
    first_row = next(reader)
    numcols = len(first_row)

# Create tree backbone based on the first column
backbone, parentmap = colreader(0)
for taxon in backbone:
    # create map with taxa and function to add children
    taxonmap.update({taxon:t.add_child(name=(taxon))})

backbonetext = "Added %s nodes to tree backbone"
print(backbonetext % len(taxonmap))

# Add children for each additional column
for level in range (1, numcols):
    purgedtaxonlist, parentmap = colreader(level)
    for taxon in purgedtaxonlist:
        parentname = parentmap[taxon]
        parent = taxonmap[parentname]
        taxonmap.update({taxon:parent.add_child(name=(taxon))})
    print("Added %s nodes for level %s" % (len(taxonmap), level))
    # Search whole tree created up to this point for unifurcations
    # and remove them, comment this section out if you wish to include
    # unifurcations
    matches = search_by_size(t, size=1)
    # exclude terminal branches from the list
    for terminal in t.get_leaves():
        matches.remove(terminal)
    # remove unifurcations
    for unifurcation in matches:
        unifurcation.delete()
    print("Removed %s unifurcations" % (len(matches)))

# Verbosity with final tree statistics
descendants = len(t.get_descendants())
internalnodes = descendants - len(t)
print("Final tree contains %s leaves and %s internal nodes" % (len(t), internalnodes))
# Show final tree with internal nodes
print(t.get_ascii(show_internal=True))

# Write tree into a newick file with internal node values
t.write(format=1, outfile="/Users/cdoorenweerd/Desktop/systematictree/final_tree_internalnodes4.nwk")
# and one without internal node values
t.write(format=0, outfile="/Users/cdoorenweerd/Desktop/systematictree/final_tree4.nwk")