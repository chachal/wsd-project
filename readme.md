WSD Project plan
================

### 1. Team ###
481548 Aku Viitanen  
528375 Charlotta Alén  
426396 Antti Mella  

### 2. Goal ###
Goal of this project is to build a game store service, 
which allows developers to sell browser compatible 
javascript games to users. Service will be responsive 
to allow mobile usage, have databases to store data 
and implement strong security against different attacks.

To accomplish all of this we will be using bootstrap + 
Django framework combo and the project will be deployed 
on Heroku.

### 3. Plans ###

#### 3.1. Database ####
Database is built to support user authentication, purcha- 
sing, scoring and owning games. Django models implement 
ids for all tables, and thus they work great as primary 
keys. Foreign keys will be used to tie the elements to- 
gether and ensure that if for example a game is deleted, 
then the associated scores are deleted as well. Users 
will mostly be set to inactive to keep records of purchases.

![Database schema](https://git.niksula.hut.fi/viitana3/wsd2016-project/raw/master/doc/WSD.png "Database schema")

#### 3.2. Templates and design ####
Bootstrap will be used to help with a clean and informative 
design. Templates will inherit from each other depending 
on user role to reduce repeating code. JQuery will be used 
as the API between the games and the service itself.

#### 3.3. Security ####
Django itself comes with plenty of protection against SQL 
injections and authentication manipulation. Thus the main 
focus for us will be keeping a close eye on JQuery and java- 
script actions. User inputs will be kept very simple to 
ensure proper security checks can be applied. As the data- 
base handles assets of variable value, all kinds of database 
race conditions will be minimized or, if possible, completely 
neutralized.

### 4. Process and time schedule ###
Process will start as soon as the plan is reviewed and 
accepted. Django initialization and dependency scripts 
will be done first to ensure that all project members have 
a smooth start and can get straight to business. Project 
initialization will preferably happen during the holidays. 
From there on we will use sprint format by assigning tasks 
through trello to keep workflow steady. Regular meetups 
wont probably be necessary but collaborating through VOIP 
is probable.

* Weeks 1-2: Database models, basic views and templates 
* Weeks 3-4: Finish models, create views with SQL queries. Extend templates using bootstrap. Finish minimum requirements. 
* Weeks 5-6: JQuery and responsivity. Fill as many optional requirements as possible. 
* Week 7: Finishing touches. Hackathons if previous tasks have fallen behind. 
* 18.2.: Final build deployed


### 5. Testing ###
Unit tests will be written to all views that handle 
complex SQL queries to ensure data doesn't get corrupted. 
Exception catches will be implemented for the duration of 
development to quickly locate possible errors in data 
handling. Django can catch most syntax errors and running 
local server in debug mode during development helps with 
catching errors before too much is built upon them.

### 6. Risk analysis ###
The project time is not very long and falling behind on 
first weeks will put immense pressure to february. One 
of the group members has experience with django, but 
bootstrap is new to all members, thus its implementation 
may take more time than expected. Most crucial things to 
get right from the beginning are the database models. Most 
of the work relies on them and thus they finding problems 
in them at the last minutes can cause majoe haulovers 
across the board.

### 7. Report ###
481548 Aku Viitanen  
528375 Charlotta Alén  
426396 Antti Mella  
  
We were able to implement most of the basic functionality, but due to our busy schedules we didnt magane to implement proper security restrictions to all views(the test functions for it exist). Our most complete part is the authentication, which uses gmail to send out activation links. Our users can buy and play games, but the messaging interaction is unimplemented. Developers can add and delete games as well as see sales transactions log.

All of us worked on all the things but biggest responsibilities were:  
Aku - Authentication  
Antti - Developer tools  
Charlotta - Front end  

https://aqueous-brook-23280.herokuapp.com/ deployed version

