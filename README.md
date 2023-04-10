# Recommandation_System

> 本專案內容為推薦系統模型訓練、部署相關程式碼以及執行方式  

> 首先藉由FP-growth進行關聯分析，並以lift指標定義連結  
> 接著使用 HinSAGE 建模(link prediction)  
> 最後新增熱門推薦，來解決新產品無資料的狀況(cold-start)

## Environment
`python3.8.13`


## Installation

`pip install -r requirements.txt`


## Directory

```bash
.
├── README.md
├── config
│   └── config.ini (路徑 & 模型參數)
├── data
│   └── online_retail_II.csv (raw_data，為防止侵權，請另外至下方網址下載)
├── models
│   └── edge_model  
├── src
│   └── training.py
├── service
│   ├── module.py 
│   ├── module_api.py
└── └── api_test.py 
```

### 資料來源
https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci

## Usage

### 調整參數

若要進行任何參數調整，請至`config.ini`中改寫參數。

### 情境說明

透過每位消費者的線上購買資料訓練模型，準確推薦消費者可能想購買的商品。

### API 說明
#### module_api.py
1. `module_api.py`會於初始化時，載入`config.ini`參數與`module.py`推薦系統
2. `module.py`會於初始化時，載入`edge_model`模型，並匯入`node_df.csv`、`edge_df.csv`
3. I :  
   item : str，購買商品，空值請回傳空字串，舉例 : '22726'  
4. O :  
   dic : dict，推薦內容包含3個商品推薦(StockCode)，皆不可為空值  
   舉例 : {'StockCode': ["22494","21417","16254"]}  

```bash
cd ~/Recommandation_System/service
python module_api.py
```


