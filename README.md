# 行銷小幫手

> 本專案內容包含行銷小幫手程式碼以及相關文件  

> [行銷小幫手](http://192.168.71.25:8501/)   
> 部署位置 : VM = 192.168.71.25，CONTAINER ID = 629cfa8e2dc9  
> 開發工具 : python + PostgreSQL + docker container  
> 使用者透過網址下查詢條件後，於[GreenPulm](http://192.168.71.27/)進行資料整理與分析，python 僅為 API，傳遞使用者條件與回傳 PostgreSQL 查詢結果

## Environment
`python3.8.13`

## Installation

`pip install -r requirements.txt`


## Directory

```bash
.
├── README.md
├── config
│   ├── config.ini (連線、支付別等參數)
│   └── 支付別.csv (定期手動更新支付別文件，資訊部於2025已解決 va_ref_paymethod表的重複問題，未來可直接用中台資料，不必手動更新)
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


