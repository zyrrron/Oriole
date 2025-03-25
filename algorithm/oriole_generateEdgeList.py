import argparse
import utils as ut
import sys
sys.path.append("../Oriole")


def generateEdgeList():
    # Parse the command line inputs
    parser = argparse.ArgumentParser(description="perform graph partition using metis")
    parser.add_argument("-settings", dest="settings", required=True, help="settings.txt", metavar="string")
    parser.add_argument("-samples", dest="samples", required=True, help="1,2", metavar="string")
    args = parser.parse_args()

    # Run the command
    samples = args.samples.split(',')
    settings = ut.load_settings(args.settings)

    for s in samples:
        print('sample ', s)
        graph_path = settings[s]['graph_path']
        JSON_file = graph_path + '/' + s + '.json'
        # load json file
        ports, gates = ut.read_json(JSON_file)
        ut.generateGateDict(gates, graph_path)
        ut.synthesize_graph(ports, gates, graph_path, t=10)


generateEdgeList()