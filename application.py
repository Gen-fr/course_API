from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
db = SQLAlchemy(app)

class Course(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    start_date = db.Column(db.String, default = "00-00-00")
    end_date = db.Column(db.String)
    hours = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.name} {self.hours} hours -  {self.start_date} {self.end_date}"
    
    def change_var(self, key=str,val=str):
        if key == "name":
            self.name = val
        if key == "hours":
            self.hours = val
        if key == "start_date":  
            self.start_date = val
        if key == "end_date":  
            self.end_date = val
        

#Courses list get All courses
@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.order_by(Course.id).all() #TODO check with empty base 
    result = []
    for course in courses:
        course_data = {}
        course_data['id'] = course.id
        course_data['name'] = course.name
        course_data['start_date'] = course.start_date
        course_data['end_date'] = course.end_date
        course_data['hourse'] = course.hours
        result.append(course_data)
 
    return jsonify({'courses' : result})

# GET one course
@app.route('/courses/<int:id>', methods=['GET'])
def get_course(id):  
    course = Course.query.get_or_404(id)
    course_data = {}
    course_data['id'] = course.id
    course_data['name'] = course.name
    course_data['start_date'] = course.start_date
    course_data['end_date'] = course.end_date
    course_data['hours'] = course.hours
    return jsonify({'course' : course_data})
    
#ADD a new course
@app.route('/courses', methods=['POST']) 
def create_course():
    data = request.get_json()
    try:
        new_course = Course( name=data['name'], start_date=data['start_date'], 
                end_date=data['end_date'], hours=data['hours'])
        db.session.add(new_course)
        db.session.commit()
        return jsonify({'message' : 'New course added'})
    except: 
        return 'There was a problem adding the course'
    

# Edit a course
@app.route('/courses/<id>', methods=['PUT']) 
def edit_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json() 

    if data:
        for k,v in data.items():
            course.change_var(k,v)
            db.session.commit()
    else:
        return jsonify({"message":"No data in request"})

    return 'Edited'

#Removing
@app.route('/courses/<id>', methods = ['DELETE'])
def delete_course(id):
    course_to_delete = Course.query.get_or_404(id)
    try:
        db.session.delete(course_to_delete)
        db.session.commit()
        return jsonify({'message' : "The course has been deleted!"})
    except:
        return 'Ttere was a problem deleting the course'

#search and filtering
@app.route('/search', methods=['GET', 'POST'])
def search():
    quest = request.args.get('q', type=str)
    if not quest:
        return ({"Message":"Wrong search"})

    sort = Course.query.order_by(Course.start_date) 
    result = sort.filter(Course.name.like('%'+quest+'%')).all()

    res = []
    for course in result:
        course_data = {}
        course_data['id'] = course.id
        course_data['name'] = course.name
        course_data['start_date'] = course.start_date
        course_data['end_date'] = course.end_date
        course_data['hourse'] = course.hours
        res.append(course_data)
 
    return jsonify({'courses' : res})

#web interface
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        new_name = request.form['name']
        new_start = datetime.strptime((request.form['start']), '%Y-%m-%d')
        new_end =  datetime.strptime((request.form['end']), '%Y-%m-%d')
        new_hours = request.form['hours']
        
        new_course = Course(name = new_name,
                            hours = new_hours,
                            start_date = new_start,
                            end_date = new_end)
        try:
            db.session.add(new_course)
            db.session.commit()
            return redirect('/')
        except:
            return f'There was an issue adding your course {new_course}'

    else:
        # here is a form of display courses
        courses = Course.query.order_by(Course.id).all() 
        return render_template('index.html', courses = courses)

#human editor
@app.route('/edit/<int:id>', methods = ['POST','GET'])
def edit_course_h(id):
    course_to_edit = Course.query.get_or_404(id)

    if request.method == 'POST':
        course_to_edit.name = request.form['name']
        course_to_edit.start = datetime.strptime((request.form['start']), '%Y-%m-%d')
        course_to_edit.end =  datetime.strptime((request.form['end']), '%Y-%m-%d')
        course_to_edit.hours = request.form['hours']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return f'There was an issue update your course {new_course}'
    else:
        return render_template('edit.html', course = course_to_edit)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ =="__main__":
    app.run(debug=True)