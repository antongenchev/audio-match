import unittest
from src.hashing import generate_hashes

class TestHashing(unittest.TestCase):

    def test_generate_hashes(self):
        peaks = [(0,34), (55,10), (100,500), (100,600)]
        result = generate_hashes(peaks)
        expected_result = [('5afd40cbfba9dd237d1c4187c960b313116b0abc', 0),
                           ('9babb08f1a8d2431407adf182beb650cc14a0f5e', 0),
                           ('af0c49f456b4d2d50dab3c54a6fb48441d7f3d68', 0),
                           ('3f25c720f131169aaea7f8acbbf733178366f495', 55),
                           ('03c20cb84a4aef2383ae97df8cbcf5db8eea69a6', 55),
                           ('fa165ba6086eadedd5e422cddd54ed7ee3c99375', 100)]
        self.assertEqual(result, expected_result)