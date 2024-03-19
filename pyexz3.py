# Copyright: see copyright.txt

import os
import sys
import logging
import traceback
from optparse import OptionParser

from symbolic.loader import *
from symbolic.explore import ExplorationEngine

print("PyExZ3 (Python Exploration with Z3)")

sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__)))] + sys.path

usage = "usage: %prog [options] <path to a *.py file>"
parser = OptionParser(usage=usage)

parser.add_option("-l", "--log", dest="logfile", action="store", help="Save log output to a file", default="")
parser.add_option("-s", "--start", dest="entry", action="store", help="Specify entry point", default="")
parser.add_option("-g", "--graph", dest="dot_graph", action="store_true", help="Generate a DOT graph of execution tree")
parser.add_option("-m", "--max-iters", dest="max_iters", type="int", help="Run specified number of iterations", default=0)
parser.add_option("--cvc", dest="cvc", action="store_true", help="Use the CVC SMT solver instead of Z3", default=False)
parser.add_option("--z3", dest="cvc", action="store_false", help="Use the Z3 SMT solver")

(options, args) = parser.parse_args()

if not (options.logfile == ""):
	logging.basicConfig(filename=options.logfile,level=logging.DEBUG)

if len(args) == 0 or not os.path.exists(args[0]):
	parser.error("Missing app to execute")
	sys.exit(1)

solver = "cvc" if options.cvc else "z3"

filename = os.path.abspath(args[0])

explore_repeat = int(args[1]) if len(args) > 1 else 1 # add a argument to specify the times of repeat explore 
	
# Get the object describing the application
app = loaderFactory(filename,options.entry)
if app == None:
	sys.exit(1)

print ("Exploring " + app.getFile() + "." + app.getEntry())

result = None
try:
	i = 0
	input_file = open(filename+"_"+str(explore_repeat)+"_input.csv","w")

	while(i < explore_repeat):
		engine = ExplorationEngine(app.createInvocation(), solver=solver)

		generatedInputs, returnVals, path = engine.explore(options.max_iters)
		for input in generatedInputs:
			formatted_line = ', '.join([str(tuple_[1]) for tuple_ in input])
			input_file.write(formatted_line + '\n')

		i+=1

		# check the result
		result = app.executionComplete(returnVals)

	
	input_file.close()
	# output DOT graph
	if (options.dot_graph):
		file = open(filename+".dot","w")
		print(f"Path to DOT: {path.toDot()}")
		print(path.printAllPaths)
		file.write(path.toDot())
		file.write(path.printAllPaths())
		file.close()

except ImportError as e:
	# createInvocation can raise this
	logging.error(e)
	sys.exit(1)

if result == None or result == True:
	sys.exit(0)
else:
	sys.exit(1)	
