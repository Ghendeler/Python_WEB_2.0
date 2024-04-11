import configparser

from mongoengine import connect

config = configparser.ConfigParser()
config.read('bs_parser\\mongo\\config.ini')
# config.read('.\\config.ini')
print(config.sections())

mongo_user = config.get('DB', 'USER')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string

connect(
    host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True
)
