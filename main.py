import datetime
import sys, time
import json
from src.node_models import Node
from src.daemon import Daemon
from src.myria_runner import MyriaRunner

class MyriaDaemon(Daemon):
        def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
                super().__init__(pidfile, stdin, stdout, stderr)
                with open('configuration.json', 'r') as file:
                        config_data = json.load(file)

                # Access the 'nodes' array and print its contents
                nodes_data = config_data.get('nodes', [])
                nodes = []
                for node in nodes_data:
                        nodes.append(Node.from_json(node))
                self.myria_runner = MyriaRunner(nodes)

        def run(self):
                while True:
                        self.myria_runner.check_status()
                        time.sleep(15)
 
if __name__ == "__main__":
        daemon = MyriaDaemon('/tmp/daemon-myria.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print("Unknown command")
                        sys.exit(2)
                sys.exit(0)
        else:
                print("usage: %s start|stop|restart" % sys.argv[0])
                sys.exit(2)