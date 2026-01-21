# Aadhaar Enrollment Data Analysis (EDA)

## Overview
This project performs Exploratory Data Analysis (EDA) on the Aadhaar Enrollment Dataset to understand enrollment trends across different regions and age groups. The analysis includes data cleaning, processing, visualization, and key findings based on enrollment patterns.

## Dataset
- Source: data.gov.in (UIDAI Aadhaar Enrollment Dataset)
- Data Type: Aggregated enrollment data
- Categories included:
  - State / District / PIN Code level information
  - Age-wise enrollment groups (0–5, 5–17, 18+)
  - Time-based enrollment patterns (where available)

## Objectives
- Identify state-wise and district-wise Aadhaar enrollment trends  
- Compare enrollments across different age categories  
- Detect major patterns and variations in enrollment activity  
- Present insights using clear visualizations and summary findings  

## Tools & Technologies
- Python
- Pandas
- NumPy
- Matplotlib

## Methodology
1. Data Loading  
2. Data Cleaning  
   - Removed missing/null values (if any)
   - Removed duplicates (if any)
   - Converted columns into correct data types  
3. Data Processing  
   - Grouping and aggregation by region and age category  
   - Filtering relevant data for analysis  
4. Visualization  
   - Bar charts, trend charts, and comparison plots  
5. Insights & Key Findings  
   - Highlighted region-wise differences and demographic patterns  

## Output
The project generates charts and insights that help understand:
- Where Aadhaar enrollment is highest/lowest
- How enrollment differs across age groups
- How enrollment changes over time across regions

## How to Run
1. Clone this repository
2. Install required libraries:
   ```bash
   pip install pandas numpy matplotlib
