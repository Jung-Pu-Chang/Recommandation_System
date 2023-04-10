# Recommandation-System

> 本專案內容為推薦系統模型訓練、部署相關程式碼以及執行方式

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
│   └── online_retail_II.csv (raw_data)
├── models
│   └── edge_model  
├── src
│   └── training.py
├── service
│   ├── module.py 
│   ├── module_api.py
└── └── api_test.py 
```

## Usage

### 調整參數

若要進行任何參數調整，請至`config.ini`中改寫參數。

### 情境說明

透過每位消費者的線上購買資料訓練模型，準確推薦消費者可能想購買的商品。

### API 說明
#### module_api.py
1. `module_api.py`會於初始化時，載入`config.ini`參數與`module.py`推薦系統
2. `module.py`會於初始化時，載入`edge_model`模型，並連線至資料庫
3. I :  
   item : str，所在櫃位，格式同TenantPk欄位後6碼，不可為空值，舉例 : '140011'  
   mem_id : str，結帳者，格式同MemId欄位，舉例 : 'D49D1119B2668540'，若為非會員，請輸入'not_mem'，空值請回傳空字串' '  
4. O :  
   dic : dict，推薦內容包含3個跨櫃櫃位推薦(items)，皆不可為空值  
   舉例 : {'items': ['360004', '130464', '151000']}  
```bash
cd ~/aipos/service
python module_2_api.py
```

### 資料來源
https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci
