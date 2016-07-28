import logging
import time
from json import dumps

import requests
from celery import Celery
from flask import Flask, render_template, request, session, abort
from flask_mail import Mail, Message

app = Flask(__name__)

# EMAIL SETTINGS
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_PORT = 465
# CELERY_SETTINGS
CELERY_BROKER_URL = ''  # your brocker url for celery
CELERY_RESULT_BACKEND = ''  # your backend for storing task results
# EMAIL SENDER SETTINGS
MAIL_USERNAME = ''  # your email username
MAIL_PASSWORD = ''  # your email pass
# LOG FILE SRC
LOG_FILE = ''  # where stored your log file

# URL FOR ELASTICSEARCH
ES_URL = 'http://localhost:9200'
app.config.update(
    DEBUG=False,
    MAIL_SERVER=EMAIL_SERVER,
    MAIL_PORT=EMAIL_PORT,
    MAIL_USE_SSL=True,
    CELERY_BROKER_URL=CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=CELERY_RESULT_BACKEND,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD
)
# variable for sending Email
mail = Mail(app)


# prepearing celery for flask app
def make_celery(app):
    celery = Celery('TestBooks', backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'], )

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


# variable for decorating functionts for salary
celery = make_celery(app)


@app.route('/')
def index():
    """
    Index page
    :return rendered page in html:
    """
    return render_template('TestBooks/index.html')


@app.route('/search', methods=['POST'])
def search_run():
    """
    Method where we get post data. It`s email and search query.
    then start in another thread searching and sending mail
    by calling function search_text.delay()
    using celery as task queue
    :return : HTTP status OK
    """
    try:
        json = request.json
        session['email'] = json['email']
        search_text.delay(json['email'], json['searchText'])
    except:
        abort(400)
    return "", 200


@celery.task()
def search_text(email, search_text):
    """
    Method where we do text search by using elasticsearch
    :param email: email where send result of searching
    :param search_text: what we search
    :return: result of searching
    """
    # create request data for elasticsearch
    request_data = {
        "_source": False,
        "query": {
            "match_phrase": {
                "text": search_text
            }
        }
    }
    request_data = dumps(request_data)
    # count time for searching
    start_time = time.time()

    result_search = 'Result by searching with word: "{}"\n'.format(search_text)
    # send search request with data
    res = requests.get('{0}/books/_search?pretty'.format(ES_URL), data=request_data).json()

    # parsing response from request
    if res['hits']['total']:  # checking if we have some result
        try:
            for hit in res['hits']['hits']:
                book_id = hit['_id']
                book_name = hit['_type']
                data_book = requests.get('{0}/books/{1}/{2}?pretty'.format(ES_URL, book_name, book_id),
                                         data=request_data).json()
                book_chapter = data_book['_source']['chapter']
                book_page = data_book['_id']

                result_search += "Find in book: {0}\nChapter: {1}\nPage: {2}\n".format(book_name, book_chapter,
                                                                                       book_page)
        except Exception as e:
            result_search += "Oops. something going wrong. We do all best to fix it "
            abort(500)

    else:  # if result is none
        result_search += "Not found any text with this word"
    # searching time
    end_time = time.time() - start_time
    # get logger for writing how much time we search
    logger = get_custom_logger()
    logger.info('Time for search by word "{0}" is {1}'.format(search_text, end_time))

    send_email(result_search, email)
    return result_search


def send_email(message_string, email):
    """
    function for sending email using settings above
    :param message_string: what message we want to send
    :param email: on what email
    :return: none
    """
    with mail.connect() as conn:  # get server connection
        subject = "Search result in books"
        # create message for sending
        msg = Message(recipients=[email],
                      body=message_string,
                      subject=subject,
                      sender=MAIL_USERNAME)
        conn.send(msg)


@app.route('/result', methods=['GET'])
def search_result():
    """
    page for showing mesage that we get email and search text
    and we start searching
    :return:
    """
    return render_template('TestBooks/search_result.html', email=session.get('email'))


def get_custom_logger():
    """
    function for getting logger file
    :return:
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(LOG_FILE, 'w')
    logger.addHandler(handler)
    return logger


@app.errorhandler(404)
def page_not_found(e):
    return render_template('TestBooks/error404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('TestBooks/error500.html'), 500


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
