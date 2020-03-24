from graphviz import Digraph


def displaygraph(sim):
    real_tree_branch = sim.branch_node.branch_array[:-1]
    branch_array = sim.branch_node.ghost_array[:-1]
    result_array = sim.tree_state.ST_result_array
    number_array = sim.tree_state.ST_number_in_slot
    cot = Digraph(comment="Simple Tree", format='png')
    cot.attr(compound='true')
    cot.node('Start', label=str(number_array[0]), shape='doublecircle', xlabel=str(result_array[0]))
    # Create All Nodes
    for i in range(len(branch_array)):
        current_node = branch_array[i]
        current_result = str(result_array[i + 1])
        if current_node not in real_tree_branch:
            cot.node(current_node, label=str(number_array[i + 1]), xlabel=current_result, fillcolor='red',
                     style='filled')
        else:
            cot.node(current_node, label=str(number_array[i + 1]), xlabel=current_result)
        if len(current_node) == 0:
            print("Graphviz Error")
        elif len(current_node) == 1:
            cot.edge('Start', current_node, label=current_node)
    for i in range(len(branch_array)):
        for j in range(i + 1, len(branch_array)):
            fixed_node = branch_array[i]
            variable_node = branch_array[j]
            if variable_node[:-1] == fixed_node:
                cot.edge(fixed_node, variable_node, variable_node)
    cot.edge_attr.update(fontcolor='green')
    cot.render('Results/Result', view=True)
