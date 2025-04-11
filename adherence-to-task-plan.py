import json
import statistics
import Levenshtein
from helper import llm_plan_idx_title, human_plan_node_list, llm_plan_node_list, llm_plan_map_human_plan

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
with open("data/llm_exec_llm_plan.json", "r") as f:
    llm_step_per_project = json.load(f)

##### 1. Node Exec Rate
### 1.1 Human exec Human plan
human_coverage = []
for scenario_id, step_list in human_step_per_project.items():
    coverage_dict  = {node: 0 for node in human_plan_node_list}
    for step in step_list: 
        coverage_dict[step] = 1
    coverage = sum(list(coverage_dict.values()))/len(coverage_dict.items())
    human_coverage.append(coverage)
human_mean = statistics.mean(human_coverage)
human_stdev = statistics.stdev(human_coverage) 

### 1.2 LLM exec LLM plan
llm_coverage = []
for scenario_id, exec_list in llm_step_per_project.items():
    llm_coverage_dict = {k: 0 for k in llm_plan_idx_title.keys()}
    llm_exec = llm_step_per_project[scenario_id]
    for step in llm_exec:
        llm_coverage_dict[step] = 1
    
    coverage =  sum(list(llm_coverage_dict.values()))/len(llm_coverage_dict.items())
    llm_coverage.append(coverage)
    
llm_mean = statistics.mean(llm_coverage)
llm_stdev = statistics.stdev(llm_coverage) 

### 
print(f"{'Node Execution Rate for Human Execution Human Plan:':60} M = {human_mean:.2f}, SD = {human_stdev:.2f}")
print(f"{'Node Execution Rate for LLM Execution LLM Plan:':60} M = {llm_mean:.2f}, SD = {llm_stdev:.2f}")

##### 2. Levenshtein dist
### 2.1 Human exec Human plan 
human_lev_dist = []
for scenario_id, human_seq in human_step_per_project.items():
    edit_operations = Levenshtein.editops(human_seq, human_plan_node_list)
    human_lev_dist.append(len(edit_operations))
    
human_mean = statistics.mean(human_lev_dist)
human_stdev = statistics.stdev(human_lev_dist) 

### 2.2 LLM exec LLM plan (before mapping)
llm_lev_dist_before = []
llm_lev_dist_after = []
for scenario_id, llm_seq_before in llm_step_per_project.items():
    # before mapping
    edit_operations_before = Levenshtein.editops(llm_seq_before, llm_plan_node_list)
    llm_lev_dist_before.append(len(edit_operations_before))
    
    # after mapping
    llm_seq_after = [llm_plan_map_human_plan[step] for step in llm_seq_before if step in llm_plan_map_human_plan]
    edit_operations_after = Levenshtein.editops(llm_seq_after, human_plan_node_list)
    llm_lev_dist_after.append(len(edit_operations_after))
    
llm_mean_before = statistics.mean(llm_lev_dist_before)
llm_stdev_before = statistics.stdev(llm_lev_dist_before) 
llm_mean_after = statistics.mean(llm_lev_dist_after)
llm_stdev_after = statistics.stdev(llm_lev_dist_after) 

### 
print(f"{'Levenshtein dist. for Human Execution Human Plan:':70} M = {human_mean:.2f}, SD = {human_stdev:.2f}")
print(f"{'Levenshtein dist. for LLM Execution LLM Plan (before mapping):':70} M = {llm_mean_before:.2f}, SD = {llm_stdev_before:.2f}")
print(f"{'Levenshtein dist. for LLM Execution LLM Plan (after mapping):':70} M = {llm_mean_after:.2f}, SD = {llm_stdev_after:.2f}")
