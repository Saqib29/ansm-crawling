from flask import Flask, render_template, request, flash, redirect, url_for
from crawl_operation import ansm
import time

app = Flask(__name__)
app.secret_key = "secret_key"
chromdriver = 'chromedriver/chromedriver'
# chromedriver for linux
# chromdriver = 'chromedriver/chromedriver'

@app.route('/', methods=['GET', 'POST'])
def home():
    # print(request.method)
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        search_key = request.form['s']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        anteriority = request.form['anteriority']
        if len(search_key) == 0:
            flash('Please search something ..')
            return redirect(url_for('home'))
        
        date = (start_date, end_date)
        crawl_obj = ansm.SearchOperation(chromdriver)
        searched_data = crawl_obj.search(search_string=search_key, date=date, anteriority=anteriority)

        if searched_data == False:
            return "worked"

        return render_template('display_result.html', searched_results=searched_data, search_key=search_key)


if __name__ == "__main__":
    app.run(debug=True)
