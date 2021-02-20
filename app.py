import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'mongodb://localhost/db',
    'port': 27017
}
db = MongoEngine(app)

class Material(db.Document):
    structure_name = db.StringField(required = True, max_length = 50)
    
    def to_json(self):
        return {"structure name": self.structure_name}


class Material_Volume(db.Document):
    size_a = db.FloatField()        #or size_a = db.FloatField(0.0001, 20)
    size_b = db.FloatField()
    size_c = db.FloatField()

class Material_other(db.Document):
    bonding_length = db.FloatField(required = True)    #between 0.0001-5

class Material_Fermi(db.Document):
    fermi = 1.0        #was this calculated

class Material_Structure_type(db.Document):
    structure_type = db.StringField(required = True, max_length = 50)
    dimension_type = db.StringField(required = True, max_length = 64)


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
    record = json.loads(request.data)
    material = Material(structure_name = record['name'])
    material.save()
    return jsonify(material.to_json())


if __name__ == "__main__":
    app.run(debug=True)
