import numpy as np
import datetime as dt
from matplotlib import style
import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
inspector = inspect(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome<br/>"
        f"Available Routes:<br/>"
        f"Precipitation Information: /api/v1.0/precipitation<br/>"
        f"Station Information: /api/v1.0/stations<br/>"
        f"Temperature Information: /api/v1.0/tobs<br/>"
        f"Information from a specific date: /api/v1.0/Insert Date as YYYY-MM-DD<br/>"
        f"Information for a specific date range /api/v1.0/Insert Start Date as YYYY-MM-DD/Insert End Date as YYYY-MM-DD"
    )





@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    for date in last_date:
        sep_date=date.split('-') 

    year=int(sep_date[0]); 
    month=int(sep_date[1]); 
    day=int(sep_date[2]);
    first_date = dt.date(year, month, day) - dt.timedelta(days=365)
    
    precip_year = session.query(Measurement.date, Measurement.prcp).\
        filter(func.strftime(Measurement.date)>= first_date).\
        order_by(Measurement.date).all()

    prcp=[]
    for precip in precip_year:
        dict = {}
        dict["date"] = precip.date
        dict["prcp"] = precip.prcp
        prcp.append(dict)

    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def station():
    num_stations = session.query(Station.station).count()

    station_activity = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()    

    stations = []
    for station in station_activity:
        dict = {}
        dict["station"] = station[0]
        dict["count"] = station[1]
        stations.append(dict)

    return jsonify(stations)        




@app.route("/api/v1.0/tobs")
def tempertature():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    for date in last_date:
        sep_date=date.split('-') 

    year=int(sep_date[0]); 
    month=int(sep_date[1]); 
    day=int(sep_date[2]);
    first_date = dt.date(year, month, day) - dt.timedelta(days=365)
    
    temp_year = session.query(Measurement.date, Measurement.tobs).\
        filter(func.strftime(Measurement.date)>= first_date).\
        order_by(Measurement.date).all()


    temp=[]
    for temperature in temp_year:
        dict = {}
        dict["date"] = temperature.date
        dict["temp"] = temperature.tobs
        temp.append(dict)

    return jsonify(temp)

@app.route("/api/v1.0/<start_date>")
def from_date(start_date):
    
    from_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    calc_temps=[]
    for obs in from_date:
        dict = {}
        dict["Temp Min"] = obs[0]
        dict["Temp Avg"] = obs[1]
        dict["Temp Max"] = obs[2]
        calc_temps.append(dict)

    return jsonify(calc_temps)

@app.route("/api/v1.0/<start_date>/<end_date>")
def from_to_date(start_date, end_date):
    
    from_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    calc_temps=[]
    for obs in from_date:
        dict = {}
        dict["Temp Min"] = obs[0]
        dict["Temp Avg"] = obs[1]
        dict["Temp Max"] = obs[2]
        calc_temps.append(dict)

    return jsonify(calc_temps)
if __name__ == "__main__":
    app.run(debug=True)


