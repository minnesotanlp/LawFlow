import networkx as nx
import json
import statistics
from helper import human_plan_node_list, human_plan_idx_title, human_plan_idx2title
##### 0. Process data
### 0.1 Human data
with open("data/human_exec_human_plan.json", "r") as f:
    human_data = json.load(f)
human_step_per_project = {i: [] for i in range(1, 11, 1)}
for rec in human_data:
    scenario_id = rec['scenario_id']
    node = rec['current_step']
    if len(human_step_per_project[scenario_id]) == 0 or  human_step_per_project[scenario_id][-1] != node:
        human_step_per_project[scenario_id].append(node)

### 0.2 LLM data
with open("data/llm_cot_exec_human_plan_o1.json", "r") as f:
    llm_step_per_project = json.load(f)

##### 1. Number of cycles 
### 1.1 Human
human_cycle = []
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
    G_human = nx.DiGraph()
    for curr_step, next_step, val in records:
        G_human.add_edge(curr_step, next_step, weight=val)
        cycles = nx.simple_cycles(G_human, length_bound=6)
        num_cycles = sum(1 for cycle in cycles if len(cycle) > 2)
    human_cycle.append(num_cycles)

human_mean = statistics.mean(human_cycle)
human_stdev = statistics.stdev(human_cycle)

### 1.2 LLM
llm_cycle = []
for scenario_id, step_list in llm_step_per_project.items():
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
    G_human = nx.DiGraph()
    for curr_step, next_step, val in records:
        G_human.add_edge(curr_step, next_step, weight=val)
        cycles = nx.simple_cycles(G_human, length_bound=6)
        num_cycles = sum(1 for cycle in cycles if len(cycle) > 2)
    llm_cycle.append(num_cycles)

llm_mean = statistics.mean(llm_cycle)
llm_stdev = statistics.stdev(llm_cycle)

print(f"{'Number of Cycles for Human Execution Human Plan:':60} M = {human_mean:.2f}, SD = {human_stdev:.2f}")
print(f"{'Number of Cycles for LLM CoT Execution Human Plan:':60} M = {llm_mean:.2f}, SD = {llm_stdev:.2f}")


##### 2. Visit count 
### 2.1 Human 
visit_count_dict  = {node: 0 for node in human_plan_node_list}
human_visit_count = []

for scenario_id, step_list in human_step_per_project.items():
    human_visit_count_temp = visit_count_dict.copy()
    for step in step_list: 
        human_visit_count_temp[step] += 1
    non_zero_values = [v for v in human_visit_count_temp.values() if v != 0]
    visit_count = sum(non_zero_values)/len(non_zero_values)
    human_visit_count.append(visit_count)

human_mean = statistics.mean(human_visit_count)
human_stdev = statistics.stdev(human_visit_count) 

### 2.2 LLM
# llm_visit_count_per_project = {i: visit_count_dict.copy() for i in range (1, 11, 1)}
llm_visit_count = []

for scenario_id, step_list in llm_step_per_project.items():
    llm_visit_count_temp = visit_count_dict.copy()
    for step in step_list: 
        llm_visit_count_temp[step] += 1

    non_zero_values = [v for v in llm_visit_count_temp.values() if v != 0]
    visit_count = sum(non_zero_values)/len(non_zero_values)
    llm_visit_count.append(visit_count)

llm_mean = statistics.mean(llm_visit_count)
llm_stdev = statistics.stdev(llm_visit_count) 

###
print(f"{'Visit Count for Human Execution Human Plan:':60} M = {human_mean:.2f}, SD = {human_stdev:.2f}")
print(f"{'Visit Count for LLM CoT Execution Human Plan:':60} M = {llm_mean:.2f}, SD = {llm_stdev:.2f}")

##### 3. Subtask transition 
### 3.1 Human 
human_subtask_transition = []
for scenario_id, step_list in human_step_per_project.items():
    subtask_transition = 0
    temp = ""
    for step in step_list:
        if subtask_transition == 0 or step[0] != temp:
            subtask_transition += 1
            temp = step[0]
    human_subtask_transition.append(subtask_transition)
human_mean = statistics.mean(human_subtask_transition)
human_stdev = statistics.stdev(human_subtask_transition) 

### 3.2 LLM
llm_subtask_transition = []
for scenario_id, step_list in llm_step_per_project.items():
    subtask_transition = 0
    temp = ""
    for step in step_list:
        if subtask_transition == 0 or step[0] != temp:
            subtask_transition += 1
            temp = step[0]
    llm_subtask_transition.append(subtask_transition)

llm_mean = statistics.mean(llm_subtask_transition)
llm_stdev = statistics.stdev(llm_subtask_transition) 

###
print(f"{'Subtask Transition for Human Execution Human Plan:':60} M = {human_mean:.2f}, SD = {human_stdev:.2f}")
print(f"{'Subtask Transition for LLM CoT Execution Human Plan:':60} M = {llm_mean:.2f}, SD = {llm_stdev:.2f}")

##### 4. Node execution rate
### 4.1 Human
human_coverage = []
for scenario_id, step_list in human_step_per_project.items():
    coverage_dict  = {node: 0 for node in human_plan_node_list}
    for step in step_list: 
        coverage_dict[step] = 1
    coverage = sum(list(coverage_dict.values()))/len(coverage_dict.items())
    human_coverage.append(coverage)

human_mean = statistics.mean(human_coverage)
human_stdev = statistics.stdev(human_coverage) 

### 4.2 LLM
llm_coverage = []
for scenario_id, step_list in llm_step_per_project.items():
    coverage_dict  = {node: 0 for node in human_plan_node_list}
    for step in step_list: 
        coverage_dict[step] = 1
    coverage = sum(list(coverage_dict.values()))/len(coverage_dict.items())
    llm_coverage.append(coverage)

llm_mean = statistics.mean(llm_coverage)
llm_stdev = statistics.stdev(llm_coverage) 
###
print(f"{'Node Execution Rate for Human Execution Human Plan:':60} M = {human_mean:.2f}, SD = {human_stdev:.2f}")
print(f"{'Node Execution Rate for LLM CoT Execution Human Plan:':60} M = {llm_mean:.2f}, SD = {llm_stdev:.2f}")
