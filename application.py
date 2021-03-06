#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash, url_for, request
# from flask.ext.sqlalchemy import SQLAlchemy
import csv, os, os.path
from collections import OrderedDict
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
    tiles='OpenStreetMap',
    zoom_start=13,
   )

gj='./FullStationAreaSet_Centroids.geojson'
with open(gj) as f:
    data = json.load(f)

for feature in data['features']:
    latlng=[feature['geometry']['coordinates'][1],feature['geometry']['coordinates'][0]]
    url="/comment/%s" %(feature['properties']['Station_ID'])
    name = feature['properties']['Name']
    stop_name = name.replace("/", "_")
    maxWidth='555px'
    popup='<html><body><iframe src="%s/%s" style="width:555px;height:250px"></iframe></body></html>' %(url,stop_name)
    # print latlng, popup

    stamenmap.simple_marker(location=latlng,
            popup=popup,
            )
# print feature
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

def writedata(myfile='static/centroids.csv',newrow={}):
    ordered_fieldnames = OrderedDict([
        ('ip',None),
        ('stop_id',None),
        ('timestamp',None),
        ('stop_name',None),
        ('freeway_ramps',None),
        ('sidewalk_poor',None),
        ('poor_crosswalks',None),
        ('not_safe',None),
        ('vehicle_speed',None),
        ('poor_lighting',None),
        ('poor_signage',None),
        ('no_enforcement',None),
        ('no_shade',None),
        ('personal_safety',None),
        ('too_far',None),
        ('bad_drivers',None),
        ('no_facilities',None),
        ('other',None),
        ])
    if not os.path.isfile(myfile):
        with open(myfile,'wb') as fou:
            dw = csv.DictWriter(fou, delimiter=',', fieldnames=ordered_fieldnames)
            dw.writeheader()
            dw.writerow(newrow)
    else:
        with open(myfile,'ab') as fou:
            dw = csv.DictWriter(fou, delimiter=',', fieldnames=ordered_fieldnames)
            dw.writerow(newrow)

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

@application.route('/comment/<stop_id>/<stop_name>', methods=('GET', 'POST'))
def comment(stop_id=0,stop_name='hihi'):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    restored = stop_name.replace("_", "/")
    form = CommentForm(stop_id=stop_id, stop_name=restored, ip=request.remote_addr, timestamp=st)
    form.stop_id=stop_id
    flashmsg = "%s" %(restored)
    if form.validate_on_submit():
        # flash(form.data)
        writedata(myfile='static/centroids.csv',newrow=form.data)
        flash(flashmsg)
        # print form.data
    # else:
        # flash(form.errors)
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
    run_simple('127.0.0.1', 5000, application, use_debugger=True, use_reloader=True)
