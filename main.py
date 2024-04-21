import datetime

from flask import Flask, request, abort
from flask import render_template, redirect

from flask_login import LoginManager, login_required, current_user
from flask_login import logout_user, login_user

from data import db_session

from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.category import Category

from forms.user import RegisterForm, LoginForm
from forms.job import JobsForm
from forms.department import DepartmentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def work_log():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("work_log.html", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/job',  methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.team_leader = current_user.id
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.end_date = datetime.datetime.now() + datetime.timedelta(hours=job.work_size)
        job.is_finished = form.is_finished.data
        category = db_sess.query(Category).filter(Category.id == form.category.data).first()
        if not category:
            category = Category(id=form.category.data)
        category = db_sess.merge(category)
        job.categories.append(category)
        user = db_sess.merge(current_user)
        user.jobs.append(job)
        db_sess.merge(user)
        db_sess.commit()

        return redirect('/')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         ((Jobs.user == current_user) | (current_user.id == 1))).first()
        if job:
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.category.data = job.categories[0].id
            form.is_finished.data = job.is_finished
            job.categories.remove(job.categories[0])
            db_sess.commit()
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         ((Jobs.user == current_user) | (current_user.id == 1))).first()
        if job:
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.end_date = job.start_date + datetime.timedelta(hours=job.work_size)
            job.is_finished = form.is_finished.data
            category = db_sess.query(Category).filter(Category.id == form.category.data).first()
            if not category:
                category = Category(id=form.category.data)
            category = db_sess.merge(category)
            job.categories.append(category)
            db_sess.merge(job)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id,
                                     ((Jobs.user == current_user) | (current_user.id == 1))).first()
    if job:
        job.categories.remove(job.categories[0])
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/department',  methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief = current_user.id
        department.members = form.members.data
        department.email = form.email.data
        current_user.department.append(department)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/department_log')
    return render_template('department.html', title='Добавление депортамента',
                           form=form)


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == id,
                                                      ((Department.user == current_user) | (
                                                                  current_user.id == 1))).first()
        if department:
            form.title.data = department.title
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == id,
                                                      ((Department.user == current_user) | (
                                                                  current_user.id == 1))).first()
        if department:
            department.title = form.title.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect('/department_log')
        else:
            abort(404)
    return render_template('department.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == id,
                                                  ((Department.user == current_user) | (current_user.id == 1))).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/department_log')


@app.route("/department_log")
def department_log():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template("department_log.html", departments=departments)


def main():
    db_session.global_init("db/mars.db")

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
