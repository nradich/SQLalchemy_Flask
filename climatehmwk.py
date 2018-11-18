#Nicholas Radich SQLalchemy/Flask homework
#import dependencies
import warnings
warnings.filterwarnings('ignore')
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
connection = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


#query for precipitation and date


@app.route("/")
def welcome():
    """List all posibble routes"""
    return(
    "Welcome to Week 10 Homework using SQLalchemy and Flask!</br>"
    "Available Routes:</br>"
    "/api/v1.0/precipitation</br>"
    "/api/v1.0/stations</br>"
   "/api/v1.0/tobs</br>"
   "/api/v1.0/<start></br>"
   "/api/v1.0/<start>/<end>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
#query for precipitation and date
    dateprcp = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= '2016-08-23')

#convert to list
    datelist = [i for i in dateprcp]

    return jsonify(datelist)


#need to revisit and join for station name 
@app.route("/api/v1.0/stations")
def stationlist():
    """Returns the number of stations, need to join to get the full name"""

    station = [Station.station,Station.name]
    stationinfo = session.query(*station).all()
    stationlist = [x for x in stationinfo]
    

    return jsonify(stationlist)


@app.route("/api/v1.0/tobs")
def dateandtemp():
    """Gives the date and temperature for the past year"""
    datetemp = session.query(Measurement.tobs, Measurement.date).\
                filter(Measurement.date >= '2016-08-23')
    
    datetemplist = [y for y in datetemp]

    return jsonify(datetemplist)


#Date has to be entered in "YYYY-MM-DD" format
@app.route("/api/v1.0/<start>")
def temp_after_start(start):
    """Return the avg,min,max for dates greater than or equal to start date"""

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    # Convert list of tuples into normal list
    temperatures_start = list(np.ravel(results))

    return jsonify(temperatures_start)




#Date has to be entered in "YYYY-MM-DD" format
@app.route("/api/v1.0/<start>/<end>")
def temperatures_start_end(start, end):
    """ When given the start and the end date, calculate the TMIN, TAVG, 
        and TMAX for dates between the start and end date inclusive.
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    
    # Convert list of tuples into normal list
    temperatures_start_end = list(np.ravel(results))

    return jsonify(temperatures_start_end)







if __name__ == '__main__':
    app.run(debug=True)


