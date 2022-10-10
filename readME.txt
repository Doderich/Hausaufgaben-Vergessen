This is a GUI Application to log forgotten homework and send automated emails to Parents.
This project is as of yet completly written in python and uses the PYQT6 framework to create the GUI.
I have the ampition to also create a Webapplication, but this will take time.

Right now the current concept is the following:

The GUI file builds only the viusal of the UI and the the other btn files mange the Events fiered from the User.
The connection to the Database is handeled by db_connect.py which connects to a database. It sends SQL querys and returns the Value to the UI functions.

The automated email service is already possible but currently not impleted because it would spam my emails.

The confg.ini file referenced in the code is not avalable on the public reposetorie because my lgoin Information is stored there :P

Hopfluy this gave a overview over my project :D
