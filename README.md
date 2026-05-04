# engagement-analytics-pandas
Data analysis project using Pandas to uncover user engagement patterns and author performance from event and story datasets.
# Event & Story Data Analysis using Pandas

## Overview
This project focuses on analyzing user interaction data by combining two datasets: **events** and **stories**. The goal is to extract meaningful insights such as user engagement patterns, author performance, and time-based activity trends.

---

## Objective
- Analyze relationships between user activity and content
- Identify high-performing authors
- Understand user behavior across different time intervals
- Solve real-world data issues like merging inconsistencies and missing values

---

## Dataset Description

### 1. Events Dataset
Contains user interaction data:
- `entity_id` → references a story
- `timestamp` → time of interaction
- session/activity-related fields

### 2. Stories Dataset
Contains content-related data:
- `_id` → unique story identifier
- `author` → creator of the story
- additional metadata

---

## Data Processing

- Cleaned missing/null values
- Converted timestamps into usable datetime format
- Extracted features such as **hour of activity**
- Merged datasets using:
  - `entity_id` (events)
  - `_id` (stories)

---

## Key Analysis Questions

1. Which author has the highest total views?
2. Which author has the lowest engagement?
3. What is the hourly distribution of user sessions?
4. When is peak user activity observed?
5. How does engagement vary across time?
6. (Add your remaining questions here…)

---

## Key Insights

-  User activity shows clear peaks during specific hours of the day  
-  Certain authors consistently outperform others in engagement  
-  Initial analysis showed missing author data due to incorrect merging  
-  Data alignment plays a critical role in accurate insights  

---

## Challenges Faced

- Mismatch between `entity_id` and `_id` during merging  
- Empty outputs (`Series([], dtype: int64)`) due to join issues  
- Handling missing or inconsistent data  

**Solution:**  
Careful validation of join keys and data cleaning ensured accurate results.

---

## Tech Stack

- Python 
- Pandas  
- NumPy  
- Jupyter Notebook  

---

## Future Improvements

- Add data visualizations (matplotlib/seaborn)
- Build an interactive dashboard
- Perform deeper behavioral analysis
- Apply machine learning for prediction

---

## How to Run
1. Clone the repository  
```bash
git clone https://github.com/your-username/your-repo-name.git
1. Clone the repository  
```bash
git clone https://github.com/your-username/your-repo-name.git
