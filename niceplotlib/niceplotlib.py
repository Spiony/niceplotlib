# Matplotlib as plot library
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
# Scanning system files
import os
# json for style description
import json
# Add path



# Set default data format and use LaTeX
def init():
	mpl.use('pdf')
	mpl.rcParams["text.latex.preamble"].append(r'\usepackage{nicefrac}')

	# Preload default style dict (intended for usage in already finished plot
	# scripts)
	loadStyleDict()

	return 0


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
   main()
