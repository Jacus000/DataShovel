#  Data Shovel – Interactive Data Exploration & Analysis App

**Data Shovel** is a versatile desktop application built with **PyQt6**, designed for users to load, preview, clean, and analyze data from `.csv` files. The app empowers users to generate insightful visualizations, perform regression analysis, and export results seamlessly. It is an ideal tool for students, data analysts, and hobbyists.

##  Key Features
- **Data Import:** Easily load datasets from CSV and Excel files.
- **Table View:** Interactive data browsing with an intuitive spreadsheet-style interface.
- **Smart Filtering:** Dynamic filtering for both numerical and categorical columns.
- **Data Management:** Robust tools for data cleaning and preprocessing.
- **Advanced Visualizations:** Generate a wide variety of plots, including:
  - Bar, Line, and Scatter plots
  - Box and Violin plots
  - Histograms and Heatmaps
- **Regression Analysis:** Perform Linear Regression with real-time visualization and statistical feedback.

##  System Requirements
- **Python:** 3.10 / 3.12 or newer
- **Dependencies:** Listed in `environment.yml` or `requirements.txt`

##  Installation

### 1. Clone the repository
```bash
git clone [https://github.com/Jacus000/DataShovel.git](https://github.com/Jacus000/DataShovel.git)
cd DataShovel
```
2. Environment Setup:
    - Conda (Recommended)
        1. Remove old environment (if exists):
        ```
        conda remove -n DSenv --all -y
        ```
        2. Create new environment:
        ```
        conda env create -f environment.yml
        ```
        3. Activate environment:
        ```
        conda activate DSenv
        ```
        4. Verify installation:
        ```
        python -c "import numpy, pandas, sklearn, scipy, PyQt6, matplotlib, seaborn; print('OK')"
        ```
    - Venv:
      1. Remove old environment (if exists):
      ```
      rmdir /s /q DSvenv
      ```
      2. Create new enviroment
      ```
      rm -rf DSvenv
      ``` 
      3. Activate enviroment
      ```
      .\DSvenv\Scripts\activate
      ```
      4. Install libraries
      ```
      pip install -r requirements.txt
      ```
3. Run the App
    ```bash
    python main.py
    ```

##  Usage Example
We will use the provided sample dataset: StudentPerformanceFactors.csv

<img width="1918" height="997" alt="image" src="https://github.com/user-attachments/assets/3261e726-1d5e-4ba9-960b-f39b013a79c6" />

Simply browse and load your dataset to get started.

<img width="1917" height="1015" alt="image" src="https://github.com/user-attachments/assets/294ae1e6-180e-4dad-8919-6e9b5b770834" />

<p align="left">
  Let's look at some quick column insights: <br>
  <img src="https://github.com/user-attachments/assets/15e2e043-622c-4e1f-a844-066ccb34817c" alt="Insights" width="300">
</p>

 Filtering & Searching
Narrow down your data with powerful search and filter tools.
<img width="1915" height="1015" alt="image" src="https://github.com/user-attachments/assets/54d491a2-c000-43e2-8617-c6f91961ffca" />
1) Column Visibility: Choose which columns to display in your current view.
2) Live Search: Search for specific values; results update instantly to allow for both general and precise searches.
3) Column Management: Drop unnecessary columns to declutter your dataset.
4) Advanced Filters: Automatically matches data types (numeric/categorical) to quickly find hidden information in large datasets.
5) Real-time Results: Results are displayed simultaneously as you apply filters.

 Data Cleaning & Manipulation
Prepare your data for analysis with just a few clicks.
<img width="1912" height="1013" alt="image" src="https://github.com/user-attachments/assets/9dfd5f51-0e4a-4bfc-a6f4-fa3f17bef45f" />
1) Cleaning Tools: Choose from various types of data cleaning and manipulation.
2) Instant Preview: Constant preview of changes before they are finalized.
3) Apply & Reset: Confirm changes to the dataset or reset to the original state.
4) Dynamic Statistics: Access various options and easily accessible statistics that update constantly.

 Regression Analysis
Predict trends and visualize mathematical relationships.
<img width="1918" height="1017" alt="image" src="https://github.com/user-attachments/assets/79b9c1de-05d6-4d6a-96f4-ed15863964eb" />
1) Model Selection: Choose the appropriate regression model (e.g., Linear).
2) Predictors: Select independent numerical variables.
3) Target Variable: Decide which value you want to predict and visualize it.
4) Statistical Insights: View model coefficients ($b_0$, $x$), $R^2$ score, and RMSE. This gives immediate feedback on predictor strength and mathematical baseline.
5) Visualization: Generate a scatter plot and a linear regression line automatically after training.

<p align="left">
  Finally save your cleaned and pre - analyzed data set: <br>
  <img width="142" height="170" alt="image" src="https://github.com/user-attachments/assets/0f03dabe-1b46-4889-955d-9e36f92d6959" />

</p>






 






