from flask import Flask
from flask_restful import Api, Resource
from CourseInfo import getCourse

app = Flask(__name__)
api = Api(app)

class CourseInfo (Resource):
    def get(self, courseCode):
        return getCourse(courseCode)
    
api.add_resource(CourseInfo, "/getCourse/<string:courseCode>")

if __name__ == "__main__":
    app.run(debug=True, port=5000)