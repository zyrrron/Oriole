import json


def parse_connections(json_data):
    edge_list = []
    for connection in json_data["connections"]:
        source_component = connection["source"]["component"]
        for sink in connection["sinks"]:
            sink_component = sink["component"]
            edge_list.append(f"{source_component}->{sink_component}")
    return edge_list


def save_edge_list(edge_list, file_path):
    with open(file_path, "w") as file:
        for edge in edge_list:
            file.write(edge + "\n")


def json_to_edgelist(input_json_file, output_edgelist_file):
    with open(input_json_file, "r") as file:
        json_data = json.load(file)

    edge_list = parse_connections(json_data)
    save_edge_list(edge_list, output_edgelist_file)


input_json_file = "flow_focus.json"
output_edgelist_file = "flow_focus_json.edgelist"

json_to_edgelist(input_json_file, output_edgelist_file)
