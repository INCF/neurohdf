import os.path as op
from neurohdf.parser.obo import *

# data files are copied from http://obofoundry.org/

spatialdict = parse( open(op.join( 'data', 'spatial.obo')), keyid = 'name' )
print spatialdict

measureunit = parse( open(op.join( 'data', 'unit.obo')), keyid = 'name' )
print measureunit