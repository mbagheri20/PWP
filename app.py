import json
from flask import Flask, request
from flask.wrappers import Response
from flask_restful import Api, Resource, abort
from flask_mongoengine import MongoEngine
from mongoengine.errors import ValidationError


app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'mongodb://localhost/db',
    'port': 27017
}
db = MongoEngine(app)

class Material(db.Document): #class for Material
    id = db.ObjectIdField(db_field = '_id')
    structure_name = db.StringField(required = True, unique = True, max_length = 50)

    def to_json(self):
        if self.id is not None:
            return {"id": str(self.id), "structure name": self.structure_name}
        return {"structure name": self.structure_name}

class Material_Volume(db.Document): #class for volume. Size_c is not necessarily needed
    id = db.ObjectIdField(db_field = '_id')
    size_a = db.FloatField(required = True)
    size_b = db.FloatField(required = True)
    size_c = db.FloatField()
    material = db.ReferenceField('Material', required=True)
    
    def to_json(self):
        if self.size_c:
            return {"id": str(self.id), "size a": self.size_a, "size b": self.size_b, "size c": self.size_c, "material": self.material.to_json()}
        else:
            return {"id": str(self.id), "size a": self.size_a, "size b": self.size_b, "material": self.material.to_json() }

class Material_Other(db.Document):  #class for Other
    id = db.ObjectIdField(db_field = '_id')
    bonding_length = db.FloatField(required = True)  #between 0.0001-5
    material = db.ReferenceField('Material', required=True)
    
    def to_json(self):
        return {"id": str(self.id), "bonding length": self.bonding_length, "material": self.material.to_json()}

class Material_Fermi(db.Document):  #class for Fermi energy
    id = db.ObjectIdField(db_field = '_id')
    fermi = db.FloatField(required = True)
    material = db.ReferenceField('Material', required=True)
    structure_type = db.ReferenceField('Material_Structure_Type', required=True)
    volume = db.ReferenceField('Material_Volume', required=True)      

    def to_json(self):
        return {"id": str(self.id), "fermi": self.fermi, "material": self.material.to_json(), "volume": self.volume.to_json(), "structure type": self.structure_type.to_json()}  

class Material_Structure_Type(db.Document): #class for structure type and dimension
    id = db.ObjectIdField(db_field = '_id')
    structure_type = db.StringField(required = True, max_length = 50)
    dimension_type = db.StringField(required = True, max_length = 64)
    material = db.ReferenceField('Material', required=True)

    def to_json(self):
        return {"id": str(self.id), "structure type": self.structure_type, "dimension type": self.dimension_type, "material": self.material.to_json()}


@app.route('/')
def home():
    return "Hello World!"


class MaterialCollection(Resource):

    def get(self):
        material = Material.objects().all()
        if not material:
            return {'error': 'data not found'}, 403
        else:
            obj = []
            for each in material:
                obj.append(each.to_json())
            return obj, 201 
    
    def post(self):
        try:
            record = json.loads(request.data)
        except KeyError:
            return {'error': 'wrong format'}, 400
        try:
            if Material.objects(structure_name = record['name']).first() is None:
                material = Material(structure_name = record['name'])
                material.save()
                return Response(status=201)
            abort(409)
        except ValidationError:
            return {'error': 'wrong attribute types'}, 400

class MaterialEntry(Resource):

    def get(self, handle):
        return Response(status=501)

class OtherMaterialCollection(Resource):
    
    def get(self):
        material_other = Material_Other.objects().all()
        if not material_other:
            return {'error': 'data not found'}, 403
        else:
            obj = []
            for each in material_other:
                obj.append(each.to_json())
            return obj, 201
    
    def post(self):
        try:
            record = request.get_json()
            bonding_length = float(record['bonding length'])
            material = Material.objects(structure_name=record['material']).first()
        except KeyError:
            return {'error': 'wrong format'}, 400
        if material is not None:
            try:
                material_other = Material_Other(
                    bonding_length=bonding_length,
                    material=material.id,
                    )
                material_other.save()
                return material_other.to_json(), 200
            except ValidationError:
                return {'error': 'wrong attribute type'}, 400
        return {'error': 'entry not found'}, 400

class OtherMaterialEntry(Resource):

    def get(self, handle):
        return Response(status=501)

class MaterialVolumeCollection(Resource):
    def get(self):
        material_volume = Material_Volume.objects().all()
        if not material_volume:
            return {'error': 'data not found'}, 403
        else:
            obj = []
            for each in material_volume:
                obj.append(each.to_json())
            return obj, 200
    
    def post(self):
        try:
            record = json.loads(request.data)
            material = Material.objects(structure_name=record['material']).first()
        except KeyError:

            return {'error': 'wrong format'}, 400 
        try:
            if 'size c' in record:
                material_volume = Material_Volume(size_a = record['size a'], size_b = record['size b'], size_c = record['size c'], material = material.id)
            else:
                material_volume = Material_Volume(size_a = record['size a'], size_b = record['size b'], material = material.id)
            material_volume.save()
            return material_volume.to_json()
        except ValidationError:
            return {'error': 'wrong attribute type'}, 400

class MaterialVolumeEntry(Resource):

    def get(self, handle):
        return Response(status=501)

class MaterialFermiCollection(Resource):
    def get(self):
        material_fermi = Material_Fermi.objects().all()
        if not material_fermi:
            return {'error': 'data not found'}, 403
        else:
            obj = []
            for each in material_fermi:
                obj.append(each.to_json())
            return obj, 200
   
    def post(self):
        try:
            record = json.loads(request.data)
            material = Material.objects(structure_name=record['material']).first()
            volume = Material_Volume.objects(id = record['volume']).first()
            structure_type = Material_Structure_Type.objects(id = record['structure type']).first()
        except KeyError:
            return {'error': 'wrong format'}, 400
        try:
            if material is not None and volume is not None and structure_type is not None:
                material_fermi = Material_Fermi(fermi = record['fermi'], material = material.id, volume = volume.id, structure_type = structure_type.id)
                material_fermi.save()
                return '', 201
            return {'error': 'duplicate value'}, 409
        except ValidationError:
            return {'error': 'wrong attribute type'}, 400       

class MaterialFermiEntry(Resource):

    def get(self, handle):
        return Response(status=501)

class MaterialStructureCollection(Resource):
    def get(self):
        material_structure = Material_Structure_Type.objects().all()
        if not material_structure:
            return {'error': 'data not found'}, 403
        obj = []
        for each in material_structure:
            obj.append(each.to_json())
        return obj, 200

    def post(self):
        try:
            record = json.loads(request.data)
            material = Material.objects(structure_name=record['material']).first()
        except KeyError:
            return {'error': 'wrong format'}, 400 
        try:
            material_structure = Material_Structure_Type(structure_type = record['structure type'], dimension_type = record['dimension type'], material = material.id)
            material_structure.save()
            return material_structure.to_json()
        except ValidationError:
            return {'error': 'wrong attribute type'}, 400
 
class MaterialStructureEntry(Resource):

    def get(self, handle):
        return Response(status=501)

# Collections
api.add_resource(MaterialCollection, "/api/material/")
api.add_resource(OtherMaterialCollection, "/api/material_other/")
api.add_resource(MaterialVolumeCollection, "/api/material_volume/")
api.add_resource(MaterialFermiCollection, "/api/material_fermi/")
api.add_resource(MaterialStructureCollection, "/api/material_structure/")
# Entries
api.add_resource(MaterialEntry, "/api/material/<handle>/")
api.add_resource(OtherMaterialEntry, "/api/material_other/<handle>/")
api.add_resource(MaterialVolumeEntry, "/api/material_volume/<handle>/")
api.add_resource(MaterialFermiEntry, "/api/material_fermi/<handle>/")
api.add_resource(MaterialStructureEntry, "/api/material_structure/<handle>/")


if __name__ == '__main__':
    app.run(debug=True)