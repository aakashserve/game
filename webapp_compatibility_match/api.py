import uuid
import datetime
import webbrowser
import pandas as pd
import random as r
from flask import Flask, flash, redirect, render_template, request, session, abort,redirect,url_for

app = Flask(__name__)
# app = Flask(static_folder='../templates/')
 
@app.route("/")
def hello():
	return render_template('index.html')

@app.before_first_request
def load_global_data():
	## Load Logger File
	global log_file_object, questions, num_questions
	log_file_object = open('logs/log_file.tsv','a')
	questions = pd.read_csv('questions/questions.csv')
	num_questions = 3
	# print(questions_bank.shape)
	print("All Files Loaded")

#generate link value
def generate_link_value():
	return uuid.uuid4().hex

## generate html file run time
def generate_html_file(link_value):
	f = open("templates/"+str(link_value)+".html","w")
	start = """
	    <!DOCTYPE html>
	    <html>
	    <body>
	    <h1>Hey buddy, let's grill your interests</h1>
	    <form method="POST" action="{{url_for('capture_user_response')}}">
	"""
	end = """
	    </form>
	    </body>
	    </html>
	"""
	selected_questions = questions.sample(num_questions)
	radio = '' # empty array to push the rows of input tags 
	for index,row in selected_questions.iterrows():
	    radio  = radio +'<p>{0}</p>'.format(row['question_text'])
	    for options in row['options'].split(','):
	        radio = radio +'<input type="radio" id="{0}{1}" name="question{0}" value="{1}"> "{1}"<br>'.format(row['question_id'],options)
	message = start + radio + end 
	f.write(message)
	f.close()
	return message


@app.route('/generate_link',methods = ['POST'])
def generate_link():
	if request.method == 'POST':
		print(request.form.to_dict())
		# {'mobileno': u'35467', 'firstname': u'Abc'}
		entered_name = request.form.to_dict()['firstname']
		entered_mobile_no = request.form.to_dict()['mobileno']
		## get random link value
		link_value = generate_link_value()
		print("Entered Name {}".format(entered_name))
		print("Entered Mobile No {}".format(entered_mobile_no))
		print("Link value {}".format(link_value))
		## store it into logfile (datetime, name, mobile no, link_value, )
		log_file_object.write(str(datetime.datetime.now())+'\t'+\
			str(entered_name)+'\t'+\
			str(entered_mobile_no)+'\t'+\
			str(link_value))
		log_file_object.write('\n')
		## create html file with name same as link value in template page
		html_file_code = generate_html_file(link_value = link_value)
		html_page_link = 'https://compatibility-check.herokuapp.com/'+link_value
		sharing_message = "Share this link with your friend ! " + html_page_link
		#webbrowser.open_new_tab()
		return render_template("result.html",sharable_link=sharing_message,\
			html_file_code=html_file_code)
		#return render_template("index.html",result=sharing_message)
	else:
		print("Not gone inside result")

if __name__ == "__main__":
	app.run(host="127.0.0.1",port=9091)