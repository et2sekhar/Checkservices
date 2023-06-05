from flask import Flask
import win32serviceutil
import win32service

app = Flask(__name__)

# Defining the home page of our site
@app.route("/")  # this sets the route to this page
def home():
	return "<h1>Each Time the Wind Blows!!!</h1>"  # some basic inline html

# name of the service to check
service_name = 'BluetoothUserService_f7d859'

# get the status of the service
service_status = win32serviceutil.QueryServiceStatus(service_name)[1]

# check the status of the service
if service_status == win32service.SERVICE_RUNNING:
    output1 = (f"The {service_name} service is running.")
elif service_status == win32service.SERVICE_STOPPED:
    output1 = (f"The {service_name} service is stopped.")
else:
    output1 = (f"The {service_name} service is in an unknown state.")


@app.route("/service")
def service():
    return output1

if __name__ == "__main__":
    app.run()
