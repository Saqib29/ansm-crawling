from flask import Flask, render_template, request, flash, redirect, url_for
from crawl_operation import ansm
import time

app = Flask(__name__)
app.secret_key = "secret_key"



@app.route('/', methods=['GET', 'POST'])
def home():

    # if http request for GET then how template
    if request.method == 'GET':
        return render_template('home.html')


        #  else check POST or not then further procedure done
    elif request.method == 'POST':

        # search input 
        search_key = request.form['s']


        #  start_date and end_date
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        date = (start_date, end_date)      # date just for send data as touple of start_date & end_date

        
        # comes from choose an anteriority
        anteriority = request.form['anteriority']



        # search key should not be empty, otherwise should give error message 
        if len(search_key) == 0:
            flash('Please search something ..')
            return redirect(url_for('home'))

        
        # create object for searchOperation of ansm file
        crawl_obj = ansm.SearchOperation()

        #calling the main method search
        searched_data = crawl_obj.search(search_string=search_key, date=date, anteriority=anteriority)
        time.sleep(1)
        
        # rendering display to show searched data 
        return render_template('display_result.html', searched_results=searched_data, search_key=search_key)


if __name__ == "__main__":
    app.run(debug=True)
