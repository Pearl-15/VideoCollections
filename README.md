# VideoCollections
Django-Ajax full-stack web application. 

This application is a Django full-stack web application. It includes the Ajax to call the youtube API to search the Top-5 videos based on user input that need to type in the 'Search'.

It is a video collections application where you can search your favourite youtube videos and save them in a folder so you can go in anytime to see your saved video and watch anytime. 


# How To Run the Application
(1) clone this project
(2) create a '.env' file and paste your own youtube API Key on it, you may refer to the '.env.example' file to do it.
(3) cd to the project directory and type this comment in the terminal to run the application >>> 
'python manage.py runserver'

Now you can see the landing page

# How to Use the Application
(1) please 'Sign Up', upon 'Sign Up' completion you will be redirected to the 'Login' page

(2) please 'Log In'

(3) click on the 'Create Folder For Your Favourite Videos' button and put the 'Title' of the folder and click the 'Create' button

(4) click the 'Add Video' button, you may now start to add the video.

(5) you may paste the youtube video URL or you can search for the video. Here Ajax will send a request to youtube API and send back a response of the top 5 videos, you can click on the video to view or click on the full width to see the full width.

(6) click the 'Add' button under your favourite video.

(7) you can 'Delete' the video if you want to remove it from the folder

(8) on the Nav Bar at the top right corner there is a 'Dashboard' nav link. By clicking that you can see all of the Video Folders with videos that you have created. 

