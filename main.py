from pprint import pprint as pp

import plotly.graph_objects as go
import numpy as np
import pandas as pd
from flask import Flask, render_template, request

from stocks import query_api

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

    dateArr = np.empty(0)
    openArr = np.empty(0)
    highArr = np.empty(0)
    lowArr = np.empty(0)
    closeArr = np.empty(0)
    volArr = np.empty(0)
    mts = resp['Monthly Time Series']

    stock = resp['Meta Data']['2. Symbol']
    print(stock)
    for date in mts:
        dateArr = np.append(dateArr, date)
        info = mts[date]
        openArr = np.append(openArr, info['1. open'])
        highArr = np.append(highArr, info['2. high'])
        lowArr = np.append(lowArr, info['3. low'])
        closeArr = np.append(closeArr, info['4. close'])
        volArr = np.append(volArr, info['5. volume'])

    d = {"date": dateArr, "open": openArr, "high": highArr, "low": lowArr, "close": closeArr, "volume": volArr}
    df = pd.DataFrame(d)

    fig = go.Figure(data=[go.Candlestick(
        x=df['date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='green', decreasing_line_color='red'
    )])

    fig.update_layout(
        title=stock,
        yaxis_title="Stock",
        xaxis_title="Date"
    )

    fig.show()


    if resp:
        data.append(resp)
        if len(data) != 2:
            error = 'Bad Response from Stock API'
            return render_template('result.html', data=data, error=error)

if __name__ == '__main__':
    app.run(debug=True)