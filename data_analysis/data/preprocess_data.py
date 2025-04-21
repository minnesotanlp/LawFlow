import json
### 0.1 Human data
with open("
    human_data = json.load(f)
human_step_per_project = {i: [] for i in range(1, 11, 1)}
for rec in human_data:
    scenario_id = rec['scenario_id']
    node = rec['current_step']
    if len(human_step_per_project[scenario_id]) == 0 or  human_step_per_project[scenario_id][-1] != node:
        human_step_per_project[scenario_id].append(node)