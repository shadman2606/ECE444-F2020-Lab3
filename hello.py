from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Email


app = Flask(__name__)
app.config['SECRET_KEY']='lightbulb blue jump'
boostrap = Bootstrap(app)
moment = Moment(app)


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your email?', validators=[Required(),Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # check for new name and email
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        # check for UofT email
        if 'utoronto' in form.email.data:
            session['non_uoft_email'] = False
        else:
           session['non_uoft_email'] = True
        session['email'] = form.email.data

        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'), 
            email=session.get('email'), non_uoft_email=session.get('non_uoft_email'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
