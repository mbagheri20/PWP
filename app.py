import json
from flask import Flask, request
from flask.wrappers import Response
from flask_restful import Api, Resource
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


LINK_RELATIONS_URL = "/material/link-relations/"
MATERIAL_PROFILE = "/profiles/material/"
MATERIAL_VOLUME_PROFILE = "/profiles/material_volume/"
MATERIAL_FERMI_PROFILE = "/profiles/material_fermi/"
ERROR_PROFILE = "/profiles/errors/"
MASON = "application/vnd.mason+json"
SELF = "self"
MATERIAL_DB = "material_db"
PROFILE = "profile"
COLLECTION = "collection"
REF_MATERIAL = "ref_material"
REF_VOLUME = "ref_volume"


class MasonBuilder(dict):
    def add_error(self, title, details):
        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href


class Material(db.Document):  # class for Material
    id = db.ObjectIdField(db_field='_id')
    structure_name = db.StringField(required=True, unique=True, max_length=50)


# class for volume. Size_c is not necessarily needed
class Material_Volume(db.Document):
    id = db.ObjectIdField(db_field='_id')
    size_a = db.FloatField(required=True)
    size_b = db.FloatField(required=True)
    size_c = db.FloatField()
    bonding_length = db.FloatField(required=True)  # between 0.0001-5
    dimension_type = db.StringField(required=True, max_length=64)
    material = db.ReferenceField('Material', required=True)


class Material_Fermi(db.Document):  # class for Fermi energy
    id = db.ObjectIdField(db_field='_id')
    fermi = db.FloatField(required=True)
    material = db.ReferenceField('Material', required=True)
    volume = db.ReferenceField('Material_Volume', required=True)


@app.route('/')
def home():
    return "Try /api/"


@app.route(ERROR_PROFILE)
def error():
    return ERROR_PROFILE


@app.route("/api/")
def entrypoint():
    body = {
    }
    body["@namespaces"] = {
        MATERIAL_DB: {"name": LINK_RELATIONS_URL}
    }
    body["@controls"] = {
        MATERIAL_DB + ":material-all": {
            "href": "/api/material/",
            "method": "GET",
            "title": "Get all products"
        }
    }
    return Response(json.dumps(body), status=200)


def create_error_response(status_code, title, message=None):
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control(PROFILE, href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)


class MaterialCollection(Resource):

    def get(self):
        material = Material.objects().all()
        if not material:
            return create_error_response(
                403, "Material is missing",
                "There is no material with the given handle")
        else:
            body = MaterialBuilder()
            body.add_namespace(MATERIAL_DB, LINK_RELATIONS_URL)
            body.add_control(SELF, api.url_for(MaterialCollection))
            body.add_control_all_material()
            body.add_control_add_material()
            body["items"] = []
            for each in material:
                item = MaterialBuilder(structure_name=each.structure_name)
                item.add_control(SELF, api.url_for(
                    MaterialEntry, handle=each.structure_name))
                item.add_control(PROFILE, MATERIAL_PROFILE)
                body["items"].append(item)
            return Response(json.dumps(body), 200, mimetype=MASON)

    def post(self):
        try:
            record = json.loads(request.data)
        except KeyError:
            return create_error_response(
                400, "KeyError",
                "wrong format")
        try:
            if Material.objects(structure_name=record['name']).first() is None:
                material = Material(structure_name=record['name'])
                save = material.save()
                loc = api.url_for(MaterialEntry, handle=save.structure_name)
                return Response(status=201, headers={"Location": loc})
            return create_error_response(
                409, "Values missing",
                "All values not present")
        except ValidationError:
            return create_error_response(
                400, "ValidationError",
                "Wrong attribute types")
        except KeyError:
            return create_error_response(
                400, "KeyError",
                "Wrong attribute types")


class MaterialEntry(Resource):

    def get(self, handle):
        material = Material.objects(structure_name=handle).first()
        if not material:
            return create_error_response(
                403, "Material is missing",
                "There is no material with the given name")
        else:
            body = MaterialBuilder(structure_name=material.structure_name)
            body.add_namespace(MATERIAL_DB, LINK_RELATIONS_URL)
            body.add_control(SELF, api.url_for(MaterialEntry, handle=handle))
            body.add_control(PROFILE, MATERIAL_PROFILE)
            body.add_control(COLLECTION, api.url_for(MaterialCollection))
            body.add_control_edit_material(handle)
            body.add_control_delete_material(handle)
            return Response(json.dumps(body), 200, mimetype=MASON)

    def put(self, handle):
        try:
            record = json.loads(request.data)
        except KeyError:
            return create_error_response(
                400, "KeyError",
                "wrong format")

        material = Material.objects(structure_name=handle).first()
        if not material:
            return create_error_response(
                403, "Material is missing",
                "There is no material with the given name")
        else:

            Material.objects(structure_name=handle).update(
                set__structure_name=record['handle'])
            return Response(status=204)

    def delete(self, handle):
        material = Material.objects(structure_name=handle).first()
        if not material:
            return create_error_response(
                403, "Material is missing",
                "There is no material with the given name")
        else:
            Material.objects(id=material.id).delete()
            return Response(status=201)


class MaterialVolumeCollection(Resource):
    def get(self):
        material_volume = Material_Volume.objects().all()
        if not material_volume:
            return create_error_response(
                403, "Material Volume is missing",
                "There is no material volume with the given id")
        else:
            body = MaterialVolumeBuilder()
            body.add_namespace(MATERIAL_DB, LINK_RELATIONS_URL)
            body.add_control(SELF, api.url_for(MaterialVolumeCollection))
            body.add_control_all_material_volume()
            body.add_control_add_material_volume()
            body["items"] = []
            for each in material_volume:
                if not each.size_c:
                    item = MaterialVolumeBuilder(size_a=each.size_a,
                                                 size_b=each.size_b,
                                                 bonding_length=each.bonding_length,
                                                 dimension_type=each.dimension_type,
                                                 material=each.material.structure_name
                                                 )
                else:
                    item = MaterialVolumeBuilder(size_a=each.size_a,
                                                 size_b=each.size_b,
                                                 size_c=each.size_c,
                                                 bonding_length=each.bonding_length,
                                                 dimension_type=each.dimension_type,
                                                 material=each.material.structure_name
                                                 )
                item.add_control(SELF, api.url_for(
                    MaterialVolumeEntry, id=each.id))
                item.add_control(PROFILE, MATERIAL_VOLUME_PROFILE)
                item.add_control(REF_MATERIAL, api.url_for(
                    MaterialEntry, handle=each.material.structure_name))
                body["items"].append(item)
            return Response(json.dumps(body), 200, mimetype=MASON)

    def post(self):
        try:
            record = json.loads(request.data)
            material = Material.objects(
                structure_name=record['material']).first()
        except KeyError:
            return create_error_response(
                400, "KeyError",
                "wrong format")
        try:
            if 'size c' in record:
                material_volume = Material_Volume(
                    size_a=record['size a'],
                    size_b=record['size b'],
                    size_c=record['size c'],
                    dimension_type=record['dimension type'],
                    bonding_length=record['bonding length'],
                    material=material.id
                )
            else:
                material_volume = Material_Volume(
                    size_a=record['size a'],
                    size_b=record['size b'],
                    dimension_type=record['dimension type'],
                    bonding_length=record['bonding length'],
                    material=material.id
                )
            material_volume.save()
            loc = api.url_for(MaterialVolumeEntry, id=material_volume.pk)
            return Response(status=201, headers={"Location": loc})
        except ValidationError:
            return create_error_response(
                400, "ValidationError",
                "Wrong attribute types")


class MaterialVolumeEntry(Resource):

    def get(self, id):
        try:
            material_volume = Material_Volume.objects(id=id).first()
        except ValidationError:
            return create_error_response(
                403, "ValidationError",
                "Not a valid objectId")

        if not material_volume:
            return create_error_response(
                403, "Material Volume is missing",
                "There is no material volume with the given id")
        else:
            body = MaterialVolumeBuilder(
                size_a=material_volume.size_a,
                size_b=material_volume.size_b,
                size_c=material_volume.size_c,
                bonding_length=material_volume.bonding_length,
                dimension_type=material_volume.dimension_type,
                material=material_volume.material.structure_name
            )
            body.add_namespace(MATERIAL_DB, LINK_RELATIONS_URL)
            body.add_control(SELF, api.url_for(MaterialVolumeEntry, id=id))
            body.add_control(PROFILE, MATERIAL_VOLUME_PROFILE)
            body.add_control(COLLECTION, api.url_for(MaterialVolumeCollection))
            body.add_control_edit_material_volume(id)
            body.add_control_delete_material_volume(id)
            return Response(json.dumps(body), 200, mimetype=MASON)

    def put(self, id):
        try:
            record = json.loads(request.data)
            material_volume = Material_Volume.objects(id=id).first()
            material = Material.objects(
                structure_name=record['material']).first()
        except KeyError:
            return create_error_response(
                400, "KeyError",
                "Wrong format")

        if not material_volume:
            return create_error_response(
                403, "Material Volume is missing",
                "There is no material volume with the given id")
        try:
            if 'size c' in record:
                Material_Volume.objects(id=id).update(set__size_a=record['size a'], set__size_b=record['size b'],
                                                      set__size_c=record['size c'], set__dimension_type=record['dimension type'], set__bonding_length=record['bonding length'], set__material=material.id)
            else:
                Material_Volume.objects(id=id).update(set__size_a=record['size a'], set__size_b=record['size b'],
                                                      set__dimension_type=record['dimension type'], set__bonding_length=record['bonding length'], set__material=material.id)
            return Response(status=204)
        except ValidationError:
            return create_error_response(
                400, "ValidationError",
                "Wrong attribute types")

    def delete(self, id):
        material_volume = Material_Volume.objects(id=id).first()
        if not material_volume:
            return create_error_response(
                403, "Material Volume is missing",
                "There is no material volume with the given id")
        else:
            Material_Volume.objects(id=str(material_volume.id)).delete()
            return Response(status=201)


class MaterialFermiCollection(Resource):
    def get(self):
        material_fermi = Material_Fermi.objects().all()
        if not material_fermi:
            return create_error_response(
                403, "Material Fermi is missing",
                "There is no material fermi with the given id")
        else:
            body = MaterialFermiBuilder()
            body.add_namespace(MATERIAL_DB, LINK_RELATIONS_URL)
            body.add_control(SELF, api.url_for(MaterialFermiCollection))
            body.add_control_all_material_fermi()
            body.add_control_add_material_fermi()
            body["items"] = []
            for each in material_fermi:
                item = MaterialFermiBuilder(
                    fermi=each.fermi,
                    material=each.material.structure_name,
                    volume=str(each.volume.id))
                item.add_control(SELF, api.url_for(
                    MaterialFermiEntry, id=each.id))
                item.add_control(PROFILE, MATERIAL_FERMI_PROFILE)
                item.add_control(REF_MATERIAL, api.url_for(
                    MaterialEntry, handle=each.material.structure_name))
                item.add_control(REF_VOLUME, api.url_for(
                    MaterialVolumeEntry, id=str(each.volume.id)))
                body["items"].append(item)
            return Response(json.dumps(body), 200, mimetype=MASON)

    def post(self):
        try:
            record = json.loads(request.data)
            material = Material.objects(
                structure_name=record['material']).first()
            volume = Material_Volume.objects(id=record['volume']).first()
        except KeyError:
            return create_error_response(
                400, "KeyError",
                "Wrong format")

        try:
            if material is not None and volume is not None:
                material_fermi = Material_Fermi(
                    fermi=record['fermi'],
                    material=material.id,
                    volume=volume.id
                )
                material_fermi.save()
                loc = api.url_for(MaterialFermiEntry, id=material_fermi.pk)
                return Response(status=201, headers={"Location": loc})
            return create_error_response(
                409, "Values missing",
                "Missing values")
        except ValidationError:
            return create_error_response(
                400, "KeyError",
                "Wrong attribute types")


class MaterialFermiEntry(Resource):

    def get(self, id):
        try:
            material_fermi = Material_Fermi.objects(id=id).first()
        except ValidationError:
            return create_error_response(
                403, "ValidationError",
                "Not a valid objectId")
        if not material_fermi:
            return create_error_response(
                403, "Material Fermi is missing",
                "There is no material fermi with the given id")
        else:
            body = MaterialFermiBuilder(id=str(material_fermi.id),
                                        fermi=material_fermi.fermi,
                                        material=material_fermi.material.structure_name,
                                        volume=str(material_fermi.volume.id))
            body.add_namespace(MATERIAL_DB, LINK_RELATIONS_URL)
            body.add_control(SELF, api.url_for(MaterialFermiEntry, id=id))
            body.add_control(PROFILE, MATERIAL_FERMI_PROFILE)
            body.add_control(COLLECTION, api.url_for(MaterialFermiCollection))
            body.add_control_edit_material_fermi(id)
            body.add_control_delete_material_fermi(id)
            return Response(json.dumps(body), 200, mimetype=MASON)

    def put(self, id):
        try:
            record = json.loads(request.data)
            material_fermi = Material_Fermi.objects(id=id).first()
            material_volume = Material_Volume.objects(
                id=record['volume id']).first()
            material = Material.objects(
                structure_name=record['material']).first()
        except KeyError:
            return create_error_response(
                400, "KeyError",
                "Wrong format")

        try:
            if not material_fermi:
                return create_error_response(
                    403, "Material Fermi is missing",
                    "There is no material fermi with the given id")
            else:
                Material_Fermi.objects(id=id).update(
                    set__fermi=record['fermi'], set__material=material.id, set__volume=material_volume.id)
                return Response(status=204)
        except ValidationError:
            return create_error_response(
                400, "KeyError",
                "Wrong attribute types")

    def delete(self, id):
        material_fermi = Material_Fermi.objects(id=id).first()
        if not material_fermi:
            return create_error_response(
                403, "Material Fermi is missing",
                "There is no material fermi with the given id")
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


class MaterialBuilder(MasonBuilder):
    @staticmethod
    def material_schema():
        schema = {
            "type": "object",
            "required": ["structure_name"]
        }
        props = schema["properties"] = {}
        props["structure_name"] = {
            "description": "Material's structure name",
            "type": "string"
        }
        return schema

    def add_control_all_material(self):
        self.add_control(
            MATERIAL_DB + ":material-all",
            href="/api/material/",
            method="GET",
            title="Get all material objects"
        )

    def add_control_delete_material(self, handle):
        self.add_control(
            MATERIAL_DB + ":delete",
            href="/api/material/" + handle + "/",
            method="DELETE",
            title="Delete this resource"
        )

    def add_control_add_material(self):
        self.add_control(
            MATERIAL_DB + ":add-material",
            href="/api/material/",
            method="POST",
            encoding="json",
            title="Add a new material",
            schema=self.material_schema()

        )

    def add_control_edit_material(self, handle):
        self.add_control(
            "edit",
            href="/api/material/" + handle + "/",
            method="PUT",
            encoding="json",
            schema=self.material_schema()
        )


class MaterialVolumeBuilder(MasonBuilder):
    @staticmethod
    def material_volume_schema():
        schema = {
            "type": "object",
            "required": ["size_a", "size_b", "bonding_length", "dimension_type", "material"]
        }
        props = schema["properties"] = {}
        props["size_a"] = {
            "description": "Material's first size measurement",
            "type": "number"
        }
        props["size_b"] = {
            "description": "Material's second size measurement",
            "type": "number"
        }
        props["size_c"] = {
            "description": "Material's third size measurement",
            "type": "number"
        }
        props["bonding_length"] = {
            "description": "Material's bonding length",
            "type": "number"
        }
        props["dimension_type"] = {
            "description": "Material's dimension",
            "type": "string"
        }
        props["material"] = {
            "description": "Material for reference",
            "type": "string"
        }
        return schema

    def add_control_all_material_volume(self):
        self.add_control(
            MATERIAL_DB + ":material_volume-all",
            href="/api/material_volume/",
            method="GET",
            title="Get all material volume objects"
        )

    def add_control_delete_material_volume(self, id):
        self.add_control(
            MATERIAL_DB + ":delete_material_volume",
            href="/api/material_volume/" + id + "/",
            method="DELETE",
            title="Delete this resource"
        )

    def add_control_add_material_volume(self):
        self.add_control(
            MATERIAL_DB + ":add_material_volume",
            href="/api/material_volume/",
            method="POST",
            encoding="json",
            title="Add a new material volume entry",
            schema=self.material_volume_schema()

        )

    def add_control_edit_material_volume(self, id):
        self.add_control(
            "edit",
            href="/api/material_volume/" + id + "/",
            method="PUT",
            encoding="json",
            schema=self.material_volume_schema()
        )


class MaterialFermiBuilder(MasonBuilder):
    @staticmethod
    def material_fermi_schema():
        schema = {
            "type": "object",
            "required": ["fermi", "material", "volume"]
        }
        props = schema["properties"] = {}
        props["fermi"] = {
            "description": "Material'sfermi energy",
            "type": "number"
        }
        props["volume"] = {
            "description": "Volume for reference",
            "type": "string"
        }
        props["material"] = {
            "description": "Material for reference",
            "type": "string"
        }
        return schema

    def add_control_all_material_fermi(self):
        self.add_control(
            MATERIAL_DB + ":material_fermi-all",
            href="/api/material_fermi/",
            method="GET",
            title="Get all material fermi objects"
        )

    def add_control_delete_material_fermi(self, id):
        self.add_control(
            MATERIAL_DB + ":delete",
            href="/api/material_fermi/" + id + "/",
            method="DELETE",
            title="Delete this resource"
        )

    def add_control_add_material_fermi(self):
        self.add_control(
            MATERIAL_DB + ":add-material_fermi",
            href="/api/material_fermi/",
            method="POST",
            encoding="json",
            title="Add a new material fermi entry",
            schema=self.material_fermi_schema()

        )

    def add_control_edit_material_fermi(self, id):
        self.add_control(
            "edit",
            href="/api/material_fermi/" + id + "/",
            method="PUT",
            encoding="json",
            schema=self.material_fermi_schema()
        )


if __name__ == '__main__':
    app.run(debug=True)
