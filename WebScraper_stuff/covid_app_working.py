from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraper

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    covid_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", sickly=covid_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    covid_data = scraper.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, covid_data, upsert=True)

    # Redirect back to home page
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)