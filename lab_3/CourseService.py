from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Course:
    course_name: str
    course_desc: str
    course_topics: list[str]

@dataclass
class CourseService:
    name: str
    description: str
    courses: Dict = field(default_factory=dict)

    def __post_init__(self):
        self.courses['1'] = Course(
            course_name='course_name_1',
            course_desc='course_desc_1',
            course_topics=['course_theme_11', 'course_theme_12', 'course_theme_13']
        )
        self.courses['2'] = Course(
            course_name='course_name_2',
            course_desc='course_desc_2',
            course_topics=['course_theme_21', 'course_theme_22', 'course_theme_23']
        )
        self.courses['3'] = Course(
            course_name='course_name_3',
            course_desc='course_desc_3',
            course_topics=['course_theme_31', 'course_theme_32', 'course_theme_33']
        )

    def get_courses(self):
        return self.courses
    
    def get_course(self, course_id):
        return self.courses[course_id]
    
    def add_course(self, course_name, course_desc, course_topics):
        course_id = str(len(self.courses) + 1)
        self.courses[course_id] = Course(
            course_name=course_name,
            course_desc=course_desc,
            course_topics=course_topics
        )
        return 'Course has been added'
    
    def update_course(self, course_id, new_name, new_desc, new_topics):
        self.courses[course_id] = Course(
            course_name=new_name,
            course_desc=new_desc,
            course_topics=new_topics
        )
        return 'Course has beed updated'
    
    def delete_course(self, course_id):
        del self.courses[course_id]
        return f'Course id:{course_id} has been deleted'