# ETS LOG330 TP5
# Calcul des intervalles
# Auteur :Bernard Millet milb16018406
# 27 juillet 2018
import sys
import argparse
from math import sqrt

def readArguments():

	parser = argparse.ArgumentParser(description='TP5 – Intervalles de confiance')
	parser.add_argument('--path', action="store_true", help='Le chemin de la racine vers le fichier CSV')
	parser.add_argument('--x', action="store_true", help='Le x de la valeur estime.')

	return parser.parse_args()


def validateData(data):
	try:
		data = float(data)
	except:
		raise ValueError('Erreur de donnees')


def getListOfCoupleFromFile(fileName, nbrOfLineToSkip):

	numbersList = []
	counterLine = 0
	file = open(fileName, 'r')

	while True:

		line = file.readline()
		if not line: 
			break

		if(counterLine >= nbrOfLineToSkip):
			line = line.replace("\n", "")
			line = line.replace(",", ".")
			coupleXY = line.split(';')
			validateData(coupleXY[0])
			validateData(coupleXY[1])
			numbersList.append(coupleXY)

		counterLine += 1

	file.close()

	return numbersList


def GetBaseData(coupleData):
	baseData = {
		'sum_X': 0,
		'sum_Y': 0,
		'avrg_X': 0.0,
		'avrg_Y': 0.0,
		'B0': 0.0,
		'B1': 0.0,
		'n': 0,
	}

	X = 0
	Y = 0
	sum_XmultX = 0
	sum_XmultY = 0

	for couple in coupleData:

		validateData(couple[0])
		validateData(couple[1])

		X = float(couple[0])
		Y = float(couple[1])

		sum_XmultX += X * X
		sum_XmultY += X * Y

		baseData['sum_X'] += X
		baseData['sum_Y'] += Y


	baseData['n'] = len(coupleData)
	baseData['avrg_X'] = baseData['sum_X'] / baseData['n']
	baseData['avrg_Y'] = baseData['sum_Y'] / baseData['n']

	baseData['B1'] = (sum_XmultY - baseData['n'] * baseData['avrg_X'] * baseData['avrg_Y']) / \
      (sum_XmultX - baseData['n'] * baseData['avrg_X'] * baseData['avrg_X'])

	baseData['B0'] =  baseData['avrg_Y'] - baseData['B1'] *  baseData['avrg_X']

	return baseData


def calculateEquartType(coupleData,B0,B1):

	variance = 0.0
	equartType = 0.0
	B1multX = 0.0
	W = 0.0
	sqr_W = 0.0
	sum__sqr_W = 0.0
	variance = 0.0
	X = 0
	Y = 0
	n = 0

	for couple in coupleData:

		validateData(couple[0])
		validateData(couple[1])

		X = float(couple[0])
		Y = float(couple[1])

		B1multX = B1 * X
		W = Y - B0 - B1multX
		sqr_W = W * W
		sum__sqr_W += sqr_W
		n += 1

	variance = (1 / (n-1)) * sum__sqr_W
	equartType = sqrt(variance)

	return equartType


def calculateInterval(desiredX, coupleData, equartType, B0, B1, avrg_X):

	validateData(equartType)
	validateData(B0)
	validateData(B1)
	validateData(avrg_X)

	intervals = {'70':0.0, '90':0.0}

	tTable70 = [1.963, 1.386, 1.250, 1.190, 1.156, 1.134, 1.119, 1.108, 1.100, 1.093, 1.088, 1.083, 1.079, 1.076]
	tTable90 = [6.314, 2.920, 2.353, 2.132, 2.015, 1.943, 1.895, 1.860, 1.833, 1.812, 1.796, 1.782, 1.771, 1.761]
	X = 0
	Y = 0
	V = 0
	sqr_V = 0.0
	sum__sqr_V = 0.0
	racine = 0.0
	n = len(coupleData)
	dl = n-2
	estimatedY = desiredX * B1 + B0

	for couple in coupleData:

		validateData(couple[0])
		validateData(couple[1])

		X = float(couple[0])
		Y = float(couple[1])
		V = X - avrg_X
		sqr_V = V * V
		sum__sqr_V += sqr_V


	racine = sqrt(1 + (1/n) + ((desiredX - avrg_X) * (desiredX - avrg_X) / sum__sqr_V))
	intervals['70'] = tTable70[ dl -1] * equartType  * racine
	intervals['90'] = tTable90[ dl -1] * equartType  * racine

	return intervals


def main():

	csvPathName = 'data/tp5data.csv'
	nbrOfLineToSkipInCsv = 1
	desiredX = 1119

	args = readArguments();
	argsX = args.x
	argsPath = args.path

	if(argsX):
		desiredX = argsX
		validateData(desiredX)

	if(argsPath):
		csvPathName = argsPath


	desiredX = float(desiredX)

	listOfcouple = getListOfCoupleFromFile(csvPathName, nbrOfLineToSkipInCsv)
	baseData = GetBaseData(listOfcouple)
	equartType = calculateEquartType(listOfcouple, baseData['B0'],baseData['B1'])
	intervals = calculateInterval(desiredX, listOfcouple, equartType, baseData['B0'], baseData['B1'], baseData['avrg_X'])
	
	estimatedY = desiredX * baseData['B1'] + baseData['B0']
	print()
	print('Pour un X de {}'.format(desiredX))
	print('interval 90% = {}'.format(intervals['90']))
	print('interval 70% = {}'.format(intervals['70']))
	print('L\'intervalle Y a 90 est de {} a {}'.format(estimatedY - intervals['90'], estimatedY + intervals['90']))
	print('L\'intervalle Y a 70 est de {} a {}'.format(estimatedY - intervals['70'], estimatedY + intervals['70']))
	print('_______________________________________________________')


if __name__ == '__main__':
	main()