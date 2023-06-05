from flask import Flask, render_template, request, redirect, url_for
import win32serviceutil
import datetime
import socket
import platform

# Get the system Ip address and Computer name
ip_address = socket.gethostbyname(socket.gethostname())
computer_name = socket.gethostname()

# to get Operating system name and version
os_name = platform.system()
os_version = platform.version()

SERVICE_NAME = 'BluetoothUserService_f7d859'

# Get the service start time
try:
    service_info = win32serviceutil.QueryServiceStatus(SERVICE_NAME)
    print(service_info)
    start_time = service_info[8]  # Get the service start time from the service status tuple
    start_time = datetime.datetime.fromtimestamp(start_time)  # Convert the start time to a datetime object
    last_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')  # Format the start time as a string
except IndexError:
    last_start_time = 'Service has not been started yet'
except Exception as e:
    last_start_time = f'Error getting service start time: {str(e)}'

app = Flask(__name__)
#app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    status = get_service_status()
    return render_template('index.html',
                           status=status,
                           service=SERVICE_NAME,
                           last_start_time=last_start_time,
                           ip_address=ip_address,
                           computer_name=computer_name,
                           os_name=os_name,
                           os_version=os_version)

@app.route('/start', methods=['POST'])
def start_service():
    try:
        win32serviceutil.StartService(SERVICE_NAME)
        message = 'Service started successfully'
        #return render_template('index.html', status=status, service=SERVICE_NAME)
    except Exception as e:
        return 'Error starting service: {}'.format(str(e))
    return render_template('message.html', message=message, redirect_url='/')
@app.route('/stop', methods=['POST'])
def stop_service():
    try:
        win32serviceutil.StopService(SERVICE_NAME)
        status = get_service_status()
        return redirect(url_for("index"))
    except Exception as e:
        return 'Error stopping service: {}'.format(str(e))

def get_service_status():
    try:
        status = win32serviceutil.QueryServiceStatus(SERVICE_NAME)[1]
        return 'Running' if status == 4 else 'Stopped'
    except Exception as e:
        return 'Error getting service status: {}'.format(str(e))

if __name__ == '__main__':
    app.run(debug=True)
