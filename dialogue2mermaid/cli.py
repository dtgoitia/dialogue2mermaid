from dialogue2mermaid.load import load_dialogue
from pprint import pprint as print


FALL_THROUGH = 'fallThrough'
END = -1
DIALOGUE_STOP = 'dialogue.stop'
SEPARATOR = "---------------------------------------------------------------------------"


def get_dialogue_nodes(dialogue: dict):
    data = dialogue.get('data')
    attributes = data.get('attributes')
    json_object = attributes.get('json')
    return json_object.get('nodes')


def unify_next_node_references(nodes: list):
    """
    Update the next node reference to a standard reference.
    - if no reference and no last node: FALLTHROUGH
    - if no reference and last node: END
    - if reference null: END
    Return the next node value(s).
    """
    for node in nodes:
        if 'nextNodeIndex' in node:
            node['next'] = node.pop('nextNodeIndex')
        elif 'nextNode' in node:
            node['next'] = node.pop('nextNode')
        elif 'passNode' in node and 'failNode' in node:
            node.update({'next': {
                'pass': node.pop('passNode'),
                'fail': node.pop('failNode'),
            }})
        elif 'passNodeIndex' in node and 'failNodeIndex' in node:
            node.update({'next': {
                'pass': node.pop('passNodeIndex'),
                'fail': node.pop('failNodeIndex'),
            }})
        else:
            i = node['index']
            if i == len(nodes) - 1:
                node.update({'next': END})      # last node
            else:
                node.update({'next': i + 1})    # fall to following node
        # update stop dialogue references to END
        current_ref = node['next']
        if current_ref is None or current_ref == DIALOGUE_STOP:
            node.update({'next': END})
    return nodes


def indexify_node_label_references(nodes: list):
    """
    Change "node label" type next references to indices
    """
    for node in nodes:
        next_node = node['next']
        if type(next_node) is str:
            for node2 in nodes:
                if node2.get('label') == next_node:
                    node.update({'next': node['index']})
                    break
            continue
        if type(next_node) is dict:
            next_node_pass = next_node['pass']
            next_node_fail = next_node['fail']
            if type(next_node_pass) is str:
                for node2 in nodes:
                    if node2.get('label') == next_node_pass:
                        next_node_pass = node2['index']
            if type(next_node_fail) is str:
                for node2 in nodes:
                    if node2.get('label') == next_node_fail:
                        next_node_fail = node2['index']
            node.update({'next': {
                'pass': next_node_pass,
                'fail': next_node_fail
            }})
    return nodes


def link_nodes(nodes: list) -> str:
    # Add indices to nodes
    for i, node in enumerate(nodes):
        node.update({'index': i})
    nodes = unify_next_node_references(nodes)
    nodes = indexify_node_label_references(nodes)
    return nodes


def beautify_nodes(nodes: list) -> list:
    """
    Customize each node content and return all nodes.
    Return each node data as a dictionary.
    """
    for node in nodes:
        node_type = node.get('type')
        if node_type == 'message':
            node.update({'content': 'print'})
        elif node_type == 'operation':
            node.update({'content': 'operation'})
        elif node_type == 'action':
            node.update({'content': 'action'})
        elif node_type == 'decision':
            node.update({'content': 'decision'})
        elif node_type == 'card':
            node.update({'content': 'card'})
        elif node_type == 'customCardCollection':
            node.update({'content': 'customCardCollection'})
        else:
            node.update({'content': 'NOT UNDERSTOOD'})
    return nodes


def stringify_nodes(nodes: list) -> list:
    """
    Convert node data to Mermaid syntax
    """
    result = ""
    for node in nodes:
        i = node['index']
        if 'label' in node:
            label = f"{i} @ {node['label']}, {node['type']}"
        else:
            label = f"{i} @ {node['type']}"
        content = node['content']
        ref = f"{node['index']} --> {node['next']}"
        result += f"{i}[\"{label} <br> {content}\"]\n{ref}\n"
    return result


def nodes_to_mermaid(nodes: list) -> str:
    linked_nodes = link_nodes(nodes)
    beautified_nodes = beautify_nodes(linked_nodes)
    stringified_nodes = stringify_nodes(beautified_nodes)
    return stringified_nodes


def write_to_markdown(mermaid: str):
    with open('output.md', 'w') as file:
        file.write('```mermaid {align="center"}\ngraph TB\n')
        file.write(mermaid)
        file.write('```')


def main():
    dialogue_path = 'test.jsonc'
    dialogue = load_dialogue(dialogue_path)
    nodes = get_dialogue_nodes(dialogue)
    mermaid = nodes_to_mermaid(nodes)
    write_to_markdown(mermaid)
