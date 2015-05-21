#!/usr/bin/python

# Import the csv and ETE tree module
import csv
from ete2 import Tree


# Determines number of columns in the csv file based on the first row (header)
def countranks(systematicmatrix):
    with open(systematicmatrix, 'rU') as matrix:
        reader = csv.reader(matrix, delimiter = ',')
        first_row = next(reader)
        numcols = len(first_row)
    return numcols

# Creates a list of taxa per column (= rank) with unique values only and no empty values
def rankvalues(colnumber, systematicmatrix):
    taxonlistperrank = []
    with open(systematicmatrix, 'rU') as matrix:
        reader = csv.reader(matrix)
        next(reader, None) # skip headers
        for row in reader:
            taxonlistperrank.append(row[colnumber])
            cleantaxonlistperrank = filter(None, taxonlistperrank)
    uniquecleantaxonset = set(cleantaxonlistperrank)
    uniquecleantaxonlist = list(uniquecleantaxonset)
    return uniquecleantaxonlist

# Creates a parentmap [FIX THIS TO HANDLE GAPS]
def parentmapmaker(colnumber, systematicmatrix):
    parentmap = {}
    with open(systematicmatrix, 'rU') as matrix:
        reader = csv.reader(matrix)
        for row in reader:
            parentmap.update({row[colnumber]:row[colnumber-1]})
    return parentmap

# Creates a map of branch lengths from parent
# def rankposition(systematicmatrix):
# iets met, if prev pos in list is None, add 1 to branch length to parent, else, continue

# RUN

systematicmatrix = '20150328_macrofaunalijst_tree_lines.csv'

# Create an empty tree to populate and define taxonmap
t = Tree()
taxonmap = {}

# Create tree backbone based on the first column
backbone = rankvalues(0, systematicmatrix)
for taxon in backbone:
    taxonmap.update({taxon:t.add_child(name=(taxon))})

# Add children for levels 1-numcols
numcols = countranks(systematicmatrix)
for rank in range (1, numcols):
    taxonlist = rankvalues(rank, systematicmatrix)
    parentmap = parentmapmaker(rank, systematicmatrix)
    for taxon in taxonlist:
        parentname = parentmap[taxon]
        parent = taxonmap[parentname]
        taxonmap.update({taxon:parent.add_child(name=(taxon))})

print t.get_ascii(show_internal = True)

# write tree into a newick file with internal node values
t.write(format=1, outfile = 'final_tree_internalnodes2.nwk')
# and one without internal node values
t.write(format=0, outfile = 'final_tree2.nwk')