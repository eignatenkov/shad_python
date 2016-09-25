import unittest
import numpy as np
from scipy import stats

from ignatenkov import pb, pa, pd_c, pc_ab, pc

params = {
    'amin': 75,
    'amax': 90,
    'bmin': 500,
    'bmax': 510,
    'p1': 0.1,
    'p2': 0.01,
    'p3': 0.3
}


class TestPA(unittest.TestCase):
    def setUp(self):
        self.params = params

    def test_happy_pass(self):
        print pa(self.params)
        self.assertEqual(sum(pa(self.params)[1]), 1)

    def test_moments(self):
        custm = stats.rv_discrete(name='Uniform', values=pa(self.params))
        print custm.mean(), custm.var()
        self.assertEqual(custm.mean(), 82.5)
        self.assertEqual(custm.var(), 21.25)


class TestPB(unittest.TestCase):
    def setUp(self):
        self.params = params

    def test_happy_pass(self):
        print pb(self.params)
        self.assertEqual(sum(pb(self.params)[1]), 1)

    def test_moments(self):
        custm = stats.rv_discrete(name='Uniform', values=pb(self.params))
        print custm.mean(), custm.var()
        self.assertEqual(custm.mean(), 550)
        self.assertEqual(custm.var(), 850)


class TestPD_C(unittest.TestCase):
    def setUp(self):
        self.params = params

    def test_happy_pass(self):
        print pd_c(10, self.params)


class TestPC_AB(unittest.TestCase):
    def setUp(self):
        self.params = params

    def test_happy_pass(self):
        print pc_ab(80, 500, self.params)


class TestPC(unittest.TestCase):
    def setUp(self):
        self.params = params

    def test_happy_pass(self):
        print 'test pc'
        print pc(self.params)

if __name__ == '__main__':
    unittest.main()
