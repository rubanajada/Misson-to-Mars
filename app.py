from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = 'mongodb://localhost:27017/mission_to_mars'
client = pymongo.MongoClient(conn)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    mars = client.db.listings.find_one()

    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars = client.db.mars
    data = scrape_mars.scrape_info()
    mars.update({}, data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
