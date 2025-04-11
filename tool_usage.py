import json

tool_group_map = {
    'notes_change': 'note_taking',
    'notes_paste': 'note_taking',
    'document_content_change': 'document_writing',
    'document_paste': 'document_writing',
    'upload_files': 'upload_files',
    'download_files': 'download_files',
    'vector_search': 'vector_search',
    'browser_search': 'broswer_search'
}
tool_group = ['note_taking', 'document_writing', 'upload_files', 'download_files', 'vector_search', 'broswer_search']

with open("data/human_exec_human_plan.json", "r") as f:
    human_data = json.load(f)
human_action_per_project = {i: [] for i in range(1, 11, 1)}

for rec in human_data:
    scenario_id = rec['scenario_id']
    action = rec['action']
    if len(human_action_per_project[scenario_id]) == 0 or  human_action_per_project[scenario_id][-1] != action:
        human_action_per_project[scenario_id].append(action)

tool_usage_overall = {group: [] for group in tool_group}
for scenario_id, action_list in human_action_per_project.items():
    tool_usage = {group: 0 for group in tool_group}
    temp = None
    for action in action_list:
        if action in tool_group_map:
            if tool_usage[tool_group_map[action]] == 0 or tool_group_map[action] != temp: 
                tool_usage[tool_group_map[action]] += 1
                temp = tool_group_map[action]
        else: 
            temp = None
    for group, value in tool_usage.items():
        tool_usage_overall[group].append(value)

for group, usage_list in tool_usage_overall.items():
    num_scenario = sum(1 for usage in usage_list if usage != 0)
    total_usage = sum(usage for usage in usage_list if usage != 0)
    mean_usage = total_usage/num_scenario if num_scenario != 0 else 0
    print(f"{group}: (avg use, num scenario) = ({mean_usage:.2f}, {num_scenario})")        
    