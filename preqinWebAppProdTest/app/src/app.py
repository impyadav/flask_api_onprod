"""
# -*- coding: utf-8 -*-

Created on Aug 2023
@author: Prateek Yadav

"""
import time
import logging
from .prediction import onlinePred
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

logging.basicConfig(filename='./logs/onlinePredApp.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class InvalidRequestError(Exception):
    pass


def isSentence(ip, min_words=2, max_words=100):
    """
    Check if the input string is a valid sentence based on the number of words.
    :param ip: The input string to be checked as a sentence.
    :param min_words: The minimum number of words allowed in the sentence. Default is 2.
    :param max_words: The maximum number of words allowed in the sentence. Default is 100.
    :return: bool: Returns True if the input string is a valid sentence based on the word count criteria,
                   and False otherwise
    """
    if (len(ip.split()) >= min_words) and (len(ip.split()) <= max_words):
        return True
    else:
        return False


@app.route("/")
@cross_origin()
def hello():
    """
     To check if Flask API is up or not
    """
    return "Hello!"


@app.route('/pred', methods=['POST'])
@cross_origin()
def predict():
    """
    Route to perform a prediction based on input data.

    This route handles a POST request to perform a prediction. The incoming JSON data
    is expected to contain an 'input' field. The input string is first checked to determine
    if it qualifies as a sentence using the 'isSentence' function. If the input is a valid
    sentence, a prediction is generated using the 'onlinePred' class. The prediction time
    is recorded, and the result is included in the JSON response. If the input is not a
    valid sentence, an error is raised.

    :return: A JSON response containing either predictions or an error message.
    """
    try:
        req = request.get_json()
        if 'input' in req:
            payload = req['input'].strip()
            app.logger.info('#tokens in payload: {}'.format(len(payload.split())))
            if isinstance(payload, str):
                if isSentence(payload):
                    onlinepredObj = onlinePred(payload)
                    start_time = time.time()
                    result = onlinepredObj.inference()
                    pred_duration = (time.time() - start_time) * 1000
                    app.logger.info("prediction time: %0.02f ms" % (pred_duration))
                    response = jsonify({'predictions': str(result)})
                    response.status_code = 200
                    # app.logger.info()
                else:
                    raise InvalidRequestError('Invalid input || Not a sentence')
            else:
                raise InvalidRequestError('Invalid input || Not a sentence || Not a string'.format(type(payload)))

        else:
            raise ValueError('"input" argument missing in payload')

    except InvalidRequestError as e:
        response = jsonify({'error': str(e)})
        response.status_code = 420
        app.logger.error(e)

    except ValueError as e:
        response = jsonify({'error': str(e)})
        response.status_code = 420
        app.logger.error(e)

    except Exception as e:
        response = jsonify({'error': 'Error occurred in Flask api call || {}'.format(e)})
        app.logger.error(e)
        # response.status_code = 500
    return response

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8989, debug=True)
