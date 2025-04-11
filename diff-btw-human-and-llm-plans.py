import statistics

# Data obtained from analyzing the human plan diagram and llm generated plan
# human plan diagram and llm generated plan is available under /data
human_tree_depth_per_subtask = [3, 3, 4, 4, 4]
llm_tree_depth_per_subtask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

human_num_branch_per_subtask = [4, 8, 2, 4, 6]
llm_num_branch_per_subtask = [4, 4, 4, 4, 3, 4, 3, 4, 4, 4]

human_num_node_per_subtask = [8, 13, 6, 9, 8]
llm_num_node_per_subtask = [4, 4, 4, 4, 3, 4, 3, 4, 4, 4]

llm_num_subtask = 10
human_num_subtask = 5

# 1. Tree Depth 
human_mean = statistics.mean(human_tree_depth_per_subtask)
human_stdev = statistics.stdev(human_tree_depth_per_subtask)

llm_mean = statistics.mean(llm_tree_depth_per_subtask)
llm_stdev = statistics.stdev(llm_tree_depth_per_subtask)

print(f"{'Tree Depth for Human Plan:':40} M = {human_mean:.1f}, SD = {human_stdev:.1f}")
print(f"{'Tree Depth for LLM Plan:':40} M = {llm_mean:.1f}, SD = {llm_stdev:.1f}")

# 2. Number of Subtasks
print(f"{'Number of Subtasks for Human Plan:':40} {human_num_subtask}")
print(f"{'Number of Subtasks for LLM Plan:':40} {llm_num_subtask}")

# 3. Branches/Subtask
human_mean = statistics.mean(human_num_branch_per_subtask)
human_stdev = statistics.stdev(human_num_branch_per_subtask)

llm_mean = statistics.mean(llm_num_branch_per_subtask)
llm_stdev = statistics.stdev(llm_num_branch_per_subtask)

print(f"{'Branches/Subtask for Human Plan':40} M = {human_mean:.1f}, SD = {human_stdev:.1f}")
print(f"{'Branches/Subtask for LLM Plan:':40} M = {llm_mean:.1f}, SD = {llm_stdev:.1f}")

# 4. Nodes/Subtask
human_mean = statistics.mean(human_num_node_per_subtask)
human_stdev = statistics.stdev(human_num_node_per_subtask)

llm_mean = statistics.mean(llm_num_node_per_subtask)
llm_stdev = statistics.stdev(llm_num_node_per_subtask)

print(f"{'Nodes/Subtask for Human Plan:':40} M = {human_mean:.1f}, SD = {human_stdev:.1f}")
print(f"{'Nodes/Subtask for LLM Plan:':40} M = {llm_mean:.1f}, SD = {llm_stdev:.1f}")