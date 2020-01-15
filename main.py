from dataputter import DataPutter
import flask
import json
import schedule
import multiprocessing
import time
import datetime

dp = DataPutter()
app = flask.Flask(__name__)

def job_refresh():
    dp.refresh_data()

def to_json(data):
    return json.dumps(data) + '\n'


def schedule_starter():
    schedule.every(2).hours.do(job_refresh)
    while True:
        schedule.run_pending()
        time.sleep(1)


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype='application/json',
        response=to_json(data)
    )


@app.route('/category/<category>', methods=['GET'])
def test_flask(category):
    if category in dp.categories:
        return resp(200, dp.category_select(category))
    else:
        return resp(400, {'error': 'This is wrong category'})

@app.route('/update/', methods=['GET'])
def get_update_date():
    return resp(200, {"last_update": dp.last_update})

def flask_start():
    print("Starting FLASK API SERVER")
    app.debug = True
    app.run()


def main():
    p1 = multiprocessing.Process(target=schedule_starter)
    p2 = multiprocessing.Process(target=flask_start)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == '__main__':
    main()
