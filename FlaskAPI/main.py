from flask import Flask, jsonify
from flask_restful import Api, Resource
from CourseInfo import getCourse, getCourses
from Schedule import getSchedule

app = Flask(__name__)
api = Api(app)

class CourseInfo (Resource):
    def get(self, courseCodes, trimesterCode):
        return jsonify(getCourses(courseCodes, trimesterCode))

class Schedule (Resource):
    def get(self, courseCodes, trimesterCode):
        return jsonify(getSchedule(courseCodes, trimesterCode))
        
api.add_resource(CourseInfo, "/getCourses/<string:courseCodes>-<string:trimesterCode>")
api.add_resource(Schedule, "/getSchedule/<string:courseCodes>-<string:trimesterCode>")


if __name__ == "__main__":
    app.run(debug=True, port=5000)