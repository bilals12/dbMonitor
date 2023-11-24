### dbMonitor

## overview
dbMonitor is designed to automate and manage the monitoring and maintenance of a test lab environment. it focuses on network and database host availability and health. the system integrates 4 scripts and a jenkins pipeline to ensure continuous monitoring, automated version control, and timely notifications in case of host downtime or issues. it's really useful in software testing, QA, or dev environments.

## components
the system comprises of 4 scripts and a config XML file.
1. `nmap.sh`: bash script for detailed network scanning. uses `nmap` to check specified ports on a given host.
2. `git_work.sh`: bash script for automatic git branch management. it compares local and remote branches and switches to the most appropriate (latest) branch based on a specific pattern. this component is ideal for sprint work.
3. `detector.py`: python script for pinging hosts and initiating network scans. reads host information from `config.xml` and checks each host's availability.
4. `config.xml`: XML config file that lists the details of databases and hosts to be monitored. you can add your hosts/dbs to this file so that the function can check for them.
5. `detector.jenkinsfile`: jenkins pipeline script that orchestrates the entire monitoring process, including git operations, script execution, and notifications.

## workflow
**initialization**: jenkins pipeline `detector.jenkinsfile` starts the process, cloning the necessary git repos and managing git branches using `git_work.sh`.

**monitoring execution**: pipeline runs `detector.py`, which pings hosts listed in `config.xml`. if a host is up but has connectivity issues, `nmap.sh` is used for a detailed network scan.

**notification**: in case of host downtime, the jenkins pipeline sends an email notification with details of unresponsive machines.

## benefits
- automated monitoring: ensures availability and health of test machines without manual intervention.
- integration with ci/cd: fits seamlessly into ci/cd workflows, enhancing software testing and dev processes.
- timely notifications: quick responses to host downtimes, minimizing disruptions in testing environment.
- version control management: keeps testing environment consistent with software versions.

## setup + configs
1. initial repo setup
- clone repo containing the scripts and config file.
- store repo in a location accessible to jenkins server and users who run the scripts.

2. configuring `config.xml`
- update the file with details of the db and hosts that need to be monitored. this includes hostnames, ports, and other relevant attributes.

3. script configuration
- update the path to the `nmap` binary in `nmap.sh` and the path to `nmap.sh` in `detector.py`.
- ensure scripts have execute permissions. set this using `chmod +x [script_name]`.

4. jenkins pipeline setup
- in jenkins, create a new job and select "pipeline" as the type.
- point pipeline to the repo where `detector.jenkinsfile` is located.
- if using the script directly in jenkins, copy contents of `detector.jenkinsfile` into the "pipeline script" field in the job configuration.
- configure necessary parameters as described in `detector.jenkinsfile`, including email address for the notifications, paths to the scripts, and the path to `config.xml`.
- securely add required creds (like git creds) to jenkins and reference them in the pipeline script.

5. testing setup
- test each script independently to ensure they work.
- manually trigger pipeline and verify each stage executes correctly and the overall workflow behaves as expected.
- ensure email notifications are being sent out correctly in case of host downtimes or issues.

6. scheduling + automation
- set up the job to run at regular intervals (whatever you decide).
- if you use `git_work.sh`, make sure it's set up to automatically switch to the correct branch based on your versioning strategy.

7. documentation + maintenance
- keep documentation of your config and any customizations made.
- regularly update and maintain the scripts, jenkins job, and XML config file to adapt to any environment changes!

## usage
1. `nmap.sh`
performs network scan on specified port + host
```bash
./nmap.sh [port] [host]
```
example:
```bash
$ ./nmap.sh 80 192.168.1.10
80/tcp open
```

2. `git_work.sh`
compares local and remote git branches and switches to most appropriate branch
```bash
./git_work.sh [branch_pattern]
```
example:
```bash
$ ./git_work.sh "4."
new sprint detected. switching branch to remotes/origin/4.10
```

3. `detector.py`
pings and checks availability of hosts listed in XML config file and performs additional network scans if necessary
```bash
python3 detector.py [path_to_XML]
```
example:
```python
$ python3 detector.py config.xml
Checking host: dbserver1.example.com on port: 5432
Host dbserver1.example.com is UP
Nmap Scan Output: 5432/tcp open

Checking host: webserver2.example.com on port: 80
Host webserver2.example.com is DOWN or UNREACHABLE

Checking host: appserver3.example.com on port: 8080
Host appserver3.example.com is UP
Nmap Scan Output: 8080/tcp filtered

```

4. `detector.jenkinsfile`
automates monitoring process, manages git operations, sends notifications
- set up in jenkins pipeline job
- configure necessary params like email address, git repo URL, paths
- trigger pipeline manually or set it up to run at scheduled intervals
example:
```scss
[Pipeline] stage
[Pipeline] { (Setup and Update Repos)
Cloning into 'scripts'...
Cloning into 'scripts/dbMonitor'...
...
[Pipeline] stage
[Pipeline] { (Monitor Hosts)
Running heartbeat script...
Host dbserver1.example.com is UP
...
[Pipeline] }
[Pipeline] // stage
...
[Pipeline] stage
[Pipeline] { (Notify)
Sending notification email...
}
[Pipeline] }
[Pipeline] // stage
```
example (failure):
```scss
[Pipeline] stage
[Pipeline] { (Monitor Hosts)
Running heartbeat script...
Host webserver2.example.com is DOWN or UNREACHABLE
...
[Pipeline] }
[Pipeline] // stage
...
[Pipeline] stage
[Pipeline] { (Notify)
Sending notification email...
Email sent to: your-email@example.com
}
[Pipeline] }
[Pipeline] // stage
```


