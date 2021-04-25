from flask import Flask, render_template, request, flash, redirect, url_for
from crawl_operation import ansm
import time

app = Flask(__name__)
app.secret_key = "secret_key"
chromdriver = 'chromedriver/chromedriver'

@app.route('/', methods=['GET', 'POST'])
def home():
    # print(request.method)
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        search_key = request.form['s']
        if len(search_key) == 0:
            flash('Please search something ..')
            return redirect(url_for('home'))
        
        crawl_obj = ansm.SearchOperation(chromdriver)
        searched_data = crawl_obj.search(request.form['s'])

        return render_template('display_result.html', searched_results=searched_data, search_key=search_key)


if __name__ == "__main__":
    app.run(debug=True)
