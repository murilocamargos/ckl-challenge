Cheesecake Labs Challenge
=========================

This is an API created with Django Rest Framework to serve articles from major blogs. The API is currently fetching articles from:

* TechCrunch
* Cheesecake Labs
* Engadget
* Mashable

Each blog has it own scraper specialized in fetching data from that specific blog. Some gathers information from twitter statuses, some from google plus feeds and others from the good old RSS system. To do this, the **cool GitHub libraries** were listed in a requirements file for **dependency management**.

On behalf of simplicity, the code was deployed on Heroku via CodeShip. This was done so after a push on this repo, CodeShip would be hooked to start the **automatic tests and deployment** setting a **continuously integrated** environment for our app. The API docs can be found [here](https://cheesecake-challenge.herokuapp.com) and it provides methods for **querying/filtering the stored articles**, it also describes the use of `POST`, `PUT`, `PATCH` and `DELETE` HTTP methods for admin users *(admin:admin123)*.

A simplified scheme on how the app works is given in the figure below:

![Untitled Diagram.png](https://i.imgur.com/Ct27gDh.png)


The Challenge
=============


The main goal of this challenge is to analyze the skills and knowledge the applicant presents related to backend architecture, programming and its latest trends, as well as his/her ability to write code, comments and meaningful git commits.

The applicant must create a web app that provides an API according to the REST architecture. Here are the MVP and extra tasks that will be evaluated.

**MVP**

- Create a private repository on Bitbucket and add @carolschmitz as admin;
- The suggested framework is: Django;
- Create a web scraping tool that constantly scrapes the articles of a major blog like TechCrunch (http://techcrunch.com) and stores it in a database (DBMS is a choice of the candidate). These are the relevant data that we want to store:
  - Outlet name and metadata (URL, description, etc);
  - Authors (name, twitter handle, profile page, etc);
  - Published articles and metadata (publication date, author, content, etc);
- Create a JSON REST API endpoints that serve the database data (outlets, authors and articles) - only GET is necessary;
- Host the server and provide its IP, as well as all the endpoint(s);
- An (oversimplified) example of API response for articles: http://www.ckl.io/challenge/.
- Create a pull-request and assign it to @carolschmitz.

**Extras**

- Use cool GitHub libraries to aid the development;
- Use automatic deploys;
- Setup automatic tests;
- Integrate with CI;
- Use a dependency manager;
- Add other REST-compliant HTTP methods for the API (PUT, PATCH, POST, etc);
- Provide an API endpoint to perform searches for articles;

**Evaluation criteria**

- Technical capacity;
- Knowledge on the used tools;
- Code readability and reusability;
- Clarity on descriptive texts;
- A server that resists to DDoS attacks;
- Deadline
