from flask import Flask, render_template
from flask_migrate import Migrate
from flask_restful import Api
from db import db
from flask_cors import CORS

from resources.account import Account, AccountList
from resources.bike import Bike, BikeList
from resources.login import Login
from resources.booking import Booking, BookingList

from decouple import config as config_decouple
from config import config


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# app.config['GOOGLEMAPS_KEY'] = "AIzaSyD_8CnauFmnvQZ1zuOhY4SGIdwc3MoBbO4"
# GoogleMaps(app, key="AIzaSyD_8CnauFmnvQZ1zuOhY4SGIdwc3MoBbO4")

environment = config['development']
if config_decouple('PRODUCTION', cast=bool, default=False):
    environment = config['production']

app.config.from_object(environment)

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)


# app.app_context().push()


@app.route('/')
@app.route('/home')
def render_vue():
    return render_template("index.html")


api.add_resource(Account, '/account/<string:username>', '/account/<int:id>', '/account')
api.add_resource(AccountList, '/accounts')

api.add_resource(BikeList, '/bikes')
api.add_resource(Bike, '/bike', '/bike/<int:id>')

api.add_resource(Login, '/login')

api.add_resource(Booking, '/rent', '/rent/<int:userid>')
api.add_resource(BookingList, '/rents')

# api.add_resource(Map, '/map')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
