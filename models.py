from peewee import *

#  db = SqliteDatabase('data/dataBase/user_data.db')
db = SqliteDatabase('data/dataBase/user_data1.db')


class BaseModel(Model):
    class Meta:
        database = db


class Role(BaseModel):
    role = CharField(max_length=20)


class User(BaseModel):
    class Meta:
        db_table = 'Users'

    is_active = BooleanField()
    user_id = IntegerField()
    name = CharField(max_length=40)
    last_name = CharField(max_length=40)
    phone = CharField(max_length=40)
    date_registration = DateField()
    photo = CharField(max_length=200, null=True)


class Manager(User):
    score_client = FloatField(null=True)


class Client(User):
    organization = CharField(max_length=100)
    person_manager = ForeignKeyField(Manager)
    post = CharField(max_length=100)


class Mixer(BaseModel):
    is_active = BooleanField()
    date_registration = DateField()
    organization = CharField(max_length=100)
    car_brand = CharField(max_length=40)
    car_number = CharField(max_length=100)
    max_volume = FloatField()
    photo = CharField(max_length=200, null=True)


class Dispatcher(User):
    photo = CharField(max_length=200, null=True)
    score_client = FloatField(null=True)
    max_shipment = FloatField(null=True)
    average_shipment = FloatField(null=True)


class TheObject(BaseModel):
    is_active = BooleanField()
    date_registration = DateField()
    customer = ForeignKeyField(Client)
    obj_name = TextField()
    location = CharField(max_length=200, null=True)
    average_speed_of_unloading_by_crane = FloatField(null=True)
    average_speed_of_unloading_by_pump = FloatField(null=True)
    average_speed_of_unloading_by_self_watering = FloatField(null=True)
    condition_of_access_roads = FloatField(null=True)
    total_number = FloatField(null=True)


class Product(BaseModel):
    is_active = BooleanField()
    abbreviation = CharField(max_length=100, null=True)
    product_type = CharField(max_length=40)
    product_class = FloatField(null=True)
    frost_resistance = IntegerField(null=True)
    water_permeability = IntegerField(null=True)
    placeholder = CharField(max_length=10, null=True)
    placeholder_fraction = CharField(max_length=10, null=True)
    mobility = IntegerField(null=True)
    cone_sediment = CharField(max_length=10, null=True)
    used_in = ForeignKeyField(TheObject)
    mark_cement_mortal = IntegerField(null=True)
    type_cement_mortal = CharField(max_length=50, null=True)
    date_registration = DateField()


class Application(BaseModel):
    is_delete = BooleanField()
    is_active = BooleanField()
    is_executed = BooleanField()
    is_confirmation = DateTimeField()
    the_object = ForeignKeyField(TheObject)
    creator = ForeignKeyField(Client)
    manager = ForeignKeyField(Manager)
    dispatcher = ForeignKeyField(Dispatcher, null=True)
    creation_time = DateTimeField()
    visa_time = DateTimeField(null=True)
    execution_time = DateTimeField(null=True)
    product = ForeignKeyField(Product)
    volume_declared = FloatField()
    unloading_method = CharField(max_length=20, null=True)
    declared_unloading_speed = FloatField(null=True)
    pump_sleeve_length = FloatField(null=True)
    pump_feed_time = DateTimeField(null=True)
    volume_total = FloatField(null=True)
    volume_remains = FloatField(null=True)


class Driver(User):
    is_work = BooleanField()
    organization = CharField(max_length=100)
    mixer = ForeignKeyField(Mixer, null=True)
    score_client = FloatField(null=True)
    score_dispatcher = FloatField(null=True)
    working_by_application = ForeignKeyField(Application, null=True)


if __name__ == '__main__':
    db.create_tables([Client, Manager, Driver, Dispatcher, Role, TheObject, Mixer, Application, Product])



