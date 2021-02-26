import unittest
from app import app
from mongoengine import connect, disconnect
import json


class BasicTestCase(unittest.TestCase):
    
    longMessage = True

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost', alias='testdb')

    @classmethod
    def tearDownClass(cls):
       disconnect()

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello World!')
        
        
    def test_get_material(self):
        tester = app.test_client(self)
        response = tester.get('/material/', content_type='application/json')
        print("setting up", response.data.decode('UTF-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('UTF-8'), 
            [{
                "id":"603773b204b4a0c9781eb187",
                "structure name" : "H"
            },{
                "id":"603773b704b4a0c9781eb188",
                "structure name" : "He"
            }]
        )
        
    # def test_other(self):
    #         tester = app.test_client(self)
    #         response = tester.get('a', content_type='html/text')
    #         self.assertEqual(response.status_code, 404)
    #         self.assertTrue(b'does not exist' in response.data)
if __name__ == '__main__':
    unittest.main()