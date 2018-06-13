from dialogue2mermaid.load import load_dialogue
from pprint import pprint as print


FALL_THROUGH = 'fallThrough'


def get_dialogue_nodes(dialogue: dict):
    data = dialogue.get('data')
    attributes = data.get('attributes')
    json_object = attributes.get('json')
    return json_object.get('nodes')


def get_next_node(node: dict):
    """
    Return the value of the next node as is.
    Return 'fallThrough' string if no next node defined
    Return None if the next node is null
    """
    if 'nextNodeIndex' in node:
        return node.get('nextNodeIndex')
    elif 'nextNode' in node:
        return node.get('nextNode')
    elif 'passNode' in node and 'failNode' in node:
        return (node.get('passNode'), node.get('failNode'))
    elif 'passNodeIndex' in node and 'failNodeIndex' in node:
        return (node.get('passNodeIndex'), node.get('failNodeIndex'))
    else:
        return FALL_THROUGH


def process_node(node: dict, node_index: int) -> set:
    # print(str(node))
    node_type = node.get('type')
    node_label = node.get('id')
    result = {
        "ref": (node_label if node_label is not None else node_index),
        "index": node_index,
        "next_node": get_next_node(node)
    }
    if node_type == 'message':
        result.update({'content': 'print'})
    elif node_type == 'operation':
        result.update({'content': 'operation'})
    elif node_type == 'action':
        result.update({'content': 'action'})
    elif node_type == 'decision':
        result.update({'content': 'decision'})
    elif node_type == 'card':
        result.update({'content': 'card'})
    elif node_type == 'customCardCollection':
        result.update({'content': 'customCardCollection'})
    else:
        result.update({'content': 'NOT UNDERSTOOD'})
    return result


def link_node(current_node: dict, nodes: list):
    next_node = current_node['next_node']
    result = current_node.copy()
    if next_node is None:
        result.update({'next_node': 'END'})
    elif type(next_node) == int:
        pass
    elif type(next_node) == str:
        if next_node == FALL_THROUGH:
            result.update({'next_node': current_node['index'] + 1})
        else:
            for i, node in enumerate(nodes):
                if next_node == node['ref']:
                    result.update({'next_node': i})
                    break
    return result


def nodes_to_mermaid(nodes: list) -> str:
    round1 = []
    for i, node in enumerate(nodes):
        output = process_node(node, i)
        round1.append(output)
        print(f"{output['ref']} @ {output['content']} -> {output['next_node']}")
    round2 = []
    for node in round1:
        output = link_node(node, round1)
        round2.append(output)
    return round2
    # return str(round2)


def main():
    dialogue_path = 'test.jsonc'
    dialogue = load_dialogue(dialogue_path)
    nodes = get_dialogue_nodes(dialogue)
    mermaid = nodes_to_mermaid(nodes)
    print(mermaid)
