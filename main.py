#!/usr/bin/env python
from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for
from stocks import query_api
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


# time_series_monthly, symbol
@app.route('/weeklystockhistory')
def weeklystockhistory():
    return render_template('weeklystockprice.html',
                           data=[{'name': 'TSLA'}, {'name': 'AAPL'}, {'name': 'AMZN'}, {'name': 'MSFT'},
                                 {'name': 'NIO'}, {'name': 'NVDA'}, {'name': 'MRNA'},
                                 {'name': 'NKLA'}, {'name': 'FB'}, {'name': 'AMD'}])


@app.route("/result", methods=['GET', 'POST'])
def result():
    data = []
    error = None
    select = request.form.get('comp_select')
    resp = query_api(select)
    pp(resp)
    if resp:
        data.append(resp)
        if len(data) != 2:
            error = 'Bad Response from Stock API'
            df = pd.DataFrame(data)
            df.to_csv()
            return render_template('result.html', data=df, error=error)


@app.route("/compare")
def comparestocks():
    return render_template('compare.html',
                           data=[{'name': 'TSLA'}, {'name': 'AAPL'}, {'name': 'AMZN'}, {'name': 'MSFT'},
                                 {'name': 'NIO'}, {'name': 'NVDA'}, {'name': 'MRNA'},
                                 {'name': 'NKLA'}, {'name': 'FB'}, {'name': 'AMD'}])


@app.route("/comparestocks", methods=['GET', 'POST'])
def comaprestock():
    data = []
    error = None
    select = request.form.get('comp_select')
    resp = query_api(select)
    pp(resp)
    if resp:
        data.append(resp)
        if len(data) != 2:
            error = 'Bad Response from Stock API'
            return render_template('result.html', data=data, error=error)


@app.route('/thankyou')
def future():
    return render_template('future.html')


if __name__ == '__main__':
    app.run(debug=True)
