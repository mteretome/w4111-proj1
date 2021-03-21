
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@34.73.36.248/project1
#
# For example, if you had username zy2431 and password 123123, then the following line would be:
#
#     DATABASEURI = "postgresql://zy2431:123123@34.73.36.248/project1"
#

DATABASEURI = "postgresql://kg2712:392115@34.73.36.248/project1" # Modify this with your own credentials you received from Joseph!


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
'''
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
'''

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)
  return render_template("index.html")



  #
  # example of a database query
  '''
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
'''
  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  '''
  context = dict(data = names)
'''

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
 
#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/ingredients', methods=('GET','POST'))
def ingredients():
   if request.method=='POST':
      input=request.form.get('search-box')
      input=input.strip().lower()
      query = "SELECT distinct i.ingredient_name, e.episode_name, e.air_date, c.is_entree, c.is_appetizer, c.is_dessert FROM ingredient i,meal_contains RIGHT JOIN cook ON meal_contains.course_id=cook.course_id RIGHT JOIN course c ON meal_contains.course_id=c.course_id RIGHT JOIN episode e ON e.series_episode=cook.series_episode WHERE i.ingredient_name LIKE '%%{s}%%'".format(s=input)
      cursor = g.conn.execute(query)
      ings  = [("ingredient_name","episode_name","air_date", "is_entree","is_appetizer", "is_dessert")]
      for result in cursor:
         ings.append(result)  # can also be accessed using result[0]
      cursor.close()
      return render_template("results.html",my_title="Ingredients",search_more="ingredients",source="ingr_search",result=ings)

   return render_template("entity.html",
   my_title="Ingredients", my_image="salt.svg",
   title_desc="Every episode uses a set of different ingredients placed on a basket for the three meals the Chefs cook!",
   search_desc="Look up certain foods, specific ingredients, meals.")

@app.route('/contestants', methods = ("GET", "POST"))
def contestants():
  column_dict = {'First Name':'first_name','Last Name':'last_name', 'Place of work':'place_of_work' ,'City':'city', 'State':'state'}
  if request.method == 'POST':
     query_string = ""
     columns = []
     for i in column_dict.keys():
         if request.form.get(i):
             columns.append(i);
             query_string += column_dict[i] + ','
     
     if query_string=="":
         return render_template("entity.html",my_title="Contestants", my_image="bread.svg",title_desc="Every episode invites four Chefs from all over the United States to tell their stories and test their skills! Here are some suggested search queries!",search_desc="Look up locations, professions, last names, etc.")

     query_string = query_string[:-1]
     cursor = g.conn.execute(f"SELECT {query_string}, COUNT(*) AS frequency FROM contestant left join works_in USING (first_name, last_name) GROUP BY {query_string} ORDER BY frequency DESC")
     contest  = [tuple(columns+ ["Frequency"])]
     for result in cursor:
        contest.append(result)  # can also be accessed using result[0]
     cursor.close()
     return render_template("results.html",my_title="Contestants",search_more="contestants",source="contest_search",result=contest,no_columns=len(contest[0]))


  return render_template("entity.html",
   my_title="Contestants", my_image="bread.svg",
   title_desc="Every episode invites four Chefs from all over the United States to tell their stories and test their skills! Here are some suggested search queries!",
   search_desc="Look up locations, professions, last names, etc.")

@app.route('/judges', methods=('GET','POST'))
def judges():
	if request.method=='POST':
		 input=request.form.get('search-box')
		 input=input.strip().lower().split(" ")
		 if len(input)==1:
			 query = "select first_name, last_name, episode_name, air_date FROM Judges RIGHT JOIN episode ON Judges.series_episode=episode.series_episode WHERE first_name LIKE '%%{s}%%'".format(s=input[0].capitalize())
		 elif len(input)==2:
			 query = "select first_name, last_name, episode_name, air_date FROM Judges RIGHT JOIN episode ON Judges.series_episode=episode.series_episode WHERE first_name LIKE '%%{s}%%' AND last_name LIKE '%%{p}%%'".format(s=input[0].capitalize(), p=input[1].capitalize())
		 else:
			 return render_template("entity.html", my_title="Judges", my_image="wine.svg", title_desc="Every episode includes three Chefs to be judges, search who they are!",search_desc="Look up names, Ex: Alex Guarnaschelli")
		 cursor = g.conn.execute(query)
		 judges  = [("First Name", "Last_name", "Episode_name", "Air_date")]
		 for result in cursor:
			 judges.append(result)  # can also be accessed using result[0]
		 cursor.close()
		 return render_template("results.html",my_title="Judges",search_more="judges",source="judge_search",result=judges)
	return render_template("entity.html", my_title="Judges", my_image="wine.svg", title_desc="Every episode includes three Chefs to be judges, search who they are!",search_desc="Look up names Ex: Alex Guarnaschelli")

@app.route('/episodes', methods=('GET','POST'))
def episodes():
	if request.method=='POST':
		 input=request.form.get('search-box')
		 input=input.strip().lower().split(",")
		 input=[i.strip().capitalize() for i in input]
		 if len(input) == 0:
			 return render_template("entity.html",  my_title="Episodes and Seasons", my_image="cheese.svg", title_desc="With 26 seasons spanning over a little more than 10 years there are plenty of episodes to lookup and explore! This page provides info on season and episode information", search_desc="Look up episode keywords, separated by commas!")

		 base_query="SELECT season_number, series_episode, episode_name, air_date FROM aired_in RIGHT JOIN episode USING (series_episode) WHERE episode_name LIKE"
		 query=base_query + " '%%{s}%%'".format(s=input[0])
		 for i in input[1:]:
			 new_addition=" UNION " +base_query + " '%%{s}%%'".format(s=i)
			 query=query+new_addition
		 print(query)
		 cursor = g.conn.execute(query)
		 episodes  = [("season_number"," series_episode"," episode_name","Air_date")]
		 for result in cursor:
			  episodes.append(result)  # can also be accessed using result[0]
		 cursor.close()
		 return render_template("results.html",my_title="Episodes and Seasons",search_more="episodes",source="ep_search",result=judges)
	return render_template("entity.html",  my_title="Episodes and Seasons", my_image="cheese.svg", title_desc="With 26 seasons spanning over a little more than 10 years there are plenty of episodes to lookup and explore! This page provides info on season and episode information", search_desc="Look up episode keywords, separated by commas!")



# Example of adding new data to the database
'''
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()
'''

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
