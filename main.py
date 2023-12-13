import os, time, logging, logging.handlers
import json
from src.node_models import Node
from src.myria_runner import MyriaRunner
 
if __name__ == "__main__":
        print("Start.")
        log_dir = "/mnt/c/Git/myria-node-switcher/"
        handler = logging.handlers.WatchedFileHandler(
                os.environ.get("LOGFILE", log_dir + "myria-runner.log"))
        formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s')
        handler.setFormatter(formatter)
        root = logging.getLogger()
        root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
        root.addHandler(handler)

        with open('config.json', 'r') as file:
                config_data = json.load(file)

        # Access the 'nodes' array and print its contents
        nodes_data = config_data.get('nodes', [])
        nodes = []
        for node in nodes_data:
                nodes.append(Node.from_dict(node))
        myria_runner = MyriaRunner(nodes)

        while True:
                myria_runner.check_status()
                time.sleep(15)
