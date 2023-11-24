#!/usr/bin/env python3

import xml.dom.minidom
import subprocess
import sys


def ping_host(hostname):
    # replace with your path to "ping" binary
    ping_bin = '/bin/ping'
    result = subprocess.Popen([ping_bin, '-c', '4', hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8'), result.returncode

def nmap(port, hostname):
    # replace with your path to "nmap.sh"
    nmap_script = '/path/to/nmap.sh'
    result = subprocess.Popen([nmap_script, port, hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8'), result.returncode

def process_host(node):
    hostname = node.getAttribute('HostName')
    port = node.getAttribute('Port')
    print(f"checking host: {hostname} on port: {port}")

    # ping host
    ping_output, ping_error, ping_status = ping_host(hostname)
    if '100% packet loss' in ping_output or ping_status != 0:
        print(f" host {hostname} is DOWN or UNREACHABLE")
    else:
        print(f"host {hostname} is UP")

        # perform nmap scan if host is up
        nmap_output, nmap_error, nmap_status = nmap_scan(port, hostname)
        print(f"nmap scan output: {nmap_output}")
        if nmap_status != 0:
            print(f"error in nmap scan: {nmap_error}")

def main(xml_path):
    try:
        DOMTree = xml.dom.minidom.parse(xml_path)
        collection = DOMTree.documentElement
        # process each host in XML file
        for database in collection.getElementsByTagName('Database')[0].childNodes:
            if database.nodeName.startswith("#"):
                continue
            for info in database.childNodes:
                if info.nodeName.startswith("#"):
                    continue
                process_host(info)
        # ...
    except Exception as e:
        print(f"error processing XML: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: detector.py <path_xml>")
        sys.exit(1)

    xml_path = sys.argv[1]
    main(xml_path)
