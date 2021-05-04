from flask import Flask, render_template, request, redirect, jsonify
# url_for
# from req
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
db = SQLAlchemy(app)

class Course(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    start_date =db.Column(db.Date)
    end_date =db.Column(db.Date)
    hours=db.Column(db.Integer)

    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} {self.hours} hours - {self.description} {self.start_date} {self.end_date}"


@app.route('/course/<int:id>', methods=['GET'])
def show_course(id):
    course = Course.query.get_or_404(id)

    result = []
    return jsonify(
        id = course.id,
        name = course.name,
        start_date = course.start_date,
        end_date = course.end_date,
        hours = course.hours,

        description = course.description
    )
    
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        new_name = request.form['name']
        new_description = request.form['description']
        new_start = datetime.strptime((request.form['start']), '%Y-%m-%d')
        new_end =  datetime.strptime((request.form['end']), '%Y-%m-%d')
        new_hours = request.form['hours']
        
        new_course = Course(name = new_name,
                            hours = new_hours,
                            description = new_description,
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


@app.route('/delete/<int:id>')
def delete_course(id):
    course_to_delete = Course.query.get_or_404(id)

    try:
        db.session.delete(course_to_delete)
        db.session.commit()

        return redirect('/')
    except:
        return 'Ttere was a problem deleting the course'


@app.route('/edit/<int:id>', methods = ['POST','GET'])
def edit_course(id):
    course_to_edit = Course.query.get_or_404(id)

    if request.method == 'POST':
        course_to_edit.name = request.form['name']
        course_to_edit.description = request.form['description']
        course_to_edit.start = datetime.strptime((request.form['start']), '%Y-%m-%d')
        course_to_edit.end =  datetime.strptime((request.form['end']), '%Y-%m-%d')
        course_to_edit.hours = request.form['hours']
        
        # new_course = Course(name = new_name,
        #                     hours = new_hours,
        #                     description = new_description,
        #                     start_date = new_start,
        #                     end_date = new_end)
        try:
            
            db.session.commit()

            return redirect('/')
        except:

            return f'There was an issue update your course {new_course}'
    else:
        return render_template('edit.html', course = course_to_edit)



if __name__ =="__main__":
    app.run(debug=True)