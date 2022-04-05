import sys
import os
from os import environ
from flask import Flask, request, jsonify
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('review_URL') or 'mysql+mysqlconnector://root:root@localhost:3306/review'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

 
db = SQLAlchemy(app)
CORS(app) 
 
class Review(db.Model):
    __tablename__ = 'review'
 
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cocktail_name = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    reviewer_name = db.Column(db.String(30), nullable=False)
    reviewer_comment = db.Column(db.String(500), nullable=False)
    date_time = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
 
    def __init__(self, review_id, cocktail_name, rating, reviewer_name, reviewer_comment, date_time):
        self.review_id = review_id
        self.cocktail_name = cocktail_name
        self.rating = rating
        self.reviewer_name = reviewer_name
        self.reviewer_comment = reviewer_comment
        self.date_time = date_time
 
    def json(self):
        return {"review_id": self.review_id, "cocktail_name": self.cocktail_name, "rating": self.rating, "reviewer_name": self.reviewer_name, "reviewer_comment": self.reviewer_comment, "date_time": self.date_time}
 
#   `review_id` int NOT NULL AUTO_INCREMENT,
#   `cocktail_id` int NOT NULL,
#   `rating` int NOT NULL,
#   `reviewer_name` varchar(30) NOT NULL,
#   `reviewer_comment` varchar(500) NOT NULL,
#   `date_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 
@app.route("/review")
def get_all():
    reviewlist = Review.query.all()
    if len(reviewlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "reviews": [review.json() for review in reviewlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no reviews."
        }
    ), 404
 
 
@app.route("/review/<string:cocktail_name>")
def find_by_cocktail_name(cocktail_name):
    reviews = Review.query.filter_by(cocktail_name=cocktail_name).all()

    if len(reviews):
            return jsonify(
                {
                    "code": 200,
                    "data": [review.json() for review in reviews]
                }
            )
    return jsonify(
            {
                "code": 404,
                "message": "Review not found."
            }
        ), 404
  

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": cocktail reviews ...")
    app.run(host='0.0.0.0', port=5021, debug=True)
