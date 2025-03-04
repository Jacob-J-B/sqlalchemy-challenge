# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
import flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)
# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create a session
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
# Home Route
@app.route("/")
def home():
    return(
        "Home Page<br>"
        "Available routes:<br>"
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/start<br>"
        "/api/v1.0/start/end<br>"
        )
# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()
    session.close()
    results = {date:prcp for date,prcp in precip_scores}
    return(
        jsonify(results)
    )

# Stations
@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.station).all()
    session.close()
    stations = list(np.ravel(station_list))
    return(
        jsonify(stations)
    )

# tobs
@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    station_results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter\
    (Measurement.date >= last_year).all()
    session.close()
    active_station = list(np.ravel(station_results))
    return(
        jsonify(active_station)
    )

# start and start end
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start=None, end=None):
    temp_data = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    if not end:
        start = dt.datetime.strptime(start,"%m%d%Y")
        results = session.query(*temp_data).filter(Measurement.date >= start).all()
        session.close()
        temps = list(np.ravel(results))
        return(
            jsonify(temps)
        )
    start = dt.datetime.strptime(start,"%m%d%Y")
    end = dt.datetime.strptime(end,"%m%d%Y")
    results = session.query(*temp_data).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    temps = list(np.ravel(results))
    return(
        jsonify(temps)
    )

# run flask app
if __name__ == '__main__':
    app.run()