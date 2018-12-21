import data_process as d
from flask import Flask, render_template, request, send_from_directory, Response, g
import os
from os import path

image_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images/')
app = Flask(__name__)      

#THESE WERE TRIALS TO REMOVE CACHE(DIDN'T WORK)
# def after_this_request(func):
#     if not hasattr(g, 'call_after_request'):
#         g.call_after_request = []
#     g.call_after_request.append(func)
#     return func
# @app.after_request
# def per_request_callbacks(response):
#     for func in getattr(g, 'call_after_request', ()):
#         response = func(response)
#     return response
# @app.after_request
# def add_header(response):    
# 	response = make_response()
# 	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
# 	if ('Cache-Control' not in response.headers):
# 		response.headers['Cache-Control'] = 'public, max-age=60'
# 	return response

#TO ADD IMAGES TO WATCH LIST FOR RELOAD
extra_dirs = [image_dir,]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)
#TO REMOVE CACHE(WORKING)
@app.after_request
def add_header(r):
	r.headers['Cache-Control'] = 'public, max-age=0'
	r.headers["Expires"] = "0"
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"    
	return r


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/search')
def search():
	#THIS WAS A TRIAL TO REMOVE CACHE(DIDN'T WORK)
	# response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	# response.headers['Pragma'] = 'no-cache'
	# @after_this_request
	# def delete_cache(response):
	# 	response.cache_control(max_age='5')
	# 	return response
	Response.CacheControl = "no-cache"
	server = request.args.get('servername', default = '*' , type = str)
	date_in = request.args.get('date_in', type = str)
	if server == '*':
		return render_template('search_noargs.html')
	#search_noargs displays that no arguments have been sent in URL
	elif server== "":
		return render_template('search_nosearch.html')
	#search_nosearch is incase of no search argument or data entry

	else:
		up,cpu,mem = d.search(server,date_in)
		if(up==-1 and cpu==-1 and mem==-1):
			return render_template('search_multiple.html')
		#search_multiple is incase of multiple instances of servername when only one was expected
		return render_template('search.html', uptime=up , cpu_util = cpu , mem_util = mem , d = date_in)
		#search.html receives argument uptime cpu_util and mem_util

@app.route('/tabular')
def tabular():
	zone = request.args.get('zone', default = 'BLR', type = str)
	dataid = request.args.get('dataid', default = 0 , type = str)
	date_in = request.args.get('date_in', type = str)
	param = int(dataid)
	d.update(zone,param,date_in)
	arg = zone+dataid+".png"
	arg = "/images?path=" +arg
	return render_template('tabular.html',filename = arg, d = date_in)

@app.route('/images')
def serve_image():
	path = request.args.get('path',type=str)
	if not (path==''):
		return send_from_directory(image_dir,path)
	else:
		return send_from_directory(image_dir,'noimg.png')

if __name__ == '__main__':
  app.run(debug=True, extra_files=extra_files)