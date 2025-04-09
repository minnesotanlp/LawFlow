import networkx as nx
import json

### 1. Betweenness Centrality
node_type_tracking = {
    "note_taking": [
        "1. Gather basic information, discover any underlying complexities",
        '1.1.1 Take Notes',
        '1.1 Ask Default Questions',
        '1.2.1 Ask follow-up questions'
    ],
    "knowledge_gaps": [
        '1.2 Identify potential complications/follow-up questions',
        '1.3 Identify gaps in knowledge (#1)'
    ]
}

with open("data/human_exec_human_plan.json", "r") as f:
    human_data = json.load(f)
human_step_per_project = {i: [] for i in range(1, 11, 1)}
for rec in human_data:
    scenario_id = rec['scenario_id']
    node = rec['current_step']
    if len(human_step_per_project[scenario_id]) == 0 or  human_step_per_project[scenario_id][-1] != node:
        human_step_per_project[scenario_id].append(node)


bc_top_3_store = []
for scenario_id, step_list in human_step_per_project.items():
    transition_count = dict()
    n = len(step_list)
    for i in range(n-1):
        if step_list[i] in transition_count:
            if step_list[i+1] in transition_count[step_list[i]]:
                transition_count[step_list[i]][step_list[i+1]] += 1
            else:
                transition_count[step_list[i]][step_list[i+1]] = 1
        else:
            transition_count[step_list[i]] = dict()
            transition_count[step_list[i]][step_list[i+1]] = 1
    records = []
    for curr_step, dict_store in transition_count.items():
        for next_step, val in dict_store.items():
            records.append((curr_step, next_step, val))
    G = nx.DiGraph()
    for curr_step, next_step, val in records:
        G.add_edge(curr_step, next_step, weight=val)
    bc_directed = nx.betweenness_centrality(G, normalized=True)
    sorted_bc_directed = sorted(bc_directed.items(), key=lambda x: x[1], reverse=True)
    top_3_store = []
    for node, centrality in sorted_bc_directed:
        if len(top_3_store) < 3: 
            if centrality > 0.0:
                top_3_store.append(node)
    bc_top_3_store.append(top_3_store)
    
note_count_overall = 0
gaps_count_overall = 0
none_count_overall = 0
for scenario in bc_top_3_store:
    note_check = 0
    gaps_check = 0
    for node in scenario:
        if node in node_type_tracking["note_taking"]:
            note_check = 1
        if node in node_type_tracking["knowledge_gaps"]:
            gaps_check = 1
    note_count_overall += note_check
    gaps_count_overall += gaps_check
    if not note_check and not gaps_check:
        none_count_overall += 1

print(f"Out of 10 scenarios, note_taking nodes appear in top 3 for {note_count_overall} scenarios.")
print(f"Out of 10 scenarios, knowledge_gaps nodes appear in top 3 for {gaps_count_overall} scenarios.")
print(f"Out of 10 scenarios, both knowledge_gaps and note_taking nodes do not appear in top 3 for {none_count_overall} scenario.")