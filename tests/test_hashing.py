import unittest
import subprocess
import binascii
from time import sleep
from src.hashing import generate_hashes, save_hashes
from src.utils import load_env
from src.database_connection import get_db_connection

class TestHashing(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        load_env('tests/test.env')

        # Start the docker-compose services (PostgreSQL)
        try:
            # docker-compose --env-file tests/test.env -f tests/docker-compose.yml up -d db
            subprocess.run(['docker-compose', '--env-file', 'tests/test.env', '-f', 'tests/docker-compose.yml', 'up', '-d', 'db'], check=True)
        except subprocess.CalledProcessError as e:
            print(f'Error while starting docker services: {e}')
            raise
        sleep(10) # wait for the database to be up and running

        # Get connection to the test database
        try:
            self.connection = get_db_connection()
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f'Error connection to the database: {e}')

    @classmethod
    def tearDownClass(self):
        # Close the cursor
        try:
            if self.cursor:
                print("Closing the database cursor")
                self.cursor.close()
                print("Cursor closed")
        except Exception as e:
            print(f'Error while closing the cursor: {e}')
        # Close the connection
        try:
            if self.connection:
                print("Closing the database connection.")
                self.connection.close()
                print("Connection closed.")
        except Exception as e:
            print(f"Error while closing the connection: {e}")
        finally:
            self.connection = None

        # Clean up Docker containers and volumes
        try:
            print("Tearing down Docker containers")
            subprocess.run(['docker-compose', '--env-file', 'tests/test.env', '-f', 'tests/docker-compose.yml', 'down', '-v'], check=True)
            print("Docker containers removed")
        except subprocess.CalledProcessError as e:
            print(f'Error while tearing down containers: {e}')

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

    def test_save_hashes(self):
        '''
        Test that the hashes get successfully to the database.
        Integration test. Use a database for testing
        '''
        hashes_to_save = [('5afd40cbfba9dd237d1c4187c960b313116b0abc', 0),
                           ('9babb08f1a8d2431407adf182beb650cc14a0f5e', 0),
                           ('af0c49f456b4d2d50dab3c54a6fb48441d7f3d68', 0),
                           ('3f25c720f131169aaea7f8acbbf733178366f495', 55),
                           ('03c20cb84a4aef2383ae97df8cbcf5db8eea69a6', 55),
                           ('fa165ba6086eadedd5e422cddd54ed7ee3c99375', 100)]
        # Save the hashes to the database
        save_hashes(audio_id=1, hashes=hashes_to_save)
        # Retrieve the hashes and make sure they are as expected
        self.cursor.execute("SELECT fingerprint, time_offset FROM audio_fingerprints WHERE audio_id = 1")
        result = self.cursor.fetchall()
        result = [(binascii.hexlify(bytes(h)).decode('utf-8'), t) for h, t in result]
        # Assert the result
        self.assertEqual(set(result), set(hashes_to_save))
