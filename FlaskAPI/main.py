from flask import Flask, jsonify
from flask_restful import Api, Resource
from CourseInfo import getCourse, getCourses

app = Flask(__name__)
api = Api(app)

class CourseInfo (Resource):
    def get(self, courseCode, trimesterCode):
        return jsonify(getCourse(courseCode, trimesterCode))

class CoursesInfo (Resource):
    def get(self, courseCodes, trimesterCode):
        return jsonify(getCourses(courseCodes, trimesterCode))
    
api.add_resource(CourseInfo, "/getCourse/<string:courseCode>-<string:trimesterCode>")
api.add_resource(CoursesInfo, "/getCourses/<string:courseCodes>-<string:trimesterCode>")


if __name__ == "__main__":
    app.run(debug=True, port=5000)