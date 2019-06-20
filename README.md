Hello! This document includes the instructions and basic documentation for 
running this application.

There are four server implementations: a basic pure Python multithreaded server,
and SSL extension to that implementation, single threaded
Flask framework http implementation,and an WSGI single threaded http server.


[Instructions]:

    1) For help, in the command line from one level outside of the app 
       directory,
            
            ~$ python app -h

       This command displays the configurable command line options. The default
       settings are: 

            1 thread, WSGI server, and address localhost:5000

       A specific application configuration can be persisted by modifying the
       settings in the app/server/configuration.py configuration file.
 

    2) To run the main appilcation method in its default configuration, from one 
       level outside of the app directory
           
            ~$ python app


    3) The application behavior can be observed in the web browser with the 
       following endpoints (for the three non-SSL server implementations)

           a) http://localhost:5000
           b) http://localhost:5000/timestamp
           c) http://localhost:5000/undefined 

       The undefined endpoint is included for requirements verification. The SSL 
       self signed server implementation uses the same endpoints except prefixed 
       with https.


    4) This application optionally supports a Flask Server implementation. But
       Flask is not required as a dependency.


[Verification Test]:
With the server running, typing http://localhost:5000/timestamp, returns the
specified JSON to the web browser per the project requirements. Also, the top 
level endpoint "/" is configured to return the specified timestamp JSON, as 
well.


[Note SSL]:
For the SSL self signed server implementation, it is possible to generate a new 
cert.pem using the Python script pem.py provided in the app/server/cert 
directory. To generate a new cert.pem cd to that directory and run python pem.py 
to overwrite the existing cert.pem file.


[Interactive Session]:
This application can also be imported into an interactive session (although I 
am not sure why someone would since running the server locks the interactive 
interpreter!) In an interactive session, the Basic multithreaded http server 
implementation is provided. From one level immediately outside of the app 
directory, start a Python interactive session and import app. 

    >>> a = app.Basic(1); a.run()

The argument 1 represents the number of threads and is required. The recommended 
way for running this application, however, is from the system command line, as 
demonstrated above:
    
    ~$ python app
