import unittest
from app import Material_Fermi, Material_Volume, Material, app
import json
 
 
MASON = 'application/vnd.mason+json'
 
 
class BasicTestCase(unittest.TestCase):
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Try /api/')
 
    def test_get_material(self):
        tester = app.test_client(self)
        response = tester.get('/api/material/', content_type=MASON)
        resp = json.loads(response.data)
        comparison_data = {
            "@namespaces": {
                "material_db": {
                    "name": "/material/link-relations/"
                }
            },
            "@controls": {
                "self": {
                    "href": "/api/material/"
                },
                "material_db:material-all": {
                    "method": "GET",
                    "title": "Get all material objects",
                    "href": "/api/material/"
                },
                "material_db:add-material": {
                    "method": "POST",
                    "encoding": "json",
                    "title": "Add a new material",
                    "schema": {
                        "type": "object",
                        "required": [
                            "structure_name"
                        ],
                        "properties": {
                            "structure_name": {
                                "description": "Material's structure name",
                                "type": "string"
                            }
                        }
                    },
                    "href": "/api/material/"
                }
            },
            "items": [
                {
                    "structure_name": "a",
                    "@controls": {
                        "self": {
                            "href": "/api/material/a/"
                        },
                        "profile": {
                            "href": "/profiles/material/"
                        }
                    }
                },
                {
                    "structure_name": "b",
                    "@controls": {
                        "self": {
                            "href": "/api/material/b/"
                        },
                        "profile": {
                            "href": "/profiles/material/"
                        }
                    }
                },
                {
                    "structure_name": "c",
                    "@controls": {
                        "self": {
                            "href": "/api/material/c/"
                        },
                        "profile": {
                            "href": "/profiles/material/"
                        }
                    }
                }
            ]
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp, comparison_data)
 
    def test_get_material_entry(self):
        tester = app.test_client(self)
        response = tester.get('/api/material/c/', content_type=MASON)
        resp = json.loads(response.data)
        comparison_data = {
            "structure_name": "c",
            "@namespaces": {
                "material_db": {
                    "name": "/material/link-relations/"
                }
            },
            "@controls": {
                "self": {
                    "href": "/api/material/c/"
                },
                "profile": {
                    "href": "/profiles/material/"
                },
                "collection": {
                    "href": "/api/material/"
                },
                "edit": {
                    "method": "PUT",
                    "encoding": "json",
                    "schema": {
                        "type": "object",
                        "required": [
                            "structure_name"
                        ],
                        "properties": {
                            "structure_name": {
                                "description": "Material's structure name",
                                "type": "string"
                            }
                        }
                    },
                    "href": "/api/material/c/"
                },
                "material_db:delete": {
                    "method": "DELETE",
                    "title": "Delete this resource",
                    "href": "/api/material/c/"
                }
            }
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp, comparison_data)
 
    def test_get_material_volume(self):
        tester = app.test_client(self)
        response = tester.get('/api/material_volume/', content_type=MASON)
        volumes = Material_Volume.objects().all()
        resp = json.loads(response.data)
        comparison_data = {
            "@namespaces": {
                "material_db": {
                    "name": "/material/link-relations/"
                }
            },
            "@controls": {
                "self": {
                    "href": "/api/material_volume/"
                },
                "material_db:material_volume-all": {
                    "method": "GET",
                    "title": "Get all material volume objects",
                    "href": "/api/material_volume/"
                },
                "material_db:add_material_volume": {
                    "method": "POST",
                    "encoding": "json",
                    "title": "Add a new material volume entry",
                    "schema": {
                        "type": "object",
                        "required": [
                            "size_a",
                            "size_b",
                            "bonding_length",
                            "dimension_type",
                            "material"
                        ],
                        "properties": {
                            "size_a": {
                                "description": "Material's first size measurement",
                                "type": "number"
                            },
                            "size_b": {
                                "description": "Material's second size measurement",
                                "type": "number"
                            },
                            "size_c": {
                                "description": "Material's third size measurement",
                                "type": "number"
                            },
                            "bonding_length": {
                                "description": "Material's bonding length",
                                "type": "number"
                            },
                            "dimension_type": {
                                "description": "Material's dimension",
                                "type": "string"
                            },
                            "material": {
                                "description": "Material for reference",
                                "type": "string"
                            }
                        }
                    },
                    "href": "/api/material_volume/"
                }
            },
            "items": [
                {
                    "size_a": 1.1,
                    "size_b": 1.11,
                    "size_c": 1.111,
                    "bonding_length": 1.0,
                    "dimension_type": "3d",
                    "material": "a",
                    "@controls": {
                        "self": {
                            "href": "/api/material_volume/" + str(volumes[0].id) + "/"
                        },
                        "profile":{
                            "href": "/profiles/material_volume/"
                        },
                        "ref_material": {
                            "href": "/api/material/a/"
                        }
                    }
                },
                {
                    "size_a": 1.2,
                    "size_b": 1.22,
                    "size_c": 1.222,
                    "bonding_length": 2.0,
                    "dimension_type": "3d",
                    "material": "b",
                    "@controls": {
                        "self": {
                            "href": "/api/material_volume/" + str(volumes[1].id) + "/"
                        },
                        "profile":{
                            "href": "/profiles/material_volume/"
                        },
                        "ref_material": {
                            "href": "/api/material/b/"
                        }
                    }
                },
                {
                    "size_a": 1.3,
                    "size_b": 1.33,
                    "bonding_length": 3.0,
                    "dimension_type": "2d",
                    "material": "c",
                    "@controls": {
                        "self": {
                            "href": "/api/material_volume/" + str(volumes[2].id) + "/"
                        },
                        "profile":{
                            "href": "/profiles/material_volume/"
                        },
                        "ref_material": {
                            "href": "/api/material/c/"
                        }
                    }
                }
            ]
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp, comparison_data)
 
    def test_get_material_volume_entry(self):
        tester = app.test_client(self)
        volumes = Material_Volume.objects().all()
        response = tester.get("/api/material_volume/" +
                              str(volumes[0].id) + "/", content_type=MASON)
        resp = json.loads(response.data)
        comparison_data = {
            "size_a": 1.1,
            "size_b": 1.11,
            "size_c": 1.111,
            "bonding_length": 1.0,
            "dimension_type": "3d",
            "material": "a",
            "@namespaces": {
                "material_db": {
                    "name": "/material/link-relations/"
                }
            },
            "@controls": {
                "self": {
                    "href": "/api/material_volume/" + str(volumes[0].id) + "/"
                },
                "profile": {
                    "href": "/profiles/material_volume/"
                },
                "collection": {
                    "href": "/api/material_volume/"
                },
                "edit": {
                    "method": "PUT",
                    "encoding": "json",
                    "schema": {
                        "type": "object",
                        "required": [
                            "size_a",
                            "size_b",
                            "bonding_length",
                            "dimension_type",
                            "material"
                        ],
                        "properties": {
                            "size_a": {
                                "description": "Material's first size measurement",
                                "type": "number"
                            },
                            "size_b": {
                                "description": "Material's second size measurement",
                                "type": "number"
                            },
                            "size_c": {
                                "description": "Material's third size measurement",
                                "type": "number"
                            },
                            "bonding_length": {
                                "description": "Material's bonding length",
                                "type": "number"
                            },
                            "dimension_type": {
                                "description": "Material's dimension",
                                "type": "string"
                            },
                            "material": {
                                "description": "Material for reference",
                                "type": "string"
                            }
                        }
                    },
                    "href": "/api/material_volume/" + str(volumes[0].id) + "/"
                },
                "material_db:delete_material_volume": {
                    "method": "DELETE",
                    "title": "Delete this resource",
                    "href": "/api/material_volume/" + str(volumes[0].id) + "/"
                }
            }
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp, comparison_data)
 
    def test_get_material_fermi(self):
        tester = app.test_client(self)
        response = tester.get('/api/material_fermi/', content_type=MASON)
        fermies = Material_Fermi.objects().all()
        resp = json.loads(response.data)
        comparison_data = {
            "@namespaces": {
                "material_db": {
                    "name": "/material/link-relations/"
                }
            },
            "@controls": {
                "self": {
                    "href": "/api/material_fermi/"
                },
                "material_db:material_fermi-all": {
                    "method": "GET",
                    "title": "Get all material fermi objects",
                    "href": "/api/material_fermi/"
                },
                "material_db:add-material_fermi": {
                    "method": "POST",
                    "encoding": "json",
                    "title": "Add a new material fermi entry",
                    "schema": {
                        "type": "object",
                        "required": [
                            "fermi",
                            "material",
                            "volume"
                        ],
                        "properties": {
                            "fermi": {
                                "description": "Material'sfermi energy",
                                "type": "number"
                            },
                            "volume": {
                                "description": "Volume for reference",
                                "type": "string"
                            },
                            "material": {
                                "description": "Material for reference",
                                "type": "string"
                            }
                        }
                    },
                    "href": "/api/material_fermi/"
                }
            },
            "items": [
                {
                    "fermi": 0.42,
                    "material": "a",
                    "volume": str(fermies[0].volume.id),
                    "@controls":{
                        "self": {
                            "href": "/api/material_fermi/" + str(fermies[0].id) + "/"
                        },
                        "profile":{
                            "href": "/profiles/material_fermi/"
                        },
                        "ref_material": {
                            "href": "/api/material/a/"
                        },
                        "ref_volume": {
                            "href": "/api/material_volume/" + str(fermies[0].volume.id) + "/"
                        }
                    }
                },
                {
                    "fermi": 0.42,
                    "material": "b",
                    "volume": str(fermies[1].volume.id),
                    "@controls":{
                        "self": {
                            "href": "/api/material_fermi/" + str(fermies[1].id) + "/"
                        },
                        "profile":{
                            "href": "/profiles/material_fermi/"
                        },
                        "ref_material": {
                            "href": "/api/material/b/"
                        },
                        "ref_volume": {
                            "href": "/api/material_volume/" + str(fermies[1].volume.id) + "/"
                        }
                    }
                },
                {
                    "fermi": 0.42,
                    "material": "c",
                    "volume": str(fermies[2].volume.id),
                    "@controls":{
                        "self": {
                            "href": "/api/material_fermi/" + str(fermies[2].id) + "/"
                        },
                        "profile":{
                            "href": "/profiles/material_fermi/"
                        },
                        "ref_material": {
                            "href": "/api/material/c/"
                        },
                        "ref_volume": {
                            "href": "/api/material_volume/" + str(fermies[2].volume.id) + "/"
                        }
                    }
                }
            ]
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp, comparison_data)
 
    def test_get_material_fermi_entry(self):
        tester = app.test_client(self)
        fermies = Material_Fermi.objects().all()
        response = tester.get("/api/material_fermi/" +
                              str(fermies[0].id) + "/", content_type=MASON)
        resp = json.loads(response.data)
        comparison_data = {
            "id": str(fermies[0].id),
            "fermi": 0.42,
            "material": "a",
            "volume": str(fermies[0].volume.id),
            "@namespaces": {
                "material_db": {
                    "name": "/material/link-relations/"
                }
            },
            "@controls": {
                "self": {
                    "href": "/api/material_fermi/" + str(fermies[0].id) + "/"
                },
                "profile": {
                    "href": "/profiles/material_fermi/"
                },
                "collection": {
                    "href": "/api/material_fermi/"
                }, "edit": {
                    "method": "PUT",
                    "encoding": "json",
                    "schema": {
                        "type": "object",
                        "required": [
                            "fermi",
                            "material",
                            "volume"
                        ],
                        "properties": {
                            "fermi": {
                                "description": "Material'sfermi energy",
                                "type": "number"
                            },
                            "volume": {
                                "description": "Volume for reference",
                                "type": "string"
                            },
                            "material": {
                                "description": "Material for reference",
                                "type": "string"
                            }
                        }
                    },
                    "href": "/api/material_fermi/" + str(fermies[0].id) + "/"
                },
                "material_db:delete": {
                    "method": "DELETE",
                    "title": "Delete this resource",
                    "href": "/api/material_fermi/" + str(fermies[0].id) + "/"
                }
            }
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp, comparison_data)
 
#  HTTPS PUTS
    def test_put_material_fermi_entry(self):
        tester = app.test_client(self)
        fermies = Material_Fermi.objects().all()
        put_data = {
            "id": str(fermies[0].id),
            "fermi": 100.0,
            "material": str(fermies[0].material.structure_name),
            "volume id": str(fermies[0].volume.id)
        }
        response = tester.put("/api/material_fermi/" + str(fermies[0].id) + "/", data=json.dumps(put_data))
        self.assertEqual(response.status_code, 204)
        put_data['fermi'] = 0.42
        tester.put("/api/material_fermi/" + str(fermies[0].id) + "/", data=json.dumps(put_data))
 
    def test_put_material_volume_entry(self):
        tester = app.test_client(self)
        volumes = Material_Volume.objects().all()
        put_data = {
            "id": str(volumes[0].id),
            "size a": 100.0,
            "size b": 200.0,
            "size c": 300.0,
            "dimension type": "4D",
            "bonding length": 0.69,
            "material": str(volumes[0].material.structure_name)
        }
        response = tester.put("/api/material_volume/" + str(volumes[0].id) + "/", data=json.dumps(put_data))
        self.assertEqual(response.status_code, 204)
        put_data['size a'] = 1.1
        put_data['size b'] = 1.11
        put_data['size c'] = 1.111
        put_data['bonding length'] = 1.0
        put_data['dimension type'] = "3d"
        tester.put("/api/material_volume/" + str(volumes[0].id) + "/", data=json.dumps(put_data))
 
    def test_put_material_entry(self):
        tester = app.test_client(self)
        materials = Material.objects().all()
        put_data = {
            "handle": "H2O"
        }
        response = tester.put("/api/material/" + str(materials[0].structure_name) + "/", data=json.dumps(put_data))
        self.assertEqual(response.status_code, 204)
        put_data['handle'] = "a"
        tester.put("/api/material/" + str(materials[0].structure_name) + "/", data=json.dumps(put_data))
 
    def test_post_and_delete_material_fermi(self):
        tester = app.test_client(self)
        volumes = Material_Volume.objects().first()
        post_data = {
            "fermi": 123.0,
            "material": str(volumes.material.structure_name),
            "volume": str(volumes.id)
        }
        response = tester.post("/api/material_fermi/", data=json.dumps(post_data))
        self.assertEqual(response.status_code, 201)
        fermi = Material_Fermi.objects(fermi=123.0).all()
        self.assertEqual(len(fermi), 1)
        response = tester.delete("/api/material_fermi/" + str(fermi[0].id) + "/")
        self.assertEqual(response.status_code, 201)
        fermi = Material_Fermi.objects(fermi=123.0).all()
        self.assertEqual(len(fermi), 0)
 
    def test_post_and_delete_material_volume(self):
        tester = app.test_client(self)
        materials = Material.objects().first()
        post_data = {
            "size a": 101.0,
            "size b": 202.0,
            "size c": 303.0,
            "dimension type": "3D",
            "bonding length": 0.42,
            "material": str(materials.structure_name)
        }
        response = tester.post("/api/material_volume/", data=json.dumps(post_data))
        self.assertEqual(response.status_code, 201)
        volume = Material_Volume.objects(size_c=303.0).all()
        self.assertEqual(len(volume), 1)
        response = tester.delete("/api/material_volume/" + str(volume[0].id) + "/")
        self.assertEqual(response.status_code, 201)
        volume = Material_Volume.objects(size_c=303.0).all()
        self.assertEqual(len(volume), 0)
 
    def test_post_and_delete_material(self):
        tester = app.test_client(self)
        post_data = {
            "name": "test"
        }
        response = tester.post("/api/material/", data=json.dumps(post_data))
        self.assertEqual(response.status_code, 201)
        material = Material.objects(structure_name="test").all()
        self.assertEqual(len(material), 1)
        response = tester.delete("/api/material/" + str(material[0].structure_name) + "/")
        self.assertEqual(response.status_code, 201)
        material = Material.objects(structure_name="test").all()
        self.assertEqual(len(material), 0)
 
if __name__ == '__main__':
    unittest.main()
    
