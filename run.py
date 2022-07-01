from app import app

import sys

if (len(sys.argv)>1):
    mode = sys.argv[1]
else:
    print("No mode argument, must pass a mode")
    exit()
    
if mode == "testing":
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif mode == "production":
    import bjoern
    print("Running in production mode!")
    bjoern.run(app, "0.0.0.0", 5000)
else:
    print("Invalid mode, must be one of: testing|production")
    exit() 

app.run(debug=True)