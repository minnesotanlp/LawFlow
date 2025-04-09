import json
import statistics
from collections import Counter

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

### 0.2 LLM (OpenAI o1) data
with open("data/llm_cot_exec_human_plan_o1.json", "r") as f:
    llm_step_per_project_o1 = json.load(f)
    
### 0.3 LLM (DeepSeek R1) data
with open("data/llm_cot_exec_human_plan_r1.json", "r") as f:
    llm_step_per_project_r1 = json.load(f)
    

#### 1. Match Rate of Business Entity Formation
human_output = {1: "C-corp", 2: "nonprofit", 3: "need more information to determine", 4: "LLC", 5:"LLC", 6:"LLC", 7:"LLC", 8:"LLC", 9:"LLC", 10:"need more information to determine"}
o1_output = {1: "LLC", 2: "nonprofit", 3: "LLC", 4: "LLC", 5:"LLC", 6:"LLC", 7:"LLC", 8:"LLC", 9:"LLC", 10:"Professional LLC"}
r1_output = {1: "LLC", 2: "nonprofit", 3: "LLC", 4: "LLC", 5:"LLC", 6:"C-Corp", 7:"LLC", 8:"LLC", 9:"LLC", 10:"LLC"}

o1_rate = sum(1 for i in range(1, 11, 1) if human_output[i] == o1_output[i])/10
r1_rate = sum(1 for i in range(1, 11, 1) if human_output[i] == r1_output[i])/10

print(f"{'Match Rate of Business Entity Formation for OpenAI o1:':60} {o1_rate}")
print(f"{'Match Rate of Business Entity Formation for DeepSeek R1:':60} {r1_rate}")

#### 2. Intra - Coverage
### 2.1 Human 
human_coverage = {str(subtask): [] for subtask in range(1, 6, 1)}
for scenario_id, step_list in human_step_per_project.items():
    node_coverage_dict  = {node: 0 for node in human_plan_node_list}
    for step in step_list: 
        node_coverage_dict[step] = 1
    subtask_coverage_dict = {str(subtask): [] for subtask in range(1, 6, 1)}
    for node in human_plan_node_list:
        subtask_coverage_dict[node[0]].append(node_coverage_dict[node])
        
    for subtask in human_coverage: 
        human_coverage[subtask].append(sum(subtask_coverage_dict[subtask])/len(subtask_coverage_dict[subtask]))

### 2.2 LLM (OpenAI o1)
llm_coverage_o1 = {str(subtask): [] for subtask in range(1, 6, 1)}
for scenario_id, step_list in llm_step_per_project_o1.items():
    node_coverage_dict  = {node: 0 for node in human_plan_node_list}
    for step in step_list: 
        node_coverage_dict[step] = 1
    subtask_coverage_dict = {str(subtask): [] for subtask in range(1, 6, 1)}
    for node in human_plan_node_list:
        subtask_coverage_dict[node[0]].append(node_coverage_dict[node])
        
    for subtask in llm_coverage_o1: 
        llm_coverage_o1[subtask].append(sum(subtask_coverage_dict[subtask])/len(subtask_coverage_dict[subtask]))

### 2.3 LLM (DeepSeek R1)
llm_coverage_r1 = {str(subtask): [] for subtask in range(1, 6, 1)}
for scenario_id, step_list in llm_step_per_project_r1.items():
    node_coverage_dict  = {node: 0 for node in human_plan_node_list}
    for step in step_list: 
        node_coverage_dict[step] = 1
    subtask_coverage_dict = {str(subtask): [] for subtask in range(1, 6, 1)}
    for node in human_plan_node_list:
        subtask_coverage_dict[node[0]].append(node_coverage_dict[node])
        
    for subtask in llm_coverage_r1: 
        llm_coverage_r1[subtask].append(sum(subtask_coverage_dict[subtask])/len(subtask_coverage_dict[subtask]))

###
label_map = {"Human": human_coverage, "LLM (OpenAI o1) CoT": llm_coverage_o1, "LLM (DeepSeek R1) CoT": llm_coverage_r1}
for label in label_map:
    print(f"Subtask Coverage for {label} Exec Human Plan")
    for subtask, store in label_map[label].items():
        mean = statistics.mean(store)
        stdev = statistics.stdev(store)
        print(f"{f"Subtask {subtask}":20} M = {mean:.2f}, SD = {stdev:.2f}")
        
##### 3. Inter - Longest Common Sequence

### 3.1 Human
human_subtask_seq = []
for scenario_id, step_list in human_step_per_project.items():
    subtask_seq = []
    temp = ""
    for step in step_list:
        if len(subtask_seq) == 0 or step[0] != temp:
            subtask_seq.append(step[0])
            temp = step[0]
    human_subtask_seq.append(subtask_seq)

human_subtask_seq_prob = dict()
for seq_len in range(2, 6, 1):
    store_temp = []
    for val in human_subtask_seq: 
        store_temp.append(tuple(val[:seq_len]))
        counter = Counter(store_temp)
        divided_counter = {k: v / 10 for k, v in counter.items()}
    human_subtask_seq_prob[seq_len] = divided_counter

### 3.2 LLM (OpenAI o1)
llm_subtask_seq_o1 = []
for scenario_id, step_list in llm_step_per_project_o1.items():
    subtask_seq = []
    temp = ""
    for step in step_list:
        if len(subtask_seq) == 0 or step[0] != temp:
            subtask_seq.append(step[0])
            temp = step[0]
    llm_subtask_seq_o1.append(subtask_seq)

llm_subtask_seq_prob_o1 = dict()
for seq_len in range(2, 6, 1):
    store_temp = []
    for val in llm_subtask_seq_o1: 
        store_temp.append(tuple(val[:seq_len]))
        counter = Counter(store_temp)
        divided_counter = {k: v / 10 for k, v in counter.items()}
    llm_subtask_seq_prob_o1[seq_len] = divided_counter
    
### 3.2 LLM (DeepSeek R1)
llm_subtask_seq_r1 = []
for scenario_id, step_list in llm_step_per_project_r1.items():
    subtask_seq = []
    temp = ""
    for step in step_list:
        if len(subtask_seq) == 0 or step[0] != temp:
            subtask_seq.append(step[0])
            temp = step[0]
    llm_subtask_seq_r1.append(subtask_seq)

llm_subtask_seq_prob_r1 = dict()
for seq_len in range(2, 6, 1):
    store_temp = []
    for val in llm_subtask_seq_r1: 
        store_temp.append(tuple(val[:seq_len]))
        counter = Counter(store_temp)
        divided_counter = {k: v / 10 for k, v in counter.items()}
    llm_subtask_seq_prob_r1[seq_len] = divided_counter

### 
label_map = {"Human": human_subtask_seq_prob, "LLM (OpenAI o1) CoT": llm_subtask_seq_prob_o1, "LLM (DeepSeek R1) CoT": llm_subtask_seq_prob_r1}
ord_map = {"Human": 3, "LLM (OpenAI o1) CoT": 5, "LLM (DeepSeek R1) CoT": 5}

for label in label_map:
    print(f"Longest Common Sequence for {label} Exec Human Plan")
    for seq_len in range(2, ord_map[label]+1, 1):
        # print(f"Sequence Length = {seq_len}:")
        max_seq, max_prob = max(label_map[label][seq_len].items(), key=lambda x: x[1])
        print(f"{f"{max_seq}":30}: {max_prob}")
