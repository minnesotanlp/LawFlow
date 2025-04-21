# LawyerBench: Collecting and Simulating Lawyers Thought Process

## About
This branch contains following folders
- `data_analysis`: scripts for performed data analysis in the paper
- `modeling`: 

## Data Analysis
1. Go to `data_analysis` directory.

2. Install the required packages to run the script.

```
pip install python-Levenshtein networkx
```
3. Go to `https://huggingface.co/minnesotanlp/` and download the dataset.

4. Put the dataset file under the `data_analysis/data` directory.

5. Run the `preprocess_data.py` script to prepare the data files for the data analysis script.
```
python3 proprocess_data.py
```

6. Run the data analysis script.
```
python3 <script_name>
```

Here are the available scripts to run
```python
data_analysis
└───adherence-to-task-plan          # Table 2(a): Human and LLM Adherence to its Plan
└───diff-btw-human-and-llm-plans    # Table 1: Difference between Human and LLM Plans
└───execution_patterns              # Table 2(b): Execution patterns between Human and LLM
└───human_llm_node_level_analysis   # Table 3: Human workflow and LLM Workflow
└───meta_point
└───tool_usage
```
