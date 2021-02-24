import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from mongoengine.errors import ValidationError

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'mongodb://localhost/db',
    'port': 27017
}
db = MongoEngine(app)

class Material(db.Document):    #class for Material
    structure_name = db.StringField(required = True, unique = True, max_length = 50)
    # material = db.ListField(db.ReferenceField('Material_Volume'))

    def to_json(self):
        return {"structure name": self.structure_name}


class Material_Volume(db.Document): #class for volume. Size_c is not necessarily needed
    size_a = db.FloatField(required = True)
    size_b = db.FloatField(required = True)
    size_c = db.FloatField()
    material = db.ReferenceField('Material', required=True)
    
    def to_json(self):
        if self.size_c:
            return {"size a": self.size_a, "size b": self.size_b, "size c": self.size_c, "material": self.material}
        else:
            return {"size a": self.size_a, "size b": self.size_b, "material": db.Material.find({"structure_name": self.material.structure_name}) }


class Material_Other(db.Document):  #class for Other
    bonding_length = db.FloatField(required = True)    #between 0.0001-5
    def to_json(self):
        return {"bonding length": self.bonding_length}

class Material_Fermi(db.Document):  #class for Fermi energy
    fermi = db.FloatField(required = True)      

    def to_json(self):
        return {"fermi": self.fermi}  

class Material_Structure_Type(db.Document): #class for structure type and dimension
    structure_type = db.StringField(required = True, max_length = 50)
    dimension_type = db.StringField(required = True, max_length = 64)

    def to_json(self):
        return {"structure type": self.structure_type, "dimension type": self.dimension_type}


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/material/', methods=['GET']) 
def get_material():
    material = Material.objects().first()
    if not material:
        return jsonify({'error': 'data not found'}), 403
    else:
        return jsonify(material.to_json()), 200

@app.route('/material/', methods=['POST'])
def post_material():
    try:
        record = json.loads(request.data)
    except KeyError:
        return jsonify({'error': 'wrong format'}), 400
    try:
        material = Material(structure_name = record['name'])
        material.save()
        return jsonify(material.to_json())
    except ValidationError:
        return jsonify({'error': 'wrong attribute type'}), 400


@app.route('/material_volume/', methods=['GET'])
def get_material_volume():
    material_volume = Material_Volume.objects().all()
    if not material_volume:
        return jsonify({'error': 'data not found'}), 403
    else:
        obj = []
        for each in material_volume:
            obj.append(each.to_json())
        return jsonify(obj), 200

@app.route('/material_volume/', methods=['POST'])
def post_material_volume():
    try:
        record = json.loads(request.data)
        material = Material.objects(structure_name=record['material']).first()
    except KeyError:

        return jsonify({'error': 'wrong format'}), 400 
    try:
        if 'size c' in record:
            material_volume = Material_Volume(size_a = record['size a'], size_b = record['size b'], size_c = record['size c'], material = material)
        else:
            material_volume = Material_Volume(size_a = record['size a'], size_b = record['size b'], material = material)
        material_volume.save()
        return jsonify(material_volume.to_json())
    except ValidationError:
        return jsonify({'error': 'wrong attribute type'}), 400

@app.route('/material_other/', methods=['GET'])
def get_material_other():
    material_other = Material_Other.objects().first()
    if not material_other:
        return jsonify({'error': 'data not found'}), 403
    else:
        return jsonify(material_other.to_json()), 200

@app.route('/material_other/', methods=['POST'])
def post_material_other():
    try:
        record = json.loads(request.data)
    except KeyError:
        return jsonify({'error': 'wrong format'}), 400
    try:
        material_other = Material_Other(bonding_length = record['bonding length'])
        material_other.save()
        return jsonify(material_other.to_json())
    except ValidationError:
        return jsonify({'error': 'wrong attribute type'}), 400

@app.route('/material_fermi/', methods=['GET'])
def get_material_fermi():
    material_fermi = Material_Fermi.objects().first()
    if not material_fermi:
        return jsonify({'error': 'data not found'}), 403
    else:
        return jsonify(material_fermi.to_json()), 200

@app.route('/material_fermi/', methods=['POST'])
def post_material_fermi():
    try:
        record = json.loads(request.data)
    except KeyError:
        return jsonify({'error': 'wrong format'}), 400
    try:
        material_fermi = Material_Fermi(fermi = record['fermi'])
        material_fermi.save()
        return jsonify(material_fermi.to_json())
    except ValidationError:
        return jsonify({'error': 'wrong attribute type'}), 400

@app.route('/material_structure_type/', methods=['GET'])
def get_material_structure_type():
    material_structure = Material_Structure_Type.objects().first()
    if not material_structure:
        return jsonify({'error': 'data not found'}), 403
    else:
        return jsonify(material_structure.to_json()), 200

@app.route('/material_structure_type/', methods=['POST'])
def post_material_structure_type():
    try:
        record = json.loads(request.data)
    except KeyError:
        return jsonify({'error': 'wrong format'}), 400 
    try:
        material_structure = Material_Structure_Type(structure_type = record['structure type'], dimension_type = record['dimension type'])
        material_structure.save()
        return jsonify(material_structure.to_json())
    except ValidationError:
        return jsonify({'error': 'wrong attribute type'}), 400

if __name__ == "__main__":
    app.run(debug=True)