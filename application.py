#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash
# from flask.ext.sqlalchemy import SQLAlchemy
import csv, os
from werkzeug.serving import run_simple
import logging
from logging import Formatter, FileHandler
from forms import *
import simplejson as json
import folium

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

application = Flask(__name__)
application.config.from_object('config')
#db = SQLAlchemy(app)
stamenmap = folium.Map(location=[34.0552, -118.2352], 
    tiles='Stamen Toner',
    zoom_start=13,
    width='1000', height='600',
   )

gj='./FullStationAreaSet_Centroids.geojson'
with open(gj) as f:
    data = json.load(f)

for feature in data['features']:
    latlng=[feature['geometry']['coordinates'][1],feature['geometry']['coordinates'][0]]
    url="/comment/%s" %(feature['properties']['Station_ID'])
    stop_name=feature['properties']['Name']
    maxWidth='500px'
    popup='<html><body><iframe src="%s?%s"></iframe></body></html>' %(url,stop_name)
    print latlng, popup

    stamenmap.simple_marker(location=latlng, 
            popup=popup,
            )
print feature
stamenmap.create_map(path='templates/pages/stamen_toner.html')



# Automatically tear down SQLAlchemy.
'''
@application.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

def writedata(myfile='centroids.csv',newrow={}):
    with open(myfile, 'ab') as csvfile:
        fieldnames = ['stop_id', 'no_shade', 'freeway_ramps', 'poor_signage', 'sidewalk_poor', 'no_crosswalks','timestamp','ip']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()
        writer.writerow(newrow)

@application.route('/')
def home():
    return render_template('pages/stamen_toner.html')
    # return render_template('pages/placeholder.home.html')


@application.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@application.route('/map')
def map():
    return render_template('pages/stamen_toner.html')

@application.route('/comment/<stop_id>?<path:stop_name>', methods=('GET', 'POST'))
def comment(stop_id=0,stop_name='hihi'):
    form = CommentForm(stop_id=stop_id, stop_name=stop_name)
    form.stop_id=stop_id
    if form.validate_on_submit():
        flash(form.data)
        writedata(myfile='centroids.csv',newrow=form.data)
        # print form.data
    else:
        flash(form.errors)
        # print form.errors

    return render_template(
        'forms/comment.html', 
        title='comment',
        form=form,
        )


@application.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@application.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@application.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@application.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@application.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not application.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    application.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    application.logger.addHandler(file_handler)
    application.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, application, use_reloader=True)


