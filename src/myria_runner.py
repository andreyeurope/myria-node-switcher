import array
from node_models import Node
import datetime
import subprocess
import time

class MyriaRunner:

    def __init__(self, nodes: array.array[Node]) -> None:
        self.nodes = nodes

    def check_status(self):
        print("Checking status for node")
        # process = subprocess.Popen(["myria-node", "--status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # stdout, stderr = process.communicate()
        # output = stdout.decode()
        output = "not running"

        if "not running" not in output.lower():
            print("The program is running")
            return
        
        nodeToRun = next((node for node in self.nodes if node.should_be_running(datetime.datetime.now())), None)

        if nodeToRun is None:
            print("No node to run at the moment. Continuing..")
            self.__stop_process()
            return
        
        self.__start_node(nodeToRun)

    def __start_node(node: Node):
        print("Starting node %s..." % (node.name))
        # node_process = subprocess.Popen(["myria-node", "--start"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        # node_process.communicate(input=(node.apiKey + "\n").encode())

    def __stop_process():
        print("Stopping the process")
        # subprocess.run(["myria-node", "--stop"])
        time.sleep(5)