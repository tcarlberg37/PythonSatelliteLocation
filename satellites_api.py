from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify

db_connect = create_engine("sqlite:///satellites.db")
app = Flask(__name__)
api = Api(app)

class Satellites(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from satellites;")
        result = {"data": [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class Satellite_Timestamp(Resource):
    def get(self, timestamp):
        conn = db_connect.connect()
        query = conn.execute("select * from satellites where timestamp =%d " % int(timestamp))
        result = {"data": [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Satellites, "/satellites")
api.add_resource(Satellite_Timestamp, "/satellites/<timestamp>")

if __name__ == "__main__":
    app.run(port="5002")