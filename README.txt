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


C) The PostgreSQL account where your database on our server resides. (This should be the same database that you used for Part 2, but we need you to confirm that we should check that database.)
The URL of your web application. Once again, please do not turn off your virtual machine after you are done modifying your code and when you are ready to submit, so that your IP address does not change and the URL that you include with your project submission works.

	PostgreSQL account name: Kalpana Ganeshan, kg2712; Password: 392115

	URL: http://34.75.182.236:8111/


D) A description of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway. If you did not implement some part of the proposal in Part 1, explain why.

We have made changes to a few aspects of our project from Part 1, but the core aims have stayed the same. We wanted to implement an application that allowed users to query information from each of the entities and see frequency/instances where their search occurred. 
We also wanted users to be able to query the entities mostly separately, since queries can run a huge range of topics within the schema and it might not make sense to condense those into a single request.
Both of those core aspects were implemented in the project. We have separate pages for each entity for users to interact with, and used flask tools such as searchboxes and checkboxes to implement grouping to provide frequency data.
The one aspect of our project we did not implement was tagging similar ingredients under a category (ex. tagging bass as "fish"). We did not anticipate the difficulty of such a query with the data we had. Implementing this would require adding another dataset to the schema mapping the ingredients to their categories, but many of them are very obscure due to the nature of the show so it was difficult to find a database with the information we needed.
However, we did add functionality to our project. We were able to extract city and state from the location column of the dataset and include that in our querying capabilities through data cleaning in python. 
Additionally, we found a way to query the episode names by entering keywords, which is a practical way for users to explore episodes. For example, if a user wanted to find episodes that involved fish, they can query the keyword "fish" in our episode page to get episodes whose titles contain the word "fish" in it. Users can add as many keywords as they would like.


E) Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.

Two of the most interesting pages are Contestants and Episodes and seasons. The contestants page is interesting as it allows users to check boxes to group the contestants by state, city, place of work, or name (first or last). This was a difficult query to construct as the user can check any number of boxes.
We approached this by building the query by going through each checkbox, checking if it was checked, and adding the appropriate query to the query string, which we executed after we exited the loop. Displaying results also proved to be challenging because the number of columns displayed depends on the number of boxes checked.
The page also has a lot of interesting possibilities - we had a lot of fun trying out different queries to learn more about the contestants! 
The other most interesting page is the episodes and seasons page. This page allows the user to enter in keywords and the results return episode information for episodes containing the keywords entered. We debated whether to construct the query to only include episodes whose names contained all keywords entered, or return the results of episodes with at least one keyword. After playing around with some queries, we decided display all episodes with at least one of the keywords because that proved to return more interesting results, especially for similar keywords (like "champ" and "win").
Therefore, this query was also constructed piece by piece, and we had to be clever in how we did so with the UNION keyword in between each query. This page has a lot of interesting applications as well; seeing which keywords are most commonly and least commonly present in episode names could help viewers of the show understand how the episodes are named.

Thank you!
