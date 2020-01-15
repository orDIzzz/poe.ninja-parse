from peewee import *
import configparser
config = configparser.ConfigParser()
config.read("settings.ini")
section = "DBCon"
host = config.get(section, "host")
user = config.get(section, "user")
password = config.get(section, "password")
db_name = config.get(section, "database")

dbhandle = PostgresqlDatabase(
    db_name,
    user=user,
    password=password,
    host=host
)


class BaseModel(Model):
    class Meta:
        database = dbhandle


class Items(BaseModel):
    id = PrimaryKeyField(null=False)
    item_id = IntegerField(unique=True, null=False)
    name = CharField(max_length=100)
    category = CharField(max_length=30)
    type = CharField(max_length=30)
    current = FloatField()
    current_hc = FloatField()
    standard = FloatField()
    standard_hc = FloatField()
    class Meta:
        db_table = "items"
        order_by = ('curr',)

if __name__ == '__main__':
    Items.create_table()