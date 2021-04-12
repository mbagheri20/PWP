import unittest
from app import app
from mongoengine import connect, disconnect
import json
from flask import Flask, request, jsonify
 
 
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
        resp =  json.loads(response.data)
        comparison_data =  {
                            "@namespaces":{
                                "material_db":{
                                    "name": "/material/link-relations/"
                            }
                            },
                            "@controls":{
                                "self":{
                                "href": "/api/material/"
                            },
                            "${MATERIAL_DB}:material-all":{
                                "method": "GET",
                                "title": "Get all material objects",
                                "href": "/api/material/"
                            },
                            "${MATERIAL_DB}:add-material":{
                                "method": "POST",
                                "encoding": "json",
                                "title": "Add a new material",
                                "schema":{
                                    "type": "object",
                                    "required":[
                                        "structure_name"
                                    ],
                                    "properties":{
                                        "structure_name":{
                                            "description": "Material's structure name",
                                            "type": "string"
                                        }
                                    }
                                },
                                "href": "/api/material/"
                            }
                            },
                            "items":[
                                {
                                    "structure_name": "a",
                                    "@controls":{
                                        "self":{
                                            "href": "/api/material/a/"
                                        },
                                        "profile":{
                                            "href": "/profiles/material/"
                                        }
                                    }
                                },
                                {
                                    "structure_name": "b",
                                    "@controls":{
                                        "self":{
                                            "href": "/api/material/b/"
                                        },
                                        "profile":{
                                            "href": "/profiles/material/"
                                        }
                                    }
                                },
                                {
                                    "structure_name": "c",
                                    "@controls":{
                                        "self":{
                                        "href": "/api/material/c/"
                                        },
                                        "profile":{
                                            "href": "/profiles/material/"
                                        }
                                    }
                                }
                            ]
                            }
        print("response up", resp)
        print("comparison_data up", comparison_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp, comparison_data)
 
    def test_get_material_entry(self):
        tester = app.test_client(self)
        response = tester.get('/api/material/c/', content_type=MASON)
        resp =  json.loads(response.data)
        comparison_data =  {
                            "structure_name": "c",
                            "@namespaces":{
                                "material_db":{
                                    "name": "/material/link-relations/"
                                }
                            },
                            "@controls":{
                                "self":{
                                    "href": "/api/material/c/"
                                },
                                "profile":{
                                    "href": "/profiles/material/"
                                },
                                "collection":{
                                    "href": "/api/material/"
                                },
                                "edit":{
                                    "method": "PUT",
                                    "encoding": "json",
                                    "schema":{
                                        "type": "object",
                                        "required":[
                                            "structure_name"
                                        ],
                                        "properties":{
                                            "structure_name":{
                                                "description": "Material's structure name",
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "href": "/api/material/c/"
                                },
                                "${MATERIAL_DB}:delete":{
                                    "method": "DELETE",
                                    "title": "Delete this resource",
                                    "href": "/api/material/c/"
                                }
                            }
                            }
        print("response up", resp)
        print("comparison_data up", comparison_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp, comparison_data)
 
    def test_get_material_volume(self):
        tester = app.test_client(self)
        response = tester.get('/api/material_volume/', content_type=MASON)
        resp =  json.loads(response.data)
        comparison_data =   {
                                "@namespaces":{
                                    "material_db":{
                                        "name": "/material/link-relations/"
                                    }
                                },
                                "@controls":{
                                    "self":{
                                        "href": "/api/material_volume/"
                                    },
                                    "${MATERIAL_DB}:material_volume-all":{
                                        "method": "GET",
                                        "title": "Get all material volume objects",
                                        "href": "/api/material_volume/"
                                    },
                                    "${MATERIAL_DB}:add_material_volume":{
                                        "method": "POST",
                                        "encoding": "json",
                                        "title": "Add a new material volume entry",
                                        "schema":{
                                            "type": "object",
                                            "required":[
                                                "size_a",
                                                "size_b",
                                                "bonding_length",
                                                "dimension_type",
                                                "material"
                                            ],
                                            "properties":{
                                                "size_a":{
                                                    "description": "Material's first size measurement",
                                                    "type": "number"
                                                },
                                                "size_b":{
                                                    "description": "Material's second size measurement",
                                                    "type": "number"
                                                },
                                                "size_c":{
                                                    "description": "Material's third size measurement",
                                                    "type": "number"
                                                },
                                                "bonding_length":{
                                                    "description": "Material's bonding length",
                                                    "type": "number"
                                                },
                                                "dimension_type":{
                                                    "description": "Material's dimension",
                                                    "type": "string"
                                                },
                                                "material":{
                                                    "description": "Material for reference",
                                                    "type": "string"
                                                }
                                            }
                                        },
                                        "href": "/api/material_volume/"
                                    }
                                    },
                                "items":[
                                    {
                                        "size_a": 1.1,
                                        "size_b": 1.11,
                                        "size_c": 1.111,
                                        "bonding_length": 1.0,
                                        "dimension_type": "3d",
                                        "material": "a",
                                        "@controls":{
                                            "self":{
                                                "href": "/api/material_volume/6074393a57a24bd9e0038dc3/"
                                            },
                                            "profile":{
                                                "href": "/profiles/material_volume/"
                                            },
                                            "ref_material":{
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
                                        "@controls":{
                                            "self":{
                                                "href": "/api/material_volume/6074393a57a24bd9e0038dc4/"
                                            },
                                            "profile":{
                                                "href": "/profiles/material_volume/"
                                            },
                                            "ref_material":{
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
                                        "@controls":{
                                            "self":{
                                                "href": "/api/material_volume/6074393a57a24bd9e0038dc5/"
                                            },
                                            "profile":{
                                                "href": "/profiles/material_volume/"
                                            },
                                            "ref_material":{
                                                "href": "/api/material/c/"
                                            }
                                        }
                                    }
                                ]
                            }
        print("response up", resp)
        print("comparison_data up", comparison_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp, comparison_data)
 
    def test_get_material_volume_entry(self):
            tester = app.test_client(self)
            response = tester.get('/api/material_volume/6074393a57a24bd9e0038dc5/', content_type=MASON)
            resp =  json.loads(response.data)
            comparison_data =  {
                                "size_a": 1.3,
                                "size_b": 1.33,
                                "size_c": None,
                                "bonding_length": 3.0,
                                "dimension_type": "2d",
                                "material": "c",
                                "@namespaces":{
                                    "material_db":{
                                        "name": "/material/link-relations/"
                                    }
                                },
                                "@controls":{
                                    "self":{
                                        "href": "/api/material_volume/6074393a57a24bd9e0038dc5/"
                                    },
                                    "profile":{
                                        "href": "/profiles/material_volume/"
                                    },
                                    "collection":{
                                        "href": "/api/material_volume/"
                                    },
                                    "edit":{
                                        "method": "PUT",
                                        "encoding": "json",
                                        "schema":{
                                            "type": "object",
                                            "required":[
                                                "size_a",
                                                "size_b",
                                                "bonding_length",
                                                "dimension_type",
                                                "material"
                                            ],
                                            "properties":{
                                                "size_a":{
                                                    "description": "Material's first size measurement",
                                                    "type": "number"
                                                },
                                                "size_b":{
                                                    "description": "Material's second size measurement",
                                                    "type": "number"
                                                },
                                                "size_c":{
                                                    "description": "Material's third size measurement",
                                                    "type": "number"
                                                },
                                                "bonding_length":{
                                                    "description": "Material's bonding length",
                                                    "type": "number"
                                                },
                                                "dimension_type":{
                                                    "description": "Material's dimension",
                                                    "type": "string"
                                                },
                                                "material":{
                                                    "description": "Material for reference",
                                                    "type": "string"
                                                }
                                            }
                                        },
                                    "href": "/api/material_volume/6074393a57a24bd9e0038dc5/"
                                    },
                                    "${MATERIAL_DB}:delete_material_volume":{
                                        "method": "DELETE",
                                        "title": "Delete this resource",
                                        "href": "/api/material_volume/6074393a57a24bd9e0038dc5/"
                                    }
                                }
                                }
            print("response up", resp)
            print("comparison_data up", comparison_data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(resp, comparison_data)
 
 
    def test_get_material_fermi(self):
        tester = app.test_client(self)
        response = tester.get('/api/material_fermi/', content_type=MASON)
        resp =  json.loads(response.data)
        comparison_data =   {
                            "@namespaces":{
                                "material_db":{
                                    "name": "/material/link-relations/"
                                }
                                },
                                    "@controls":{
                                        "self":{
                                            "href": "/api/material_fermi/"
                                        },
                                        "${MATERIAL_DB}:material_fermi-all":{
                                            "method": "GET",
                                            "title": "Get all material fermi objects",
                                            "href": "/api/material_fermi/"
                                        },
                                        "${MATERIAL_DB}:add-material_fermi":{
                                            "method": "POST",
                                            "encoding": "json",
                                            "title": "Add a new material fermi entry",
                                            "schema":{
                                                "type": "object",
                                                "required":[
                                                    "fermi",
                                                    "material",
                                                    "volume"
                                                ],
                                                "properties":{
                                                    "fermi":{
                                                        "description": "Material'sfermi energy",
                                                        "type": "number"
                                                    },
                                                    "volume":{
                                                        "description": "Volume for reference",
                                                        "type": "string"
                                                    },
                                                    "material":{
                                                        "description": "Material for reference",
                                                        "type": "string"
                                                    }
                                                }
                                            },
                                            "href": "/api/material_fermi/"
                                        }
                                    },
                                    "items":[
                                        {
                                            "fermi": 0.42,
                                            "material": "a",
                                            "volume": "6074393a57a24bd9e0038dc3",
                                            "@controls":{
                                                "self":{
                                                    "href": "/api/material_fermi/6074393a57a24bd9e0038dc6/"
                                                },
                                                "profile":{
                                                    "href": "/profiles/material_fermi/"
                                                },
                                                "ref_material":{
                                                    "href": "/api/material/a/"
                                                },
                                                "ref_volume":{
                                                    "href": "/api/material_volume/6074393a57a24bd9e0038dc3/"
                                                }
                                            }
                                        },
                                        {
                                            "fermi": 0.42,
                                            "material": "b",
                                            "volume": "6074393a57a24bd9e0038dc4",
                                            "@controls":{
                                                "self":{
                                                    "href": "/api/material_fermi/6074393a57a24bd9e0038dc7/"
                                                },
                                                "profile":{
                                                    "href": "/profiles/material_fermi/"
                                                },
                                                "ref_material":{
                                                    "href": "/api/material/b/"
                                                },
                                                "ref_volume":{
                                                    "href": "/api/material_volume/6074393a57a24bd9e0038dc4/"
                                                }
                                            }
                                        },
                                        {
                                            "fermi": 0.42,
                                            "material": "c",
                                            "volume": "6074393a57a24bd9e0038dc5",
                                            "@controls":{
                                                "self":{
                                                    "href": "/api/material_fermi/6074393a57a24bd9e0038dc8/"
                                                },
                                                "profile":{
                                                    "href": "/profiles/material_fermi/"
                                                },
                                                "ref_material":{
                                                    "href": "/api/material/c/"
                                                },
                                                "ref_volume":{
                                                    "href": "/api/material_volume/6074393a57a24bd9e0038dc5/"
                                                }
                                            }
                                        }
                                    ]
                            }
        print("response up", resp)
        print("comparison_data up", comparison_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp, comparison_data)
    
    def test_get_material_fermi_entry(self):
        tester = app.test_client(self)
        response = tester.get('/api/material_fermi/6074393a57a24bd9e0038dc6/', content_type=MASON)
        resp =  json.loads(response.data)
        comparison_data =   {
                                "id": "6074393a57a24bd9e0038dc6",
                                "fermi": 0.42,
                                "material": "a",
                                "volume": "6074393a57a24bd9e0038dc3",
                                "@namespaces":{
                                    "material_db":{
                                        "name": "/material/link-relations/"
                                    }
                                    },
                                    "@controls":{
                                        "self":{
                                            "href": "/api/material_fermi/6074393a57a24bd9e0038dc6/"
                                        },
                                        "profile":{
                                            "href": "/profiles/material_fermi/"
                                        },
                                        "collection":{
                                            "href": "/api/material_fermi/"
                                        },"edit":{
                                            "method": "PUT",
                                            "encoding": "json",
                                            "schema":{
                                                "type": "object",
                                                "required":[
                                                    "fermi",
                                                    "material",
                                                    "volume"
                                                ],
                                                "properties":{
                                                    "fermi":{
                                                        "description": "Material'sfermi energy",
                                                        "type": "number"
                                                    },
                                                    "volume":{
                                                        "description": "Volume for reference",
                                                        "type": "string"
                                                    },
                                                    "material":{
                                                        "description": "Material for reference",
                                                        "type": "string"
                                                    }
                                                }
                                            },
                                            "href": "/api/material_fermi/6074393a57a24bd9e0038dc6/"
                                        },
                                        "${MATERIAL_DB}:delete":{
                                            "method": "DELETE",
                                            "title": "Delete this resource",
                                            "href": "/api/material_fermi/6074393a57a24bd9e0038dc6/"
                                        }
                                    }
                            }
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