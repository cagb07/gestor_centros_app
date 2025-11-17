import sys
import os
import unittest

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
main

class TestAuth(unittest.TestCase):

    def test_hash_and_check_password(self):
        """
        Tests that a password can be hashed and then successfully verified.
        """
        password = "mysecretpassword"
        hashed_password = hash_password(password)

        self.assertTrue(check_password(password, hashed_password))

    def test_check_wrong_password(self):
        """
        Tests that a wrong password is not verified.
        """
        password = "mysecretpassword"
        wrong_password = "anotherpassword"
        hashed_password = hash_password(password)

        self.assertFalse(check_password(wrong_password, hashed_password))

if __name__ == '__main__':
    unittest.main()
