#testisprime.py
from prime import isPrime
import unittest
class IsPrimeTestCase(unittest.TestCase):
    def testIsPrime(self):
         self.assertEqual(isPrime(2),True,'素数判断错误')
         self.assertEqual(isPrime(7),True,'素数判断错误')
         self.assertEqual(isPrime(12),False,'12不是素数，判断错误')
         self.assertEqual(isPrime(0),False,'0不是素数，判断错误')
         self.assertEqual(isPrime(1),False,'1不是素数，判断错误')
         self.assertEqual(isPrime(-7),False,'负数不是素数')

if __name__ == '__main__':
    unittest.main()
