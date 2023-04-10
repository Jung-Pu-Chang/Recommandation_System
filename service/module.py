import pandas as pd 
from pandas import DataFrame
from stellargraph import StellarGraph
from stellargraph.mapper import HinSAGELinkGenerator
import tensorflow as tf
from typing import Any
import warnings
warnings.filterwarnings('ignore')

class Model:
    model_path: str
    node_path: str
    edge_path: str
    batch_size: int
    num_samples: list
    node_df: DataFrame
    edge_df: DataFrame
    model: Any

    def __init__(self, model_path, node_path, edge_path, batch_size, num_samples):
        print("Load Basic Service")
        self.model_path = model_path
        self.node_path = node_path
        self.edge_path = edge_path
        self.batch_size = batch_size
        self.num_samples = num_samples
        self.model = tf.keras.models.load_model(model_path,custom_objects=None, compile=True, options=None)
        self.node_df = pd.read_csv(node_path, encoding='utf-8',header=0) 
        self.edge_df = pd.read_csv(edge_path, encoding='utf-8',header=0)
        self.node_df = self.node_df.sort_values(by = 'weight',ascending=False)
        self.node = self.node_df.set_index('StockCode')
        self.node = self.node.drop(['Country'], axis=1)
        self.G = StellarGraph({"corner": self.node}, {"line": self.edge_df})
        self.generator = HinSAGELinkGenerator(self.G, self.batch_size, self.num_samples,seed=100)
    # 前處理   
    def clean(self, item):
        edges_test = self.edge_df.loc[self.edge_df['source']==item]
        edgelist_test = list(edges_test[["source", "target"]].itertuples(index=False))
        labels_test = edges_test["link"] 
        test_gen = self.generator.flow(edgelist_test, labels_test,seed=100)
        return edges_test, test_gen

    # 預測
    def pred(self, edges_test, test_gen):
        if len(edges_test) > 0:
            print("Done: Model Recommand")
            y_pred = pd.DataFrame(self.model.predict(test_gen))
            edges_test = edges_test.reset_index()
            y_pred = pd.concat([edges_test[['source','target']],y_pred],axis=1)
            y_pred.columns = ['buy', 'StockCode','weight']
            y_pred = pd.merge(y_pred, self.node_df.drop(['weight'], axis=1), on="StockCode",how='left')
            y_pred = y_pred.drop(['buy'], axis=1)
            return y_pred      
        else:
            print("Done: Hot Recommand")
            y_pred = self.node_df.iloc[:1000,:]
            return y_pred  

    def recommand(self, item):  
        edges_test, test_gen = self.clean(item)
        pred_df = self.pred(edges_test, test_gen)
        out = pred_df['StockCode'].head(3).values.tolist()
        dic = dict()
        dic['StockCode'] = out
        return out

if __name__=='__main__': #測試
    import configparser
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    model_path = config['recommand']['model_path']
    node_path = config['recommand']['data_path']+'node_df.csv'
    edge_path = config['recommand']['data_path']+'edge_df.csv'
    
    #config.read('config.ini')
    #model_path = 'edge_model'
    #node_path = 'node_df.csv'
    #edge_path = 'edge_df.csv'
    batch_size = int(config['recommand']['batch_size'])
    num_samples = list(config['recommand']['num_samples'])
    num_samples = [int(x) for x in num_samples]
    
    'init test'
    test = Model(model_path, node_path, edge_path, batch_size, num_samples) 
    
    'recommand test'
    out = test.recommand('data玩容噗')
    out = test.recommand('22726')
    
    'clean test'
    a,b = test.clean('data玩容噗')
    c,d = test.clean('22726') 
    
    'pred test'
    pred_1 = test.pred(a,b)
    pred_2 = test.pred(c,d)
