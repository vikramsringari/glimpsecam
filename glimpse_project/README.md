# Web App Instructions 
## Version 1.0 upload 7/21/18
### Running Django Server
* In order to view the API you must have Django and Python environments installed on your terminal. Since we have not yet deployed the site you must view it on a local server in order to test the web page.
* Terminal commands are "python manage.py runserver" once you are in the file with the manage.py file and you have your Django environment running
##### Registration Process
*For the registration page*
  Make sure the user enters a real email address, and a device key that they will remember. They need both to sign in to their account later
  Logic has been installed making sure that a user cannot enter an invalid email, or the same email that has already been used.
  This is so the email address is unique and can be used as a username/sign in tool for the login page without running into errors.
##### Log In Process
*For the login page*
  Logic has been installed making it so you have to sign in with the correct email and device key number that you previously entered in atregistration page. 
##### God Mode Process
*For the "GodMode" page*
  The username is "Dylan Rose" and the password is "isourboss"
  This page is still incomplete but will eventually show information about each camera, battery life, images taken, videos taken, data used, etc.
  This page will also show a complete list of EVERY single image and video that has been taken, giving the admin in charge access to everything for testing purposes
### Things that still need to be done
* Connect the User Page and connect mode page to display the images that are in each user and the entire server
* Have both EventPage.HTML and godMode.html display images via for loops from the data base in a aesthetically pleasing fashion
* Make all html pages responsive to screen size 
* *@media only screen and (min-width: 1024px)* for desktop pages
* *@media only screen and (min-width: 481px)* for tablets
* *@media only screen and (max-width: 480px)* for mobile phones
