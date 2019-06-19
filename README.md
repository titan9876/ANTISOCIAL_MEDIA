# ANTISOCIAL_MEDIA
For those of us that don't fit the normal social requirements of society

Last Update: 4/15/2019 by MDG
*****************************************************************************************************************
You can use this command set to take care of all of the installs and configurations at once:

for package in "Flask flask-wtf flask-sqlalchemy flask-bcrypt flask-login Pillow"; do pip install $package; done

#change directory to package location:
The program should run fine from ASM_Project Directory by running: python antisocial_media.py

However, you can also run the engine separately or add the flask engine to /etc/init.d (rc.d)
To run it:
	#cd to application home directory and type:
	# export FLASK_APP=antisocial_media.py
	# export FLASK_DEBUG=1 for DEV. (Allows Server to Continue Running and provides debug info.)
	#		Turn off Debug for PROD use. ('export FLASK_DEBUG=0')
	# flask run
******************************************************************************************************************

Requirements: 
1. If flask isn't installed, you can run: pip install Flask
2. You will need to have flask-wtf installed as well for form data: pip install flask-wtf
3. This code is using SqlAlchemy for data storage: pip install flask-sqlalchemy
4. Passwords are encrypted using Flask-Bcrypt to install: pip install flask-bcrypt
5. Login Validation uses flask-login. To install: pip install flask-login
6. Images are sized down to speed up processing using Pillow: pip install Pillow
