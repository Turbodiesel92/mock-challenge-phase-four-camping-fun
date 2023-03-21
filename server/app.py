from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class Index(Resource):
    def get(self):
        response_dict = {
            "message": "Hello Campers!"
        }

        return make_response(jsonify(response_dict), 200)

api.add_resource(Index, '/')

class Campers(Resource):
    def get(self):
        camper_dicts = [camper.to_dict() for camper in Camper.query.all()]

        return make_response(
            jsonify(camper_dicts),
            200
        )

    def post(self):
        new_camper = Camper(
            name=request.get_json()['name'],
            age=request.get_json()['age'],
        )

        db.session.add(new_camper)
        db.session.commit()

        return make_response(
            jsonify(new_camper.to_dict()),
            201
        )

api.add_resource(Campers, '/campers')

class CamperById(Resource):
    def get(self, id):
        camper = Camper.query.filter_by(id=id).first()
        camper_dict = camper.to_dict(rules=('activities',))

        return make_response(
            jsonify(camper_dict),
            200
        )

api.add_resource(CamperById, '/campers/<int:id>')

class Activities(Resource):
    def get(self):
        activity_dicts = [activity.to_dict() for activity in Activity.query.all()]

        return make_response(
            jsonify(activity_dicts),
            200
        )

api.add_resource(Activities, '/activities')

class ActivityById(Resource):
    def delete(self, id):
        activity = Activity.query.filter(Activity.id == id).first()

        if not activity:
            return make_response(
                { "error": "Activity not found" },
                404
            )
        else:
            db.session.delete(activity)
            db.session.commit()

            return make_response("", 200)

api.add_resource(ActivityById, '/activities/<int:id>')

class Signups(Resource):
    def post(self):
        new_signup = Signup(
            time=request.get_json()['time'],
            camper_id=request.get_json()['camper_id'],
            activity_id=request.get_json()['activity_id']
        )

        db.session.add(new_signup)
        db.session.commit()

        return make_response(
            jsonify(new_signup.activity.to_dict()),
            201
        )

api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)