def pretty_var(token: any) -> any:
    return token.get('var') if type(token) == dict else token


def beautified_decision_node(node: dict) -> str:
    decision = node['rule']
    rule = list(decision.keys())[0]
    left = pretty_var(decision[rule][0])
    right = pretty_var(decision[rule][1])
    return f"{str(left)} {rule} {str(right)}"


def beautified_operation_node(node: dict) -> str:
    operation = node['operation']
    result = ''

    if 'output' in node:
        result = f"{node['output']} = "

    if 'method' in operation:
        method = operation['method']
        method_name = method[1]
        if method_name in ('addItem', 'getItem', 'updateItem'):
            var = pretty_var(method[0])
            i = pretty_var(method[2][0])
            result += f"{var}.{method_name}({i})"
        else:
            str(operation['unrecognised method'])
    elif 'var' in operation:
        result += f"{operation['var']}"
    else:
        plugin_name = list(operation.keys())[0]
        p = [str(pretty_var(item)) for item in operation[plugin_name]]
        p = ', '.join(p)
        result += f"{plugin_name}({p})"

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
            node.update({'content': 'NOT UNDERSTOOD'})
    return nodes
