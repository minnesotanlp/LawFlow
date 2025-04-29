# [LawFlow: Collecting and Simulating Lawyers Thought Process](https://arxiv.org/abs/2504.18942)

## Abstract
Legal practitioners, particularly those early in their careers, face complex, high-stakes tasks that require adaptive, context-sensitive reasoning. While AI holds
promise in supporting legal work, current datasets and models are narrowly focused on isolated subtasks and fail to capture the end-to-end decision-making required in real-world practice. To address this gap, we introduce LawFlow, a dataset of complete end-to-end legal workflows collected from trained law students, grounded in real-world business entity formation scenarios. Unlike prior datasets focused on input-output pairs or linear chains of thought, LawFlow captures dynamic, modular, and iterative reasoning processes that reflect the ambiguity, revision, and client-adaptive strategies of legal practice. Using LawFlow, we compare human and LLM-generated workflows, revealing systematic differences in structure, reasoning flexibility, and plan execution. Human workflows tend to be modular and adaptive, while LLM workflows are more sequential, exhaustive, and less sensitive to downstream implications. Our findings also suggest that legal professionals prefer AI to carry out supportive roles, such as brainstorming, identifying blind spots, and surfacing alternatives, rather than executing complex workflows end-to- end. Building on these findings, we propose a set of design suggestions, rooted in empirical observations, that align AI assistance with human goals of clarity, completeness, creativity, and efficiency, through hybrid planning, adaptive execution, and decision-point support. Our results highlight both the current limitations of LLMs in supporting complex legal workflows and opportunities for developing more collaborative, reasoning-aware legal AI systems. All data and code are available on our project page: https://minnesotanlp.github.io/LawFlow-website/.

## About
This branch contains following folders
- `data_analysis`: scripts for performed data analysis in the paper
- `modeling`: Notebooks for modelling and training models on our data


## Modeling
1. Go to `modeling` directory.

2. There are 3 notebooks:
- `Plan_Generation.ipynb`: LLM Generated High-Level Plan based on the Business entity formation scenarios(Figure 5 in the paper)
- `Generate_LLM_Outputs.ipynb`: LLM simulated execution on scenarios using Human Plan (Table 2 in the paper)
- `Train_WorkFlow_Monitor.ipynb`: Train Llama 3.2 1B model on Human Executed Sequences and flag unusual workflow steps (Table 3, Figure 8)

3. For Plan_Generation.ipynb and Generate_LLM_Outputs.ipynb:

   a. Acquire OpenAI o1 Reasoning Model API Keys from: https://openai.com/ and DeepSeek R1 Reasoning model keys from: https://www.deepseek.com/

4. For Train_WorkFlow_Monitor.ipynb:

   a. For llama 3.2 1B model, sign up at and request for weights from: https://llama.meta.com/llama-downloads

   b. Acquire a [HuggingFace API Key]([url](https://huggingface.co/)) and [Weights & Biases API Key]([url](https://wandb.ai)) (For monitoring the run, optional)

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

---
## Code Contributors
[Ritik Parkar](https://github.com/RitikParkar), [Khanh Chi Le](https://github.com/chile2706) 

## BibTex
```
@misc{das2025lawflowcollectingsimulating,
      title={LawFlow : Collecting and Simulating Lawyers' Thought Processes}, 
      author={Debarati Das and Khanh Chi Le and Ritik Sachin Parkar and Karin De Langis and Brendan Madson and Chad M. Berryman and Robin M. Willis and Daniel H. Moses and Brett McDonnell and Daniel Schwarcz and Dongyeop Kang},
      year={2025},
      eprint={2504.18942},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2504.18942}, 
}
```
