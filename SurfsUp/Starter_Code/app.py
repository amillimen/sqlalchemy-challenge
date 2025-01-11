# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


app = Flask(__name__)

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#home route
@app.route("/")
def home():
    return(
        f"<center><h2>Welcome to the Hawaii Climate Analysis local API</h2></center>"
        f"<center><h3>Select from one of the avaiable routes:</h3></center>"
        f"<center>api/v1.0/precipitation<center>"
        f"<center>api/v1.0/stations<center>"
        f"<center>api/v1.0/tobs<center>"
        f"<center>api/v1.0/start/end<center>"
        )

#api//v1.0/pstations route
@app.route("/api//v1.0/precipitation")
def precip():

    #return the previous year's precip as json
    # Calculate the date one year from the last date in data set.
    previousYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    previousYear

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previousYear).all()

    session.close

#dictionary with the date as the key and the precipitatin (prcp) as the value
    precipitation = {date: prcp for date, prcp in results}

    return jsonify(precipitation)

    #api//v1.0/precipitation<center>"

@app.route("/api//v1.0/stations")
def stations():

    #run query to identify stations
    results = session.query(Station.station).all()
    session.close

    stationList = list(np.ravel(results))

    #convert to json and display
    return jsonify(stationList)

@app.route("/api//v1.0/tobs")
def temperatures():
    
    # Calculate the date one year from the last date in data set.
    previousYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    
    results = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= previousYear).all()
    
    session.close()

    temperatureList = list(np.ravel(results))

    #return the list of temperatures
    return jsonify(temperatureList)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):

    #select statement
    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    if not end:
        startDate = dt.datetime.strptime(start, "%m%d%Y")

        results = session.query(*selection).filter(Measurement.date >= startDate).all()

        session.close()

        dateList = list(np.ravel(results))

        return jsonify(dateList)

    else: 
        startDate = dt.datetime.strptime(start, "%m%d%Y")
        endDate = dt.datetime.strptime(end, "%m%d%Y")

        results = session.query(*selection).filter(Measurement.date >= startDate).all()

        session.close()

        dateList = list(np.ravel(results))

        return jsonify(dateList)


#app Launcher
if __name__=='__main__':
    app.run(debug=True)
