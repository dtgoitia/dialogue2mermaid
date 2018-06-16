import os
import webbrowser
import click
from dialogue2mermaid.load import load_dialogue
from dialogue2mermaid.logic import beautify_nodes
from dialogue2mermaid.mermaid import mermaid_to_html
# from pprint import pprint as print


END = -1
DIALOGUE_STOP = 'dialogue.stop'


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
                if node2.get('id') == next_node:
                    node.update({'next': node2['index']})
                    break
            continue
        if type(next_node) is dict:
            next_node_pass = next_node['pass']
            next_node_fail = next_node['fail']
            if type(next_node_pass) is str:
                for node2 in nodes:
                    if node2.get('id') == next_node_pass:
                        next_node_pass = node2['index']
            if type(next_node_fail) is str:
                for node2 in nodes:
                    if node2.get('id') == next_node_fail:
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


def get_ref(node: dict) -> str:
    i = node['index']
    ref = node['next']
    if ref == END:
        return ''
    if type(ref) == dict:
        # it's decision node
        return f"{i} -->|PASS| {ref['pass']}\n{i} -->|FAIL| {ref['fail']}"
    else:
        return f"{i} --> {ref}"


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
        ref = get_ref(node)
        result += f"{i}[\"{label} <br> {node['content']}\"]\n{ref}\n"
    return result


def nodes_to_mermaid(nodes: list) -> str:
    linked_nodes = link_nodes(nodes)
    beautified_nodes = beautify_nodes(linked_nodes)
    stringified_nodes = stringify_nodes(beautified_nodes)
    return stringified_nodes


def write_to_file(output_path: str, mermaid: str):
    with open(output_path, 'w') as file:
        file.write(mermaid_to_html(mermaid))


@click.command()
@click.option('--input', '-i', default='input.json', help='JSON dialogue relative path')
@click.option('--output', '-o', default='index.html', help='Output HTML file')
@click.option('--browser/--no-browser', '-b/-nb', default=False, help='Open output in browser')
@click.option('--watch/--no-watch', '-w/-nw', default=False, help='Watch input file and reload')
def main(input, output, watch, browser):

    if watch != 0:
        print('Watch option is not available yet')
        return None

    dialogue = load_dialogue(input)
    nodes = get_dialogue_nodes(dialogue)
    mermaid = nodes_to_mermaid(nodes)
    write_to_file(output, mermaid)

    if browser:
        webbrowser.open(f"file://{os.path.realpath(output)}", new=2)
