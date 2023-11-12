""" The application is
Created on Nov 11, 2023
Run file of the application """

from search import createApp, systemInfo
from decouple import config as envar  # import the environment var
from time import localtime
# import pytz

print(f"[{systemInfo}] @ ", {localtime()})

# envi = 'dev' # UNCOMMENT this line to change to dev mode
envi = envar('ENVI', 'production') # COMMENT OUT this line to change to dev mode
match envi:

    case 'production':
        # for running gunicorn (in production)
        app = createApp()

    case _:
        # for dev
        if __name__ == '__main__':
            app = createApp()
            app.run(port=int(envar("PORT", 5500)),
                    debug=envar("DEBUG", True))