import unittest
from app import app
from mongoengine import connect, disconnect
import json
from flask import Flask, request, jsonify


class BasicTestCase(unittest.TestCase):
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Try /api/')

    def test_get_material(self):
        tester = app.test_client(self)
        response = tester.get(
            '/api/material/', content_type='application/json')
        resp = json.loads(response.data)
        comparison_data = {'@namespaces': {'material_db': {'name': '/material/link-relations/'}}, '@controls': {'self': {'href': '/api/material/'}, '${MATERIAL_DB}:material-all': {'method': 'GET', 'title': 'Get all material objects', 'href': '/api/material/'}, '${MATERIAL_DB}:add-material': {'method': 'POST', 'encoding': 'json', 'title': 'Add a new material', 'schema': {'type': 'object', 'required': ['structure_name'], 'properties': {'structure_name': {
            'description': "Material's structure name", 'type': 'string'}}}, 'href': '/api/material/'}}, 'items': [{'structure_name': 'a', '@controls': {'self': {'href': '/api/material/a/'}, 'profile': {'href': '/profiles/material/'}}}, {'structure_name': 'b', '@controls': {'self': {'href': '/api/material/b/'}, 'profile': {'href': '/profiles/material/'}}}, {'structure_name': 'c', '@controls': {'self': {'href': '/api/material/c/'}, 'profile': {'href': '/profiles/material/'}}}]}
        print("response up", resp)
        print("comparison_data up", comparison_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp, comparison_data)

    # def test_other(self):
    #         tester = app.test_client(self)
    #         response = tester.get('a', content_type='html/text')
    #         self.assertEqual(response.status_code, 404)
    #         self.assertTrue(b'does not exist' in response.data)
if __name__ == '__main__':
    unittest.main()
