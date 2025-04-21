# LawFlow

## Data Analysis

1. Go to `data_analysis` directory

2. Install required packages to perform data analysis

```
pip install python-Levenshtein networkx
```
3. Go to `https://huggingface.co/minnesotanlp/` and download the dataset

4. Put the dataset under the `data` directory

5. Run the `preprocess_data.py` script to get 3 files `human_exec_human_plan.json`,  `llm_cot_exec_human_plan_o1.json`, and `llm_cot_exec_human_plan_r1.json`
```
python3 proprocess_data.py
```

6. Run the data analysis script
```
python3 <script_name>
```
```python
data_analysis
└───adherence-to-task-plan          # Table 2(a)
└───diff-btw-human-and-llm-plans    # Table 1
└───execution_patterns              # Table 2(b)
└───human_llm_node_level_analysis   # Table 3
└───meta_point
└───tool_usage
```
