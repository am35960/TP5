import unittest
import test.test_intervalles as test_intervalles

suite1 = unittest.TestLoader().loadTestsFromModule(test_intervalles)

unittest.TextTestRunner(verbosity=2).run(suite1)