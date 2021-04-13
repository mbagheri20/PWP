from flask import Flask
from flask_mongoengine import MongoEngine
from app import Material, Material_Fermi, Material_Volume

populate_db = Flask(__name__)
populate_db.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'mongodb://localhost/db',
    'port': 27017
}
db = MongoEngine(populate_db)


class Migration(db.Document):  # class for migration
    migration = db.StringField(required=True, unique=True, max_length=64)
    successful = db.BooleanField(required=True)


def initialize():
    migrations = []
    material_migration = ("Material", update_values(material(), "Material"))
    migrations.append(material_migration)
    volume_migration = ("Material_Volume", update_values(
        volume(), "Material_Volume"))
    migrations.append(volume_migration)
    fermi_migration = ("Material_Fermi", update_values(
        fermi(), "Material_Fermi"))
    migrations.append(fermi_migration)
    for each in migrations:
        if each:
            mig = Migration(migration=each[0], successful=each[1])
            mig.save()
            print("migration updated")
        else:
            mig = Migration(migration=each[0], successful=each[1])
            mig.save()
            print("something went wront :(")
    return


def update_values(dictlist: list, type: any) -> bool:
    classTypeEnum
    if type not in classTypeEnum.keys():
        print("error")
        return False
    try:
        for each in dictlist:
            thign = classTypeEnum[type](**each)
            thign.save()
            print(str(classTypeEnum[type]) + " saved")
        return True
    except ValueError:
        print("error occured")
        return False


def material() -> list:
    """return list of dicts
    [{material1}, {material2}]
    """
    material_list = [
        {"structure_name": "a"},
        {"structure_name": "b"},
        {"structure_name": "c"}
    ]
    return material_list


def volume() -> list:
    """return list of dicts
    [{volume1}, {volume2}, {volume3}]
    """
    materials = Material.objects().all()
    volume_list = [
        {
            "size_a": 1.1,
            "size_b": 1.11,
            "size_c": 1.111,
            "bonding_length": 1,
            "dimension_type": "3d",
            "material": materials[0].id
        },
        {
            "size_a": 1.2,
            "size_b": 1.22,
            "size_c": 1.222,
            "bonding_length": 2,
            "dimension_type": "3d",
            "material": materials[1].id
        },
        {
            "size_a": 1.3,
            "size_b": 1.33,
            "bonding_length": 3,
            "dimension_type": "2d",
            "material": materials[2].id
        },
    ]
    return volume_list


def fermi() -> list:
    """return list of dicts
    [{fermi}, {fermi}, {fermi}]
    """
    fermi_list = []
    volumes = Material_Volume.objects().all()
    for each_volume in volumes:
        fermi = {"volume": each_volume.id,
                 "material": each_volume.material.id,
                 "fermi": 0.42
                 }
        fermi_list.append(fermi)
    return fermi_list


def found_migrations() -> bool:
    migration = Migration.objects().first()
    if migration is None:
        return False
    return True


classTypeEnum = {
    "Material": Material,
    "Material_Volume": Material_Volume,
    "Material_Fermi": Material_Fermi
}

if __name__ == '__main__':
    if not found_migrations():
       initialize()
       print("Database Initialized, Migrations added")
    else:
        print("Migrations Found")
        # db.drop_database('db')
        # print(db)
        # # initialize()
        # print("Database Reset, Migrations added")
    exit()
