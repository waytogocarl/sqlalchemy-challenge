# import flask - connect python to the web
import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# set-up the database
engine = create_engine("sqlite:////Users/carleighwest/Desktop/sqlalchemy-challenge/Resources/hawaii.sqlite")

# use automap
Base = automap_base()
Base.prepare(autoload_with=engine)

# save the references for each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create the session
session = Session(engine)

# create an app with flask
app = Flask(__name__)

# define what you do when a user hits the index route, list all available routes
@app.route("/") # the / is an endpoint
def home():
    return (
        f"Surf's Up! Are You Ready for Your Hawaii Vacation?<br/>" # <br/> makes a break and sends the text to the next line
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' should be in the format MMDDYYY.<p/>"

    )

# convert results from the precipitation analysis, retrieve only the last 12 months of data
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year."""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# query for the date and the prcp
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

    session.close()

# create a dictionary with date as the key and prcp as the value
    precip  = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)



@app.route("/api/v1.0/stations")
def stations ():
    """Return a list of the stations."""
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results)) # np.ravel consolidates when there are lists within lists
    return jsonify(stations=stations)



@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for the previous year"""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Query the dates and temperature observations of the most-active station for the previous year of data.
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()

    session.close()

    temps= list(np.ravel(results))
    return(jsonify(temps=temps))


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).filter(Measurement.date >= start).all()

        session.close()

        temps = list(np.ravel(results))
        return jsonify(temps)
    
    #calculate TMIN, TAVG, TMAX with start and stop

    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

# if both start and end are provided, the code converts it to a datetime format, it then queries the database for temps between the specified dates
    results = session.query(*sel).filter(Measurement.date >= start). filter(Measurement.date <= end).all()

    session.close()

# convert the results to a list and return them as a json response
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run()
