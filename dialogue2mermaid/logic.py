UNRECOGNIZED_NODE = '( Ooops, not understood... yet :P )'
LINE_MAX_LENGTH = 40
NEW_LINE = '<br>'
INDENTATION = '---'


def beautify_decision(decision: dict) -> str:
    name = list(decision.keys())[0]
    if name in ('and', 'or'):
        result = [f"({beautify_decision(item)})" for item in decision[name]]
        return f" {name} ".join(result)
    left = beautify_json_logic(decision[name][0])
    right = beautify_json_logic(decision[name][1])
    return f"{str(left)} {name} {str(right)}"


def beautify_decision_node(node: dict) -> str:
    decision = node['rule']
    return beautify_decision(decision)


def method_has_arguments(method: dict) -> bool:
    return True if len(method) > 2 else False


def beautify_method(method: dict) -> str:
    receiver = beautify_json_logic(method[0])
    method_name = method[1]
    if method_has_arguments(method):
        arguments = [beautify_json_logic(arg) for arg in method[2]]
        return f"{receiver}.{method_name}({', '.join(arguments)})"
    else:
        return f"{receiver}.{method_name}()"


def beautify_json_logic(json: any) -> str:
    if type(json) is not dict:
        return str(json) if type(json) is int else json
    name = list(json.keys())[0]
    args = json[name]
    if name == 'var':
        var_result = json.get('var') if type(json) == dict else json
        return "''''" if var_result == "" else var_result
    elif name in ('+', '-', '*', '/'):
        result = [str(beautify_json_logic(item)) for item in args]
        delimiter = f" {name} "
        result = delimiter.join(result)
        return f"({result})"
    elif name in ('>', '<', '>=', '<=', '==', '===', '!=', '!=='):
        result = [str(beautify_json_logic(item)) for item in args]
        return f"({result[0]} {name} {result[1]})"
    elif name == 'if':
        library = json[name]
        true = beautify_json_logic(library[1])
        false = beautify_json_logic(library[2])
        result = beautify_library(library[0])
        return f"if {result}:{NEW_LINE}then: {true}{NEW_LINE}else: {false}"


def beautify_library(operation: dict) -> str:
    name = list(operation.keys())[0]
    if name in ('+', '-', '*', '/'):
        return beautify_json_logic(operation)
    elif name in ('>', '<', '>=', '<=', '==', '===', '!=', '!=='):
        return beautify_json_logic(operation)
    elif name == 'if':
        return beautify_json_logic(operation)
    elif name in ('and', 'or'):
        return beautify_decision(operation)
    else:
        p = [str(beautify_json_logic(item)) for item in operation[name]]
        p = ', '.join(p)
        return f"{name}({p})"


def beautify_operation_node(node: dict) -> str:
    operation = node['operation']
    result = ''

    if 'output' in node:
        result = f"{node['output']} = "

    if 'method' in operation:
        result += beautify_method(operation['method'])
    elif 'var' in operation:
        result += f"{operation['var']}"
    else:
        result += beautify_library(operation)

    return result


def snip(s: str) -> str:
    return s if len(s) < LINE_MAX_LENGTH else (s[0:LINE_MAX_LENGTH] + '...')


def join_per_length(chunks: list) -> list:
    result = []
    line = ''
    for chunk in chunks:
        if len(chunk) + len(line) <= LINE_MAX_LENGTH:
            line += chunk + ' '
            continue
        result.append(line)
        line = chunk + ' '
    result.append(line)
    return result


def split_per_length(string: str) -> list:
    chunks = string.split(' ')
    if len(chunks) == 1:
        return snip(string)
    return NEW_LINE.join(join_per_length(chunks))


def beautify_message_node(node: dict) -> str:
    return split_per_length(node['message']).replace('\"', "''")


def dict_to_string(dictionary: dict, delimiter: str, indentation_level: int) -> str:
    """
    Return a dictionary as a string.

    Dictionary example:
    {
      "animals": {
        "a": "elephant",
        "b": {
            "b1": "dog",
            "b2": "cat"
        }
      },
      "human": "Bob"
    }

    Return:
    - animals:
    ---- a: elephant
    ---- b:
    ------- b1: dog
    ------- b2: cat
    - human: Bob
    """
    result = ''
    for key, value in dictionary.items():
        if type(value) is dict:
            ind = indentation_level * INDENTATION
            result += f"{NEW_LINE}{ind}- {key}:"
            result += dict_to_string(value, ': ', indentation_level + 1)
        else:
            ind = indentation_level * INDENTATION
            result += f"{NEW_LINE}{ind}- {key}{delimiter}{value}"
    return result


def beautify_action_node(node: dict) -> str:
    service = node['service']
    result = ''
    if 'method' in service:
        result += f"{service['method']} "
    result += snip(service['url'])
    if 'headers' in service:
        result += f"{NEW_LINE}headers:{dict_to_string(service['headers'], ': ', 0)}"
    if 'body' in service:
        result += f"{NEW_LINE}body:{dict_to_string(service['body'], ': ', 0)}"
    if 'outputs' in node:
        result += f"{NEW_LINE}OUTPUTS:"
        outputs = node['outputs']
        if 'header' in outputs:
            result += f"{NEW_LINE}header:{dict_to_string(outputs['header'], ' = ', 0)}"
        if 'body' in outputs:
            result += f"{NEW_LINE}body:{dict_to_string(outputs['body'], ' = ', 0)}"
    return result


def beautify_prompt_node(node: dict) -> str:
    result = f"{node['output']} = {node['message']}"
    if 'validation' in node:
        result += f"{NEW_LINE}validation: {beautify_json_logic(node['validation'])}"
    if 'contentTypes' in node:
        result += f"{NEW_LINE}contentTypes: {', '.join(node['contentTypes'])}"
    return result


def beautify_event_node(node: dict) -> str:
    return node['event']


def loop_node_inputs(inputs: dict) -> str:
    result = f"{NEW_LINE}INPUTS:"
    for key, value in inputs.items():
        result += f"{NEW_LINE}{key} → {beautify_json_logic(value)}"
    return result


def loop_node_outputs(outputs: dict) -> str:
    result = f"{NEW_LINE}OUTPUTS:"
    for key, value in outputs.items():
        result += f"{NEW_LINE}{key} ← {beautify_json_logic(value)}"
    return result


def beautify_repeat_dialogue_node(node: dict) -> str:
    result = f"repeat '{node['dialogueId']}'"
    if 'repeatUntil' in node:
        result += f" until {beautify_json_logic(node['repeatUntil'])}"
    if 'inputs' in node:
        result += loop_node_inputs(node['inputs'])
    if 'outputs' in node:
        result += loop_node_outputs(node['outputs'])
    return result


def beautify_sequence_dialogue_node(node: dict) -> str:
    result = f"repeat '{node['dialogueId']}'"
    if 'listName' in node:
        result += f"{NEW_LINE}for every {node['inputItem']} in {node['listName']}"
    if 'inputs' in node:
        result += loop_node_inputs(node['inputs'])
    if 'outputs' in node:
        result += loop_node_outputs(node['outputs'])
    return result


def beautify_nodes(nodes: list) -> list:
    """
    Customize each node content and return all nodes.
    Return each node data as a dictionary.
    """
    for node in nodes:
        node_type = node.get('type')
        if node_type == 'action':
            node.update({'content': beautify_action_node(node), 'shape': 'square'})
        elif node_type in ('card', 'cardCollection', 'customCardCollection'):
            node.update({'content': 'card', 'shape': 'asymetric'})
        elif node_type == 'decision':
            node.update({'content': beautify_decision_node(node), 'shape': 'rhombus'})
        elif node_type == 'downloadAction':
            node.update({'content': beautify_action_node(node), 'shape': 'square'})
        elif node_type == 'event':
            node.update({'content': beautify_event_node(node), 'shape': 'square'})
        elif node_type == 'message':
            node.update({'content': beautify_message_node(node), 'shape': 'round'})
        elif node_type == 'operation':
            node.update({'content': beautify_operation_node(node), 'shape': 'square'})
        elif node_type == 'repeatDialogue':
            node.update({'content': beautify_repeat_dialogue_node(node), 'shape': 'square'})
        elif node_type == 'sequenceDialogue':
            node.update({'content': beautify_sequence_dialogue_node(node), 'shape': 'square'})
        elif node_type in ('stringPrompt', 'numberPrompt', 'confirmationPrompt', 'choicePrompt', 'datePrompt',
                           'timePrompt', 'dateTimePrompt', 'attachmentPrompt'):
            node.update({'content': beautify_prompt_node(node), 'shape': 'square'})
        else:
            node.update({'content': UNRECOGNIZED_NODE, 'shape': 'square'})
    return nodes
