import re


def parse_dot_file(file_path):
    edges = []
    with open(file_path, 'r') as file:
        content = file.read()

        pattern = re.compile(r'(\w+) -> (\w+)')
        matches = pattern.findall(content)

        for match in matches:
            edges.append(f"{match[0]}->{match[1]}")

    return edges


def save_edge_list(edges, output_file_path):
    with open(output_file_path, 'w') as file:
        for edge in edges:
            file.write(f"{edge}\n")


input_file_1 = 'flow_focus.dot'

edges1 = parse_dot_file(input_file_1)

output_file_1 = 'flow_focus.edgelist'

save_edge_list(edges1, output_file_1)

print(f"Edge list for {input_file_1}:")
print("; ".join(edges1))
