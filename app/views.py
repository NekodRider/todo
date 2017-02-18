from flask import render_template, flash, redirect, request, session, url_for, jsonify
from app import app, data


@app.route('/list', methods=["POST", "GET"])
def list():
    user_id = session.get('id')
    todos = data.getPost(user_id)
    if request.method == "POST" and request.headers.has_key("X-Requested-With"):
        type = int(request.form.get("type", "null"))
        if (type == 0):
            todos = data.getPost(user_id)
            return jsonify(todos=todos)
        elif (type == 1):
            new_content = request.form.get("content", "null")
            data.Post(user_id, new_content)
            todos = data.getPost(user_id)
            return jsonify(todos=todos)
        elif (type == -1):
            id = int(request.form.get("id", "null"))
            data.delete_Post(id)
            todos = data.getPost(user_id)
            return jsonify(todos=todos)
        elif (type == 2):
            id = int(request.form.get("id", "null"))
            status = int(request.form.get("status", "null"))
            data.done_Post(id, status)
            todos = data.getPost(user_id)
            return jsonify(todos=todos)

    elif request.method == "POST":
        if (request.form.get("type") == 0):
            todos = data.getPost(user_id)
            return jsonify(todos=todos)
        elif (request.form.get("type") == 1):
            new_content = request.form.get("content", "null")
            data.Post(user_id, new_content)
            todos = data.getPost(user_id)
            return jsonify(todos=todos)
        elif (request.form.get("type") == -1):
            data.delete_Post(request.form.get("id"))
            todos = data.getPost(user_id)
            return jsonify(todos=todos)
        elif (request.form.get("type") == 2):
            data.done_Post(request.form.get("id"), request.form.get("status"))
            todos = data.getPost(user_id)
            return jsonify(todos=todos)
    else:
        if session.get('id'):
            user = {'id': session.get('id'),
                    'name': session.get('name')}
            return render_template("list.html",
                                   title='List',
                                   todos=todos,
                                   user=user)
        else:
            user = {'id': '', 'name': ''}
            return render_template("index.html",
                                   title='Home',
                                   user=user)


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if (request.args):
        id = request.args['id']
        pw = request.args['pw']
        if (data.login_Check(id, pw)):
            flash('Login Successful!')
            session['id'] = request.args['id']
            session['name'] = data.login_Check(id, pw)['name']
            if session.get('id'):
                user = {'id': session.get('id'),
                        'name': session.get('name')}
            else:
                user = {'id': '', 'name': ''}
            return render_template("index.html",
                                   title='Home',
                                   user=user)
        else:
            user = {'id': '', 'name': ''}
            flash('Login Failed!')
            return render_template('login.html',
                                   title='Sign In',
                                   user=user)
    else:
        if session.get('id'):
            user = {'id': session.get('id'),
                    'name': session.get('name')}
        else:
            user = {'id': '', 'name': ''}
        return render_template("index.html",
                               title='Home',
                               user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = {'id': '', 'name': ''}
    return render_template('login.html',
                           title='Sign In',
                           user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.args):
        id = request.args['id']
        name = request.args['name']
        pw = request.args['pw']
        if (data.Register(id, name, pw) == True):
            flash('Register Successful!')
            user = {'id': '', 'name': ''}
            return render_template("login.html",
                                   title='Sign In',
                                   user=user)
        else:
            user = {'id': '', 'name': ''}
            flash('Register Failed!' + str(data.Register(id, name, pw)))
            return render_template('register.html',
                                   title='Register',
                                   user=user)
    else:
        if session.get('id'):
            user = {'id': session.get('id'),
                    'name': session.get('name')}
        else:
            user = {'id': '', 'name': ''}
        return render_template('register.html',
                               title='Register',
                               user=user)


@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('index'))
