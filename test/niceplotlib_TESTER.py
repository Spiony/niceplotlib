import niceplotlib as nipl
import numpy as np
print('# --------------------------------------------------------------------------- #')
print('#                               NICEPLOTLIT TEST                              #')
print('# --------------------------------------------------------------------------- #\n\n')

# Debugging function
def printStructure(n, data):
	noCount = n
	strSpace = '   '
	strFmt = (n-1) * strSpace + ' * {}'

	if isinstance(data[0], str):
		print(strFmt.format(1))
	elif isinstance(data[0], float):
		print(strFmt.format(1))
	elif isinstance(data[0], int):
		print(strFmt.format(1))
	else:
		for cont in data:
			if type(cont).__name__ == 'list':
				print(strFmt.format(len(cont)))
				printStructure(noCount + 1, cont)
			else:
				dataShape = cont.shape
				print(strFmt.format(dataShape))
				printStructure(noCount + 1, cont)


print('# -------------------------- TEST readCSV Function  ------------------------- #\n')

plotDATA = nipl.readCSV('simpleDataSet.csv', headerLength = 1)
print('\nLength of plotDATA: {}\n', len(plotDATA))
for part in plotDATA:
	print('   {}'.format(part))
	
print('# ---------------------------------------------------------------------------- #\n\n')
	
	
print('# ------------------------- TEST readAllCSV Function  ------------------------ #\n')

plotDATA = nipl.readAllCSV(headerLength = 1)
print('\nLength of plotDATA: {}\n'.format(len(plotDATA)))
for part in plotDATA:
	print('   {}'.format(part))

print('# ---------------------------------------------------------------------------- #\n\n')
		

print('#------------------ TEST readAllCSV Function in other folder  ---------------- #\n')
	
print('TEST readAllCSV Function in other folder')
	
plotDATA = nipl.readAllCSV(dir = 'stack\\', headerLength = 1, csvDelimiter = '\t', legendRegex = r'sim_c([0-9]*)')

print('\nLength of plotDATA: {}\n'.format(len(plotDATA)))

print('\nLegend of plotDATA: {}\n'.format(plotDATA[2]))
print('\nHeaders of plotDATA: {}\n'.format(plotDATA[3]))
print('Data Structure\n')
printStructure(1, plotDATA)
print('\n')

for part in plotDATA:
	print('   {}'.format(part))
	
	
print('# ---------------------------------------------------------------------------- #\n\n')


print('# ------------------------- TEST import JSON Style --------------------------- #\n')
	
styleDict = nipl.loadStyleDict()
nipl.reportStyle(styleDict)
	
print('# ---------------------------------------------------------------------------- #\n\n')


print('# ---------------------------- TEST Plot Functions ----------------------------- #\n')
	
# Single to Single
plotDATA = nipl.readSingleCSV('simpleDataSet.csv', headerLength = 1)
outputName = 'single2single'
fig = nipl.createMultiLinesPlot(outputName, plotDATA[0], plotDATA[1], xlab = 'time / s', ylab = 'distance / m', title = 'niceplotlib', labels = [plotDATA[3]], axisFlag = [plotDATA[-1]])
fig = nipl.stylizePlot(fig)
nipl.savePlot(fig, outputName, outputDatatypes = ['pdf', 'png'])

# Single to Multiple


# Multiple to Single
plotDATA = nipl.readAllCSV(dir = 'stack\\', headerLength = 1, csvDelimiter = '\t', legendRegex = r'sim_c([0-9]*)')
outputName = 'multiple2single'
fig1 = nipl.createMultiLinesPlot(outputName, plotDATA[0], plotDATA[1], xlab = '', ylab = '', title = '', labels = plotDATA[3], axisFlag = plotDATA[-1])
fig1 = nipl.stylizePlot(fig1)
nipl.savePlot(fig1, outputName, outputDatatypes = ['pdf', 'png'])


# Multiple to Multiple
plotDATA = nipl.readAllCSV(dir = 'stack\\', headerLength = 1, csvDelimiter = '\t', legendRegex = r'sim_c([0-9]*)')
outputNamePre = 'multiple2multiple'
#for part in plotDATA:
	#print('   {}'.format(part))
# combine legend regex data with header data 
for i in range(len(plotDATA[0])):	
	outputName = outputNamePre + str(i)
	fig1 = nipl.createMultiLinesPlot(outputName, [plotDATA[0][i]], [plotDATA[1][i]], xlab = '', ylab = '', title = '', labels = [plotDATA[3][i]], axisFlag = plotDATA[-1])
	fig1 = nipl.stylizePlot(fig1)
	nipl.savePlot(fig1, outputName, outputDatatypes = ['png'])


print('# ---------------------------------------------------------------------------- #\n\n')

# make a test with adding something fancy to the figure