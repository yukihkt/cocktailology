from flask import Flask, request, jsonify
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/review'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
 
class Review(db.Model):
    __tablename__ = 'review'
 
    reviewID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    strDrink = db.Column(db.String(50), nullable=False)
    reviewerName = db.Column(db.String(30), nullable=False)
    reviewerComment = db.Column(db.String(500), nullable=False)
    dateTime = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
 
    def __init__(self, reviewID, strDrink, reviewerName, reviewerComment, dateTime):
        self.reviewID = reviewID
        self.strDrink = strDrink
        self.reviewerName = reviewerName
        self.reviewerComment = reviewerComment
        self.dateTime = dateTime
 
    def json(self):
        return {"reviewID": self.reviewID, "strDrink": self.strDrink, "reviewerName": self.reviewerName, "reviewerComment": self.reviewerComment, "dateTime": self.dateTime}
 
 
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
 
 
@app.route("/review/<string:strDrink>")
def find_by_isbn13(strDrink):
    review = Review.query.filter_by(strDrink=strDrink)

    if review:
            return jsonify(
                {
                    "code": 200,
                    "data": review.json()
                }
            )
    return jsonify(
            {
                "code": 404,
                "message": "Review not found."
            }
        ), 404

# can change the code to write post if we want 
# @app.route("/book/<string:isbn13>", methods=['POST'])
# def create_book(isbn13):
#     if (Book.query.filter_by(isbn13=isbn13).first()):
#         return jsonify(
#             {
#                 "code": 400,
#                 "data": {
#                     "isbn13": isbn13
#                 },
#                 "message": "Book already exists."
#             }
#         ), 400

#     data = request.get_json()
#     book = Book(isbn13, **data)

#     try:
#         db.session.add(book)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#             "code": 500,
#             "data": {
#                 "isbn13": isbn13
#             },
#             "message": "An error occurred creating the book."
#         }
#     ), 500

#     return jsonify(
#         {
#             "code": 201,
#             "data": book.json()
#         }
#     ), 201
 
 
if __name__ == '__main__':
    app.run(port=5090, debug=True)
