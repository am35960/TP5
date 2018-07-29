# ETS LOG330 TP5
# Unit test pour intervalles de confiance
# Auteur :Bernard Millet milb16018406
# 29 juillet 2018

import unittest
import sys
import api.TP5 as TP5


class TestRegression(unittest.TestCase):

	def setUp(self):
		self.maxNumber = 9223372036854775807 # 2^63 - 1
		self.minNumber = -9223372036854775808 # 2^63 * -1


	def test_intervalles_invalidValue(self):
		with self.assertRaises(ValueError):
			desiredX = 1119
			listOfcouple = [['String!',2],[2.2,4.4],[3.3,2.2]]#STRING PLUTOT QUE REEL
			baseData = TP5.GetBaseData(listOfcouple)
			equartType = TP5.calculateEquartType(listOfcouple, baseData['B0'],baseData['B1'])
			intervals = TP5.calculateInterval(desiredX, listOfcouple, equartType, baseData['B0'], baseData['B1'], baseData['avrg_X'])


	def test_intervalles_lowerBound(self):
		desiredX = 1119
		listOfcouple = [[self.minNumber,2],[2.2,4.4],[3.3,2.2]]
		baseData = TP5.GetBaseData(listOfcouple)
		equartType = TP5.calculateEquartType(listOfcouple, baseData['B0'],baseData['B1'])
		intervals = TP5.calculateInterval(desiredX, listOfcouple, equartType, baseData['B0'], baseData['B1'], baseData['avrg_X'])
		self.assertTrue(intervals['70']> self.minNumber and intervals['70'] < self.maxNumber)


	def test_intervalles_higherBound(self):
		desiredX = 1119
		listOfcouple = [[self.maxNumber,2],[2.2,4.4],[3.3,2.2]]
		baseData = TP5.GetBaseData(listOfcouple)
		equartType = TP5.calculateEquartType(listOfcouple, baseData['B0'],baseData['B1'])
		intervals = TP5.calculateInterval(desiredX, listOfcouple, equartType, baseData['B0'], baseData['B1'], baseData['avrg_X'])
		self.assertTrue(intervals['70']> self.minNumber and intervals['70'] < self.maxNumber)