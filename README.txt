W4111 Project - Chopped Database - Part 3 submission

Kalpana Ganeshan, kg2712
Maria Teresa Tome Armijo, mtt2130


A) SERVER SETUP: SERVER.PY
Additional functions added to base code provided:

A.1: Ingredients
	PURPOSE:
	Prompts the user to enter an ingredient name, returns the episode information and meal information for every instance of the ingredient

	USER INPUT:
	User enters input in a searchbox and clicks the "search" button. 
	The input is then stripped and lowercased. The function checks for invalid input (an empty string) 	
	The input is then inserted into the query below

	QUERY:
	SELECT distinct i.ingredient_name, e.episode_name, e.air_date, c.is_entree, c.is_appetizer, c.is_dessert 
	FROM ingredient i,meal_contains 
	RIGHT JOIN cook ON meal_contains.course_id=cook.course_id 
	RIGHT JOIN course c ON meal_contains.course_id=c.course_id 
	RIGHT JOIN episode e ON e.series_episode=cook.series_episode 
	WHERE i.ingredient_name LIKE '%%{input}%%'"

	DISPLAYING RESULTS:
	Add each result as a tuple to a list (the variable "ings")
	Render the results.html template and pass in the results and the source.

	
A.2: Contestants 
	PURPOSE:
	Prompts the user to check boxes for different attributes of the contestant entity (ex: state, place of work) and groups the rows by the entities checked
	
	USER INPUT:
	User checks appropriate boxes and clicks "search" button
	For each box, if checked, add to a list of columns(variable "columns") and add to a string containing the column names (variable "query_string")
	If the query string is empty, return the current page
	If not, insert "query_string" into below query	

	QUERY:
	SELECT {query_string}, COUNT(*) AS frequency 
	FROM contestant 
	LEFT JOIN works_in USING (first_name, last_name) 
	GROUP BY {query_string} ORDER BY frequency DESC

	DISPLAYING RESULTS:
	Create a list with the column names + "Frequency" to display the results of the groupby
	For each row in result, add as a tuple to a list (the variable "contest")
	Render the results.html template and pass in the results and the source.	

A.3: Judges 
	PURPOSE:
	Promts the user to enter either (1) a judge's first name or (2) a judge's first and last name and returns information on all episodes with the judge.

	USER INPUT:
	User enters input in a searchbox and clicks the "search" button. 
	The input is then stripped and lowercased and split by a space to turn it into a list
	If the length of the list is 1, the user has just entered a first name. Query 1 is run with the user input.
	If the length of the list is 2, the user has entered a first and last name. Query 2 is run with the user input.
	If neither of the above is true, the input is invalid and the current page is returned.
	
	QUERY:
	Query 1) If the user enters only a first name, capitalize the first name and query
	SELECT first_name, last_name, episode_name, air_date 
	FROM Judges 
	RIGHT JOIN episode ON Judges.series_episode=episode.series_episode 
	WHERE first_name LIKE '%%{s}%%'".format(s=input[0].capitalize())

	Query 2) if the user enters a first and last name, capitalize the names and query
	SELECT first_name, last_name, episode_name, air_date 
	FROM Judges 
	RIGHT JOIN episode ON Judges.series_episode=episode.series_episode 
	WHERE first_name LIKE '%%{s}%%' AND last_name LIKE '%%{p}%%'".format(s=input[0].capitalize(), p=input[1].capital

	DISPLAYING RESULTS:
	Create a variable "judges" with the column names to display
	For each row in result, add as a tuple to "judges"
	Render the results.html template and pass in the results and the source.

A.4: Episodes (and seasons)
	PURPOSE:
	Prompts the user to enter comma separated keywords and returns the episode and season information with episodes having titles with the keywords entered

	USER INPUT:
	User enters input in a searchbox and clicks the "search" button. 
	The input is then stripped and lowercased and split by a comma to turn it into a list	
	Every word in the list is capitalized.
	If the length of the input is 0, the current page is returned
	A base query string is established (see below) and the first element in the list is added.
	For every successive element, the query expands
		
	
	QUERY:
	We start with a base query and construct the query successively.
	Base query) 
		SELECT season_number, series_episode, episode_name, air_date 
		FROM aired_in RIGHT JOIN episode USING (series_episode) 
		WHERE episode_name LIKE
	We add the first element in the list to the query)
		base query + '%%{s}%%'".format(s=input[0])
	For each additional element, we add)
		" UNION " +base_query + " '%%{s}%%'".format(s=i)
	
	DISPLAYING RESULTS:
	Create a variable "episodes" with the column names to display
	For each row in result, add as a tuple to "episodes" 
	Render the results.html template and pass in the results and the source.	

B) HTML FILES

B.1: Index.html
	PURPOSE:
	Base page; displays menu bar and options to navigate to pages to query

	FEATURES:
	Top navigation bar
	Navigation buttons to each of the pages
	

B.2: Entity.html
	PURPOSE:
	A template for each entity's page to query and interact with the entity	

	FEATURES:
	Top navigation bar
	All searchboxes have placeholder text and submit buttons
	Checkbox implementation 

B.3: Results.html
	PURPOSE:
	A template to display the results from queries on every page

	FEATURES:
	Top navigation bar
	Hover tables to display results from all queries
	Because the number of columns is dependent on the checkboxes for contestants, code implementation takes into account number of checkboxes and only displays relevant columns


Thank you!
