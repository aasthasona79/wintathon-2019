from flask import Flask, render_template,url_for
import os
import pandas as pd
import random
app = Flask(__name__)

@app.route("/")
def index():
	file = 'Events-v1.csv'
	event=pd.read_csv(file)
	l=event["Event Name"]
	print(type(l))
	return render_template("index.html",eventt=l,num=3)

@app.route("/<name>")
def name(name):
	print name[0:len(name)-5]
	file = 'Events-v1.csv'
	event=pd.read_csv(file)
	l=event["Event Name"]
	for i in range(0,len(l)):
		if l[i] == name:
			break
	description=event["Description"][i]
	tags=event["Tags"][i].split(',')
	print(tags[random.randint(0,len(l))])
	#print(description)
	source = unicode(description, 'utf-8')
	latitude = event["coordinates"][0]
	longitude = event["coordinates"][1]

	return render_template(name,name=name[0:len(name)-5],description=source,tag1=tags[0],tag2=tags[1],tag3=tags[2],latitude=latitude,longitude=longitude)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
   app.run(debug = True)