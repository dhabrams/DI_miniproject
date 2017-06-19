from flask import Flask,render_template,request,redirect
import requests
import json
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components

app = Flask(__name__)

@app.route('/')
def main():
	return redirect('/index')


@app.route('/index',methods=['GET','POST'])   
def getclose():
	if request.method == 'GET':
		return render_template('index.html') 
	else:
		
		stock = request.form['symbol']
		search_url="https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=20170501&date.lt=20170531&ticker=" + stock + "&api_key=9sjzm4hqVmJ3P48oAyUz"

		req = requests.get(search_url)
		stock_data = req.json()

		col_labels = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume', 'ex-dividend', 'split_ratio', 'adj_open', 'adj_high', 'adj_low', 'adj_close', 'adj_volume']
		
		df = pd.DataFrame.from_dict(stock_data['datatable']['data'][0:])

		df.columns = col_labels

		df['date'] = pd.to_datetime(df['date'])
		df = df.set_index(['date'])

		output_file("lines.html")

		p = figure(title="May Closing quotes for " + stock, x_axis_label= 'date', x_axis_type = 'datetime', y_axis_label='close')

		p.line(df.index,df.close, line_width=2)

		script, div = components(p)

		#show(p)
		return render_template('graph.html',script=script, div=div) 
		return redirect('/index')

if __name__ == "__main__":
	app.run(port=33507)  # need '(host='0.0.0.0')' for digitalocean instead