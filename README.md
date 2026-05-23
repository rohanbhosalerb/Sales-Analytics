# 📊 Sales Data Analyzer

A Python data analytics project that performs exploratory data analysis (EDA) on a retail sales dataset — including data cleaning, summary statistics, and four insightful visualizations.

## 🔍 What It Does

- **Loads & inspects** a CSV sales dataset
- **Cleans** missing values and engineers new features (month, quarter)
- **Prints** key metrics: total revenue, average order value, top category, regional breakdown
- **Generates 4 charts** saved to `outputs/`:
  | Chart | Description |
  |---|---|
  | `monthly_revenue.png` | Revenue trend across all 12 months |
  | `category_breakdown.png` | Bar + pie chart of revenue per category |
  | `region_category_heatmap.png` | Heatmap of revenue by region & category |
  | `discount_impact.png` | How discounts affect revenue & order volume |

## 📁 Project Structure

```
sales-data-analyzer/
├── data/
│   └── sales_data.csv        # Generated dataset (1,000 orders)
├── outputs/                  # Charts are saved here
├── generate_data.py          # Creates the sample dataset
├── analyze.py                # Main analysis script
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/sales-data-analyzer.git
cd sales-data-analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the dataset
```bash
python generate_data.py
```

### 4. Run the analysis
```bash
python analyze.py
```

Charts will be saved to the `outputs/` folder.

## 📈 Sample Output

```
=======================================================
📦  DATASET OVERVIEW
=======================================================
  Rows      : 1,000
  Columns   : 9
  Date range: 2023-01-01 → 2023-12-31

🧹  Cleaned: dropped 38 incomplete rows → 962 remaining

=======================================================
📊  KEY METRICS
=======================================================
  Total Revenue   : $XXX,XXX.XX
  Avg Order Value : $XXX.XX
  Top Category    : Electronics
  ...
```

## 🛠️ Tech Stack

- **Python 3.8+**
- **pandas** — data loading, cleaning, aggregation
- **NumPy** — numerical operations
- **Matplotlib** — charting
- **Seaborn** — styled statistical visualizations

## 💡 Ideas to Extend

- Add a Jupyter notebook with interactive charts
- Swap in a real dataset (e.g. from Kaggle)
- Build a Streamlit dashboard for live filtering
- Add unit tests with `pytest`

## 📄 License

MIT

## 📊 Sample Charts

### Monthly Revenue
![Monthly Revenue](outputs/monthly_revenue.png)

### Category Breakdown
![Category Breakdown](outputs/category_breakdown.png)

### Region × Category Heatmap
![Heatmap](outputs/region_category_heatmap.png)

### Discount Impact
![Discount Impact](outputs/discount_impact.png)
