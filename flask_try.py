# https://stackoverflow.com/questions/12277933/send-data-from-a-textbox-into-flask
from flask import Flask, request, render_template
import scratch
from basic_query import Query

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/', methods=['POST'])
def my_form_post():
    if request.method == 'POST':
        user_input = request.form['user_input']
        print(user_input)
        return search(user_input)
    return render_template('welcome.html')

def search(user_input):
    qObj = Query()
    # result_list = qObj.get_result_falsk(user_input)
    result_list = scratch.get_result_falsk(user_input)
    print(result_list) # [url, title, body]
    return render_template('search.html', user_input=user_input, result_list=result_list)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
