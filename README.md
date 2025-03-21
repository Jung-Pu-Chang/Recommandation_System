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
├── docs
│   ├── 行銷小幫手_技術文件 (整體架構以及待開發與擴充功能)
│   └── 行銷小幫手_使用手冊 (使用說明書)
├── service
│   ├── app.py (Streamlit 前端) 
│   ├── module.py (呼叫SQL、極少部分資料整理)
│   ├── utils.py (共用函式)
│   └── log 
├── src
│   ├── sql
│   │   ├── spendband_money.sql (整體 spendband 查詢)
│   │   ├── spendband_item.sql (商品 spendband 查詢)
│   │   ├── confidence.sql (合購/加購 碰撞率 查詢)
│   │   ├── total_payment.sql (各支付別 查詢)
│   │   ├── bank_payment.sql (各銀行支付別 查詢)
│   │   └── DM_validation.sql (DM 成效 查詢)
│   ├── gui_test.py (app.py 測試)
│   └── test_module.py (module.py 測試)
├── docker-compose.yml 
├── Dockerfile_Streamlit
└── requirements.txt (部署相關套件)
```

### 小幫手更新
> 透過 MobaXterm 進入 192.168.71.25    
> 進入 /root/dev/PX_AnalyticsHub/  
> 將地端檔案直接複製貼上並取代  
> CI / CD 會自動搬至 629cfa8e2dc9 CONTAINER  


