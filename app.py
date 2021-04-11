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
    bonding_length = db.FloatField(required = True)  #between 0.0001-5
    dimension_type = db.StringField(required = True, max_length = 64)
    material = db.ReferenceField('Material', required=True)
    
    def to_json(self):
        if self.size_c:
            return {"id": str(self.id), "size a": self.size_a, "size b": self.size_b, "size c": self.size_c, "bonding length": self.bonding_length, "dimension type": self.dimension_type, "material": self.material.to_json()}
        else:
            return {"id": str(self.id), "size a": self.size_a, "size b": self.size_b, "bonding length": self.bonding_length, "dimension type": self.dimension_type, "material": self.material.to_json() }

class Material_Fermi(db.Document):  #class for Fermi energy
    id = db.ObjectIdField(db_field = '_id')
    fermi = db.FloatField(required = True)
    material = db.ReferenceField('Material', required=True)
    volume = db.ReferenceField('Material_Volume', required=True)      

    def to_json(self):
        return {"id": str(self.id), "fermi": self.fermi, "material": self.material.to_json(), "volume": self.volume.to_json()}  

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
            return obj, 200 
    
    def post(self):
        try:
            record = json.loads(request.data)
        except KeyError:
            return {'error': 'wrong format'}, 400
        try:
            if Material.objects(structure_name = record['name']).first() is None:
                material = Material(structure_name = record['name'])
                save = material.save()
                loc = api.url_for(MaterialEntry, handle=save.structure_name)
                return Response(status=201, headers={"Location": loc})
            abort(409)
        except ValidationError:
            return {'error': 'wrong attribute types'}, 400

class MaterialEntry(Resource):

    def get(self, handle):
        material = Material.objects(structure_name=handle).first()
        if not material:
            return {'error': 'data not found'}, 403
        else:
            material.to_json()
            return material.to_json(), 200

    def put(self, handle):
        try:
            record = json.loads(request.data)
        except KeyError:
            return {'error': 'wrong format'}, 400
        
        material = Material.objects(structure_name=handle).first()
        if not material:
            return {'error': 'data not found'}, 403
        else:
            Material.objects(structure_name=handle).update(set__structure_name=record['handle'])

            return Response(status=204)
        


    def delete(self, handle):
        material = Material.objects(structure_name=handle).first()
        if not material:
            return {'error': 'deletable entry not found'}, 403
        else:
            Material.objects(id=material.id).delete()
            return Response(status=200)

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
                material_volume = Material_Volume(
                        size_a = record['size a'],
                        size_b = record['size b'],
                        size_c = record['size c'],
                        dimension_type = record['dimension type'],
                        bonding_length = record['bonding length'],
                        material = material.id
                    )
            else:
                material_volume = Material_Volume(
                        size_a = record['size a'],
                        size_b = record['size b'],
                        dimension_type = record['dimension type'],
                        bonding_length = record['bonding length'],
                        material = material.id
                    )
            material_volume.save()
            loc = api.url_for(MaterialVolumeEntry, id=material_volume.pk)
            return Response(status=201,headers={"Location": loc})#, headers={"Location": loc}
        except ValidationError:
            return {'error': 'wrong attribute type'}, 400

class MaterialVolumeEntry(Resource):

    def get(self, id):
        material_volume = Material_Volume.objects(id=id).first()
        if not material_volume:
            return {'error': 'data not found'}, 403
        else:
            return material_volume.to_json(), 200

    def put(self, id):
        try:
            record = json.loads(request.data)
            material_volume = Material_Volume.objects(id=id).first()
            material = Material.objects(structure_name=record['material']).first()
            print(material.structure_name)
        except KeyError:
            return {'error': 'wrong format'}, 400 
        if not material_volume:
            return {'error': 'editable not found'}, 403
        try:
            if 'size c' in record:
                Material_Volume.objects(id=id).update(set__size_a=record['size a'],set__size_b=record['size b'],
                set__size_c=record['size c'],set__dimension_type=record['dimension type'],set__bonding_length=record['bonding length'],set__material=material.id)
            else:
                Material_Volume.objects(id=id).update(set__size_a=record['size a'],set__size_b=record['size b'],
                set__dimension_type=record['dimension type'],set__bonding_length=record['bonding length'],set__material=material.id)
            return Response(status=204)
        except IndexError: #ValidationError
            return {'error': 'wrong attribute type'}, 400

    
    def delete(self, id):
        material_volume = Material_Volume.objects(id=id).first()
        if not material_volume:
            return {'error': 'data not found'}, 403
        else:            
            Material_Volume.objects(id=str(material_volume.id)).delete()
            return Response(status=201)

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
            material = Material.objects(structure_name = record['material']).first()
            volume = Material_Volume.objects(id = record['volume']).first()
        except KeyError:
            return {'error': 'wrong format'}, 400
        try:
            if material is not None and volume is not None:
                material_fermi = Material_Fermi(fermi = record['fermi'], material = material.id, volume = volume.id)
                material_fermi.save()
                loc = api.url_for(MaterialFermiEntry, id=material_fermi.to_json()['id'])
                return Response(status=201, headers={"Location": loc})
            return {'error': 'duplicate value'}, 409
        except ValidationError:
            return {'error': 'wrong attribute type'}, 400       

class MaterialFermiEntry(Resource):

    def get(self, id):
        material_fermi = Material_Fermi.objects(id=id).first()
        if not material_fermi:
            return {'error': 'data not found'}, 403
        else:
            return material_fermi.to_json(), 200

    def put(self, id):
        try:
            record = json.loads(request.data)
            material_fermi = Material_Fermi.objects(id=id).first()
            material_volume = Material_Volume.objects(id=record['volume id']).first()
            material = Material.objects(structure_name=record['material']).first()
            print("s")
        except KeyError:
            return {'error': 'wrong format'}, 400
        try:
            if not material_fermi:
                return {'error': 'editable not foud'}, 403
            else:
                Material_Fermi.objects(id=id).update(set__fermi=record['fermi'], set__material = material.id, set__volume = material_volume.id)
                
                return Response(status=204)
        except ValidationError:
            return {'error': 'wrong attribute type'}, 400       
    
    def delete(self, id):
        material_fermi = Material_Fermi.objects(id=id).first()
        if not material_fermi:
            return {'error': 'deletable not found'}, 403
        else:
            Material_Fermi.objects(id=str(material_fermi.id)).delete()
            return Response(status=201)


# Collections
api.add_resource(MaterialCollection, "/api/material/")
api.add_resource(MaterialVolumeCollection, "/api/material_volume/")
api.add_resource(MaterialFermiCollection, "/api/material_fermi/")
# Entries
api.add_resource(MaterialEntry, "/api/material/<handle>/")
api.add_resource(MaterialVolumeEntry, "/api/material_volume/<id>/")
api.add_resource(MaterialFermiEntry, "/api/material_fermi/<id>/")


if __name__ == '__main__':
    app.run(debug=True)