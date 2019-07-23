#python3

# import variables
import os, subprocess, time, json, logging

# Vacuum cleaner for closed application and desktop containers 
while True:
    dockerPs = 'docker ps --format "{{ json .}}" | jq --slurp .'
    X = subprocess.check_output(dockerPs, shell=True).decode('utf-8')
    data = json.loads(str(X))
    time.sleep(30)

    for i in range(0, len(data)):
        if data[i]['Names'].startswith('vcd-'):
            if "seconds" not in data[i]['RunningFor']:
                # check for application containers
                if data[i]['Names'].count('-') > 1:
                    activeSSHString = 'docker exec ' + data[i]['Names'] + ' ps aux | egrep "[s]shd: "'
                    if os.system(activeSSHString):
                        logging.warning("deleting: " + data[i]['Names'])
                        os.system("docker rm -f " + data[i]['Names'])

                # check for desktop containers
                else:
                    activeSessionString = "docker exec " + data[i]['Names'] + " ps -ef h | grep xrdp"
                    activeSession = subprocess.check_output(activeSessionString, shell=True)
                    if not "Xorg" in str(activeSession):
                        logging.warning("deleting: " + data[i]['Names'])
                        os.system("docker container rm -f " + data[i]['Names'])

