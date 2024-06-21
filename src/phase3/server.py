from flask import Flask
from flask import render_template
from flask import request
import joblib
import re

# clean user input
def preprocess(text):
    text = re.findall(r'\b\w+\b', text.lower())  # lowercase and strip
    return ' '.join(text)

# load the trained model and vectorizer
vectorizer = joblib.load('tfidf_vectorizer_user_review.pkl')
regressor = joblib.load('random_forest_regressor_user_review.pkl')

def create_app(vectorizer, regressor):

    # app settings
    app = Flask(__name__)

    # model
    vectorizer=vectorizer
    regressor=regressor

    # host main page
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # feed input to model and pull rating
    def predict_rating(summary):
        summary = preprocess(summary)
        summary_tfidf = vectorizer.transform([summary])
        rating = regressor.predict(summary_tfidf)[0]
        return rating
    
    # recieve summary text from user
    @app.route('/sendSummary', methods=['POST'])
    def sendSummary():
        if request.method == 'POST':
            summary = request.form['summary']
            rating = predict_rating(summary)
            print("Predicted rating:", round(rating, 2))
        return str(rating)
    return app

create_app(vectorizer, regressor).run(host='0.0.0.0', port=5050, debug=True)

