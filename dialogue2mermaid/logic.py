UNRECOGNIZED_NODE = '( Ooops, not understood... yet :P )'
from pprint import pprint


def pretty_var(token: any) -> any:
    result = token.get('var') if type(token) == dict else token
    return "''''" if result == "" else result


def beautify_decision(decision: dict) -> str:
    name = list(decision.keys())[0]
    if name in ('and', 'or'):
        result = [f"({beautify_decision(item)})" for item in decision[name]]
        return f" {name} ".join(result)
    left = pretty_var(decision[name][0])
    right = pretty_var(decision[name][1])
    return f"{str(left)} {name} {str(right)}"


def beautified_decision_node(node: dict) -> str:
    decision = node['rule']
    return beautify_decision(decision)


def method_has_arguments(method: dict) -> bool:
    return True if len(method) > 2 else False


def beautify_method(method: dict) -> str:
    receiver = pretty_var(method[0])
    beautify_json_logic(method[0])
    name = method[1]
    if name in ('addItem', 'current', 'filter', 'getCount', 'getItem', 'indexOf', 'length', 'removeItem',
                'sort', 'split', 'updateItem'):
        if method_has_arguments(method):
            arguments = [pretty_var(arg) for arg in method[2]]
            return f"{receiver}.{name}({', '.join(arguments)})"
        else:
            return f"{receiver}.{name}()"
    else:
        return UNRECOGNIZED_NODE


def beautify_json_logic(json: any) -> str:
    # TODO
    # beautify_json_logic is not returning to anything.
    # See where is beautify_json_logic implemented and move all json logic into here

    # print("beautify_json_logic:")
    # pprint(json)
    # print("\n")
    if type(json) is not dict:
        return json
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
        return f"if {result}:<br>then: {true}<br>else: {false}"


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


def beautified_operation_node(node: dict) -> str:
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
            node.update({'content': beautified_operation_node(node)})
        elif node_type == 'action':
            node.update({'content': 'action'})
        elif node_type == 'decision':
            node.update({'content': beautified_decision_node(node)})
        elif node_type == 'card':
            node.update({'content': 'card'})
        elif node_type == 'customCardCollection':
            node.update({'content': 'customCardCollection'})
        else:
            node.update({'content': UNRECOGNIZED_NODE})
    return nodes
