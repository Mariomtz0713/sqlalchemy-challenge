# Import the dependencies.
from flask import Flask, jsonify 
import datetime as dt
import sqlalchemy
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return(
        f"Welcome to Mario's first offical page!<br/>"
        f"Here are the avaliable api routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Initializing query
    recent_date = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_year_date = (dt.datetime.strptime(recent_date.date, '%Y-%m-%d') - dt.timedelta(days=365)).date()
    last12months_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year_date).all()
    session.close()
    
    return jsonify(dict(last12months_query))


@app.route("/api/v1.0/stations")
def stations():
    # Initializing query
    station_list_query = session.query(Station.station).all()
    session.close()

    # Unraveling query
    converted_station_list_query = list(np.ravel(station_list_query))
    
    return jsonify(converted_station_list_query)


@app.route("/api/v1.0/tobs")
def tobs():
    # Initializing query
    recent_date = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_year_date = (dt.datetime.strptime(recent_date.date, '%Y-%m-%d') - dt.timedelta(days=365)).date()
    most_active_station_temps_query = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date >= last_year_date).all()
    session.close()

    # Unraveling query
    converted_most_active_station_temps_query = list(np.ravel(most_active_station_temps_query))
    
    return jsonify(converted_most_active_station_temps_query)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Initializing query
    start_date = start
    temps_analysis = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    # Unraveling query
    converted_temps_analysis = list(np.ravel(temps_analysis))

    # Making the data visually clear and appealing
    min_temp = converted_temps_analysis[0]
    max_temp = converted_temps_analysis[1]
    avg_temp = converted_temps_analysis[2]
    temps_analysis_dict = {'Min temp': min_temp, 'Max temp': max_temp, 'Avg temp': avg_temp}

    return jsonify(temps_analysis_dict)
  
 
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Initializing query
    start_date = start
    end_date = end
    temps_analysis = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    session.close()

    # Unraveling query
    converted_temps_analysis = list(np.ravel(temps_analysis))

    # Making the data visually clear and appealing
    min_temp = converted_temps_analysis[0]
    max_temp = converted_temps_analysis[1]
    avg_temp = converted_temps_analysis[2]
    temps_analysis_dict = {'Min temp': min_temp, 'Max temp': max_temp, 'Avg temp': avg_temp}

    return jsonify(temps_analysis_dict)



if __name__ == "__main__":
    app.run(debug=True)