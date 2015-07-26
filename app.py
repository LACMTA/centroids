#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash
# from flask.ext.sqlalchemy import SQLAlchemy
import csv, os
import logging
from logging import Formatter, FileHandler
from forms import *
import simplejson as json
import folium

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
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
    popup='<html><body><iframe src="%s"></iframe></body></html>' %(url)
    print latlng, popup

    stamenmap.simple_marker(location=latlng, 
            popup=popup,
            )
print feature
stamenmap.create_map(path='templates/pages/stamen_toner.html')



# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
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

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/map')
def map():
    return render_template('pages/stamen_toner.html')

@app.route('/comment/<stop_id>', methods=('GET', 'POST'))
def comment(stop_id):
    form = CommentForm(stop_id=stop_id, stop_name='hi')
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

@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    # app.run()
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
