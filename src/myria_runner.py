from src.node_models import Node
import datetime
import subprocess
import time
import logging

class MyriaRunner:

    def __init__(self, nodes):
        self.nodes = nodes

    def check_status(self):
        logging.info("Checking status for node")
        output = self.__check_myria_status()
        isProgramRunning = "not running" not in output.lower()
        nodeToRun = next((x for x in self.nodes if x.should_be_running(datetime.datetime.now())), None)
        anyNodeToRun = nodeToRun is not None

        if isProgramRunning and anyNodeToRun:
            logging.info("The program is running")
            return

        if isProgramRunning and not anyNodeToRun:
            logging.info("The program should stop")
            self.__stop_process()
            return

        if not isProgramRunning and not anyNodeToRun:
            logging.info("No node to run at the moment. Continuing..")
            return
        
        self.__start_node(nodeToRun)

    def __check_myria_status(self) -> str:
        process = subprocess.Popen(["myria-node", "--status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode()

    def __start_node(self, node: Node):
        logging.info("Starting node %s..." % (node.name))
        node_process = subprocess.Popen(["myria-node", "--start"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        node_process.communicate(input=(node.apiKey + "\n").encode())
        time.sleep(5)

    def __stop_process(self):
        logging.info("Stopping the process")
        subprocess.run(["myria-node", "--stop"])
        time.sleep(5)