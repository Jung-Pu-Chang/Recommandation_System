import pandas as pd
import numpy as np
from keras.models import load_model
import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.backend as K
from tensorflow.keras import Model, optimizers, losses, metrics
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth,association_rules
from sklearn.preprocessing import LabelEncoder
from sklearn import model_selection
from stellargraph import StellarGraph,globalvar,datasets
import stellargraph as sg
from stellargraph.mapper import HinSAGELinkGenerator
from stellargraph.layer import HinSAGE, link_classification
import warnings

'use 2011 transaction data'
warnings.filterwarnings('ignore')
raw = pd.read_csv('online_retail_II.csv', encoding='utf-8')
raw.columns 
raw = raw.dropna(subset=['Customer ID'])
raw['total_price'] = raw['Quantity'] * raw['Price']
raw['ymd'] = raw['InvoiceDate'].astype(str).str[:10]
raw['y'] = raw['InvoiceDate'].astype(str).str[:4]
raw = raw.loc[raw['y']=='2011'] 

'Basket Analysis: StockCode purchased per person per day = basket'
raw['key'] = raw['Customer ID'].astype(str) + ['-'] + raw['ymd'].astype(str)
df = raw.drop_duplicates(subset=['key','StockCode'],keep='first')
df['chk'] = 1
basket = df.groupby('key')['StockCode'].apply(list).values
te = TransactionEncoder()
te_ary = te.fit(basket).transform(basket)
df = pd.DataFrame(te_ary, columns=te.columns_)

'node feature : weight(buy times) Country(made in where)'
items = list(df.columns)
counts = df.sum(axis = 'columns').values
node_df = pd.DataFrame(list(zip(items, counts)), columns =['StockCode', 'buy'])
ph_2 = raw.drop_duplicates(subset=['StockCode'],keep='last')
node_df = pd.merge(node_df, ph_2[["StockCode","Country"]], on="StockCode",how='left')
labelencoder = LabelEncoder()
node_df['Country_en'] = labelencoder.fit_transform(node_df['Country'])
node_df = node_df.rename(columns={'buy': 'weight'})
node_df.to_csv('./data/node_df.csv',encoding='utf_8',index=False) 

'edge feature : link = lift(index for promoting by other item) > 10'
df['item_count'] = df.sum(axis = 1)
df = df.loc[df['item_count']>1]
df = df.drop(['item_count'], axis=1)
res = fpgrowth(df,min_support=0.01,max_len=2,use_colnames=True)
edge_df = association_rules(res, metric="support", min_threshold=0.01)
edge_df["antecedents"] = edge_df["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
edge_df["consequents"] = edge_df["consequents"].apply(lambda x: list(x)[0]).astype("unicode")
edge_df = edge_df.rename(columns={'antecedents': 'source', 'consequents': 'target'})
edge_df.loc[(edge_df['lift']>10), "link"] = 1
edge_df['link'] = edge_df['link'].fillna(0) 
edge_df = edge_df[['source','target','link']]
edge_df.to_csv('./data/edge_df.csv',encoding='utf_8',index=False) 

"df to graph"
node_df = node_df.set_index('StockCode')
node_df = node_df.drop(['Country'], axis=1)
G = StellarGraph({"corner": node_df}, {"line": edge_df})
print(G.info())

'train_test_split'
edges_train, edges_test = model_selection.train_test_split(
    edge_df, train_size=0.7, test_size=0.3)

edgelist_train = list(edges_train[["source", "target"]].itertuples(index=False))
edgelist_test = list(edges_test[["source", "target"]].itertuples(index=False))

labels_train = edges_train["link"]
labels_test = edges_test["link"]

"model(HinSAGE) training"
num_samples = [8, 4] 
batch_size = 2000
epochs = 1

generator = HinSAGELinkGenerator(G, batch_size, num_samples,)
train_gen = generator.flow(edgelist_train, labels_train, shuffle=True)
test_gen = generator.flow(edgelist_test, labels_test)
generator.schema.type_adjacency_list(generator.head_node_types, len(num_samples))

hinsage_layer_sizes = [32, 32]
assert len(hinsage_layer_sizes) == len(num_samples)

hinsage = HinSAGE(
    layer_sizes=hinsage_layer_sizes, generator=generator, bias=True, dropout=0.0)

x_inp, x_out = hinsage.in_out_tensors()

# Final estimator layer
score_prediction = link_classification(output_act="relu", 
                                       edge_embedding_method="ip")(x_out)

model = Model(inputs=x_inp, outputs=score_prediction)
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=[tf.keras.metrics.Precision(), tf.keras.metrics.Recall()],
)

num_workers = 4

history = model.fit(
    train_gen,
    validation_data=test_gen,
    epochs=epochs,
    verbose=1,
    shuffle=False,
    use_multiprocessing=False,
    workers=num_workers,
)
#sg.utils.plot_history(history)

'export model'
model.save("edge_model")

'export config'
import configparser
model_path = './models/edge_model'
data_path = './data/'
batch_size = 200
num_samples = [8, 4]
config = configparser.ConfigParser()
config['recommand'] = {}
config['recommand']['model_path'] = model_path
config['recommand']['data_path'] = data_path
config['recommand']['batch_size'] = str(batch_size)
config['recommand']['num_samples'] = ''.join(str(x) for x in num_samples)
with open('config.ini', 'w') as f:
    config.write(f)
