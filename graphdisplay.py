import matplotlib
from graphviz import Digraph

def displaygraph(branch_array, result_array, number_array):
    cot = Digraph(comment="Simple Tree", format='png')
    cot.attr(compound='true')
    cot.node('Start', label=str(number_array[0]), shape='doublecircle', xlabel=str(result_array[0]))
    # Create All Nodes
    for i in range(len(branch_array)):
        current_node = branch_array[i]
        current_result = str(result_array[i+1])
        cot.node(current_node, label=str(number_array[i+1]), xlabel=current_result)
        if len(current_node) == 0:
            print("Graphviz Error")
        elif len(current_node) == 1:
            cot.edge('Start', current_node, label=current_node)
        # else:
        #     prev_node = branch_array[i-1]
        #     if current_node[-2] == prev_node[-1]:
        #         cot.edge(prev_node, current_node)
    for i in range(len(branch_array)):
        for j in range(i+1, len(branch_array)):
            fixed_node = branch_array[i]
            variable_node = branch_array[j]
            if variable_node[:-1] == fixed_node:
                cot.edge(fixed_node, variable_node, variable_node)
    cot.render('Result', view=True)

