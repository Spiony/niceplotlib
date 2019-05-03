'''
This library offers a set of functions to create nice looking plots

The matplotlib library is used for plot functions. The functions of the library
take care of data import and export. Some plot functions are generalized to
ease the creation of plots. 


'''


# Read CSV Files
import csv
# Numerical calculations
import numpy as np
# Matplotlib as plot library
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
# Scanning system files
import os
# Analyse file names
import re
# json for style description
import json

# Add path
import sys


###############################################################################
# Input Functions
###############################################################################

# Set default data format and use LaTeX

def init():
	mpl.use('pdf')
	mpl.rcParams["text.latex.preamble"].append(r'\usepackage{nicefrac}')

	# Preload default style dict (intended for usage in already finished plot
	# scripts)
	loadStyleDict()

	return 0


###############################################################################
# Input Functions
###############################################################################

def getFilepaths(dir = '.', dataType = 'csv'):
	return [f for f in os.listdir(dir) if (os.path.isfile(os.path.join(dir, f)) and f.endswith(dataType))]


def readSingleCSV(filepath, csvDelimiter = ',', headerLength = 0, hasCommonAxis = 1, legendRegex = r''):

	legendStr = []
	header = []
	
	[xVec, yVecStack, headerData, legendStr, axisFlag] = readCSV(filepath, csvDelimiter, headerLength, hasCommonAxis, legendRegex)

	out = [[xVec], [yVecStack]]
	out.append(legendStr)
	out.append(headerData)
	out.append(axisFlag)

	return out


def readCSV(filepath, csvDelimiter = ',', headerLength = 0, hasCommonAxis = 1, legendRegex = r''):
	print(' * reading file {}'.format(filepath))
	xStack = []
	yStack = []
	headerData = []
	legendStr = ''
	
	if not legendRegex  == r'':
		legendStr = list(re.findall(legendRegex, filepath, flags=0)[0])
	
	if headerLength:
		headerData = np.genfromtxt(filepath, delimiter = csvDelimiter, dtype=str)[:headerLength][0]

	csvData = np.genfromtxt(filepath, delimiter = csvDelimiter)[headerLength:]
	csvData = csvData.transpose()

	yVecStack = []
	if hasCommonAxis:
		xVec = np.array(csvData[0])
	
		for row in csvData[1:]:
			yVecStack.append(row.transpose())
	else:
		xVec = range(csvData[0])
	
		for row in csvData:
			yVecStack.append(row.transpose())		

	xStack.append(xVec)
	yStack.append(yVecStack)
	
	return [xVec, yVecStack, headerData, legendStr, hasCommonAxis]


def readAllCSV(dir = os.getcwd(), csvDelimiter = ',', headerLength = 0, hasCommonAxis = 1, legendRegex = r''):
	print('\nRead Data in {} ... '.format(dir))

	csvFilePaths = getFilepaths(dir)
	xStack = []
	yStack = []
	headerStack = []
	legendStack = []
	axisFlagStack = []
	for file in csvFilePaths:
		[xVec, yVecStack, headerData, legendStr, axisFlag] = readCSV(os.path.join(dir, file), csvDelimiter, headerLength, hasCommonAxis, legendRegex)

		xStack.append(xVec)
		yStack.append(yVecStack)
		headerStack.append(headerData)
		legendStack.append(legendStr)
		axisFlagStack.append(axisFlag)
		
	out = [xStack, yStack]
	
#	if not legendRegex  == r'':
	out.append(legendStack)
		
#	if headerLength:
	out.append(headerStack)
	out.append(axisFlagStack)

	print('Done!')	
	return out


###############################################################################
# Style Functions
###############################################################################

def loadStyleDict(filepath = os.path.dirname(__file__) + '\style.json'):
	jsonFile = open(filepath)
	jsonContent = jsonFile.read()
	
	styleDict = json.loads(jsonContent)
	styleKeys = styleDict.keys()
	
	if 'scale' not in styleKeys:
		# small, medium, big, large
		scaleDict = {0: 0.475, 1: 0.6, 2: 0.8, 3: 1.0}
		styleDict['scale'] = scaleDict[styleDict['scaleId']]
	
	if 'ratio' not in styleKeys:
		# equal, 4:3, GOLDEN, WIDE
		ratioDict = {0: 1.0, 1: 1.3333333333, 2:  1.6180339887, 3: 1.7777777777}
		styleDict['ratio'] = ratioDict[styleDict['ratioId']]
		
	styleDict['width'] = styleDict['maxTextwidth'] * styleDict['scale']
	styleDict['height'] = styleDict['width'] / styleDict['ratio']	
		
	# Search for mplrc file
	# Current State: always search in module folder
	styleDict['mplRC'] = os.path.join(os.path.dirname(__file__), styleDict['mplRC']) 

	plt.style.use(styleDict['mplRC'])

	return styleDict


def reportStyle(styleDict):
	styleKeys = styleDict.keys()
	
	for key in styleKeys:
		print('  {}: {}'.format(key, styleDict[key]))
	print('\n')
	return 0


def stylizePlot(fig, styleDict = loadStyleDict()):
	fig.set_size_inches(styleDict['width'], styleDict['height'])	
	fig.subplots_adjust(left= styleDict['figBorder'][0], bottom = styleDict['figBorder'][1], right = styleDict['figBorder'][2], top = styleDict['figBorder'][3])
	return fig


###############################################################################
# Plot Wrapper Functions
###############################################################################


# Split this function into plotting and style part
def createMultiLinesPlot(outputName, xStack, yStack, xlab = '', ylab = '', xlim = [], ylim = [], title = '', fileIds = [],varIdsIn = [], labels = [], fig = [], axisFlag = [0], styleDict = loadStyleDict()):
	print('Create Plot {} ... '.format(outputName), end='')
	
	if not fig:
		fig = plt.figure()
		ax = fig.add_subplot(111)

	lineStyleStack = styleDict['lineStyles']
	noLineStyles = len(lineStyleStack)

	if len(labels) > 0:
		styleDict['visible'] = 1
		styleDict['labels'] = labels

	fileIds = range(len(xStack))
		
	for i, fileId in enumerate(fileIds):
		if len(varIdsIn) < 1:
			varIds = range(len(yStack[i]))
		else:
			varIds = varIdsIn
		for j, varid in enumerate(varIds):
			if styleDict['legVisible']:
				plt.plot(xStack[fileId], yStack[fileId][varid], lineStyleStack[j % noLineStyles], label = styleDict['labels'][fileId][axisFlag[fileId] + varid])
			else:
				plt.plot(xStack[fileId], yStack[fileId][varid], lineStyleStack[j % noLineStyles])

	
	if len(title) > 0:
		ax.set_title(title)
	
	if len(xlab) > 0:
		ax.set_xlabel(xlab)
	
	if len(ylab) > 0:
		ax.set_ylabel(ylab)
	
	if len(xlim) > 0:
	  ax.set_xlim(xlim)
	
	if len(ylim) > 0:
	  ax.set_ylim(ylim)
	
	if styleDict['legVisible']:
		handles, labels = ax.get_legend_handles_labels()
		
		if not styleDict['legExport']:
			legend = ax.legend(handles, labels, ncol = styleDict['legNcol'])
			legend.get_frame().set_linewidth(styleDict['legLinewidth'])
		else:
			figlegend = plt.figure()
			legend = figlegend.legend(handles, labels, ncol = styleDict['legNcol'], loc = 'center')
			legend.get_frame().set_linewidth(styleDict['legLinewidth'])
			legendName = outputName + '_legend.pdf'
			exportLegend(legend, legendName)
	
	print('Done!\n')
	return fig

	
###############################################################################
# Export Functions
###############################################################################

def savePlot(fig, outputFilename, outputDatatypes = ['pdf']):
	
	print('Creating Files... ')
		
	for i in range(len(outputDatatypes)):
	  print(' - save figure {} no. {} ... '.format(outputFilename, i), end='')
	  fig.savefig(''.join([outputFilename, '.', outputDatatypes[i]]))
	  print('Done!')
	print('Done!')
	
	return 0


def exportLegend(legend, outputFilename, outputDatatypes, noEntries, ncols):
	print('Export legend... ', end='')
	nrows = int(noEntries/ncols) + noEntries % ncols
	fontSize = plt.rcParams['font.size']
	
	# Determine size of legend figure
	# Divide by 72 because fontSize is saved in "point" format (1 pt = 1/72 inch)
	height = (nrows + (legend.labelspacing + legend.handleheight) * (nrows-1) + 2 * legend.borderpad) * fontSize / 72
	width = (ncols + (legend.columnspacing + legend.handlelength + legend.handletextpad + 2 * legend.borderpad) * ncols) * fontSize / 72
	
	fig  = legend.figure
	fig.canvas.draw()
	fig.set_size_inches(width, height)
	savePlots(fig, outputFilename, outputDatatypes)
    
	return 0


# stuff to run always here such as class/def
def main():
    pass


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()