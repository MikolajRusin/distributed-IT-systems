from flask import Flask, jsonify, request
from CourseService import CourseService

app = Flask(__name__)

service = CourseService(name='Course Server', description='Service including courses')

@app.route('/welcome')
def welcome_page():
    return f'Welcome to the {service.name} ({service.description})'

@app.route('/courses', methods=['GET'])
def get_courses():
    courses_list = service.get_courses()
    return jsonify(courses_list)

@app.route('/courses/<string:course_id>', methods=['GET'])
def get_course(course_id):
    course = service.get_course(course_id)
    return jsonify(course)

@app.route('/add', methods=['POST'])
def add_course():
    course_data = request.get_json()
    course_name = course_data.get('course_name')
    course_desc = course_data.get('course_desc')
    course_topics = course_data.get('course_topics')
    status = service.add_course(course_name=course_name, course_desc=course_desc, course_topics=course_topics)
    return status

@app.route('/update/<string:course_id>', methods=['PUT'])
def update_course(course_id):
    new_data = request.get_json()
    new_name = new_data.get('new_name')
    new_desc = new_data.get('new_desc')
    new_topics = new_data.get('new_topics')
    status = service.update_course(course_id, new_name, new_desc, new_topics)
    return status

@app.route('/delete/<string:course_id>', methods=['DELETE'])
def delete_course(course_id):
    status = service.delete_course(course_id)
    return status

if __name__ == '__main__':
    app.run()