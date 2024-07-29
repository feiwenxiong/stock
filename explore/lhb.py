import os
import sys
cpath_current = os.path.dirname(os.path.dirname(__file__))
sys.path.append(cpath_current)
import instock
from instock.core.crawling.stock_lhb_em import *
import time
from py2neo import Graph, Subgraph
from py2neo import Node, Relationship, Path
from datetime import datetime
import json
from instock.core.crawling.stock_selection import * 

#数据库链接密码
NEO4J_PASSWORD = "root"

class TransactionWrapper:
    '''
    用来适配with语句的上下文管理器wrapper
    '''
    def __init__(self, graph):
        self.graph = graph
        self.tx = None

    def __enter__(self):
        self.tx = self.graph.begin()
        return self.tx

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.graph.rollback(self.tx)
            #self.tx.rollback()
        else:
            self.graph.commit(self.tx)
            #self.tx.commit()
        self.tx = None


def connect_neo4j_db():
    # 连接数据库
    graph = Graph('bolt://localhost:7687', auth=('neo4j', NEO4J_PASSWORD))
    # graph = Graph('http://localhost:7474', username='neo4j', password=NEO4J_PASSWORD)
    # 删除所有已有节点
    #graph.delete_all()
    return graph

def save_graph_to_json(graph, output_filename):
    # 获取所有节点和关系
    nodes = list(graph.nodes)
    relationships = list(graph.relationships)

    # 构建节点和关系的映射
    node_map = {node.identity: {"labels": list(node.labels), "properties": dict(node)} for node in nodes}
    relationship_map = [
        {
            "start_node": rel.start_node.identity,
            "end_node": rel.end_node.identity,
            "type": type(rel).__name__,
            "properties": dict(rel),
        }
        for rel in relationships
    ]

    # 结合节点和关系数据
    graph_data = {
        "nodes": node_map,
        "relationships": relationship_map
    }

    # 将数据写入JSON文件
    with open(output_filename, "w") as file:
        json.dump(graph_data, file, indent=2)

def save_transaction_to_json(tx, output_filename):
    # 通过Cypher查询获取所有节点和关系
    nodes_result = tx.run("MATCH (n) RETURN n")
    relationships_result = tx.run("MATCH ()-[r]-() RETURN r")

    # 将结果转换为节点和关系的列表
    nodes = [record["n"] for record in nodes_result]
    relationships = [record["r"] for record in relationships_result]

    # 构建节点和关系的映射
    node_map = {node.identity: {"labels": list(node.labels), "properties": dict(node)} for node in nodes}
    relationship_map = [
        {
            "start_node": rel.start_node.identity,
            "end_node": rel.end_node.identity,
            "type": type(rel).__name__,
            "properties": dict(rel),
        }
        for rel in relationships
    ]

    # 结合节点和关系数据
    graph_data = {
        "nodes": node_map,
        "relationships": relationship_map
    }

    # 将数据写入JSON文件
    with open(output_filename, "w") as file:
        json.dump(graph_data, file, indent=2)

def write_all_nodes_degree(graph):
    # 定义Cypher查询
    query = """
    MATCH (n)
    WITH n, size((n)-[]-()) AS degree
    SET n.degree = degree
    RETURN count(n)
    """

    # 在事务中执行查询
    with TransactionWrapper(graph) as tx:
        result = tx.run(query)
    print(f"Updated {result.data()} nodes with their degrees.")
    return 

def lhb_yyb_stock_daily_work(start_date="20240725", end_date="20240725",delete=True):
    '''
    获取和存储营业部和股票的关系图与原始表格
    '''
    stock_lhb_hyyyb_em_df = stock_lhb_hyyyb_em(
         start_date=start_date, end_date=end_date
    )
    stock_lhb_hyyyb_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"lhb_yyb2stock_{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.xlsx"),index=False)
    
    
    #对个股股票获取龙虎榜数据
    stock_lhb_detail_em_df = stock_lhb_detail_em(start_date=start_date, end_date=end_date)
    
    graph = connect_neo4j_db()
    #每日更新图
    if delete:
        graph.delete_all()
    df_processed = stock_lhb_hyyyb_em_df[["营业部名称","买入股票","上榜日","买入总金额","总买卖净额"]]
    with TransactionWrapper(graph) as tx:
         # 遍历DataFrame的每一行，为每一行创建一个节点
        for index, row in df_processed.iterrows():
            node_yyb = Node("营业部",
                            name=row["营业部名称"],
                            date=str(row['上榜日']),
                            netIn=row["总买卖净额"],
                            inPct= round(row["总买卖净额"] / (row["买入总金额"]  + 1), 3),) 
            #tx.create(node_yyb)
            tx.merge(node_yyb,"营业部","name")
            stocks = row["买入股票"].strip().split()
            if stocks:
                for stock in stocks:
                    
                    current_stock_detail = stock_lhb_detail_em_df[stock_lhb_detail_em_df["名称"] == stock]
                    # tmp_dict = current_stock_detail.to_dict()
                    columns = ["代码","解读","收盘价","涨跌幅",
                               "龙虎榜净买额","龙虎榜买入额","龙虎榜卖出额","市场总成交额",
                               "净买额占总成交比","成交额占总成交比","换手率","流通市值","上榜原因"]
                    current_stock_detail = current_stock_detail[columns]
                    for index, current_line in current_stock_detail.iterrows():
                        tmp_dict = current_line.to_dict()
                    # print(tmp_dict)
                    # tmp_dict.pop("上榜日")
                    node_stock = Node("股票",name=stock,**tmp_dict)
                    #tx.create(node_stock)
                    #保证股票唯一性
                    tx.merge(node_stock,"股票","name")
                    

                    real = Relationship(node_yyb,'投资',node_stock)
                    tx.create(real)

    #获取属性degree 
    with TransactionWrapper(graph) as tx:
        write_all_nodes_degree(graph)
    
    #保存图
    with TransactionWrapper(graph) as tx:
        try:
            filename = os.path.join(os.path.dirname(__file__) , f"lhb_yyb2stock_graph_{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.json")
            save_transaction_to_json(tx,filename) 
        except Exception as e:
            print(e)

    
    #补充
    with TransactionWrapper(graph) as tx:
        query = """
                MATCH (n:股票) 
                RETURN n;
                """
        # query_yyb =  """
        #             MATCH (n:营业部) 
        #             RETURN n;
        #             """
        stocks = tx.run(query).data()
        #yybs = tx.run(query_yyb).data()
        # stocks.data()
        columns= ["序号","交易营业部名称","买入金额","买入金额-占总成交比例","卖出金额","卖出金额-占总成交比例"	,"净额","类型"]
        for stock_dcit in tqdm(stocks):
            stock = stock_dcit["n"]
            
            if 1:
                stock_sell = stock_lhb_stock_detail_em(symbol=stock["代码"], date=end_date, flag="卖出")
                yyb_names = stock_sell["交易营业部名称"]
                order_ = stock_sell[columns[0]]
                #cypher查询sell node节点
                for i,yyb_name in enumerate(yyb_names):
                    #如果没有对应yyb就创建
                    params = {"name": yyb_name} 
                    query_yyb = """
                                MERGE (n:营业部 {name: $name})
                                ON CREATE SET  n.name = $name
                                RETURN n;
                                """
                    #找到股票对应的营业部node
                    yybs_sells_nodes = tx.run(query_yyb,params).data()
                    for it in yybs_sells_nodes:
                        if i  >= 5:
                            #重复数据
                            break
                        #get nodes
                        yyb_node = it["n"]
                        #stock和node之间建立relationship
                        
                            # print(1)
                        real = Relationship(stock,
                                            f'卖_{order_[i]}',
                                            yyb_node,
                                            卖出金额=float(stock_sell.loc[i,columns[4]]),
                                            卖出金额_占总成交比例=float(stock_sell.loc[i,columns[5]])
                                                )
                        tx.create(real)
                    
                    
            if 1:     
                #buy
                stock_buy = stock_lhb_stock_detail_em(symbol=stock["代码"], date=end_date, flag="买入")
                yyb_names = stock_buy["交易营业部名称"]
                order_buy = stock_buy[columns[0]]
                for j,yyb_name in enumerate(yyb_names):
                    #没有该营业部的话就创建一个yyb_node
                    params = {"name": yyb_name} 
                    query_yyb = """
                                MERGE (n:营业部 {name: $name})
                                ON CREATE SET  n.name = $name
                                RETURN n;
                                """
                    yybs_buys_nodes = tx.run(query_yyb,params).data()
                    #找到股票对应的营业部node
                    for it in yybs_buys_nodes:
                        if i  >= 5:
                            #重复数据
                            break
                        #node
                        yyb_node = it["n"]
                        #stock和node之间cerate relationship
                        real = Relationship(yyb_node,
                                            f'买_{order_buy[j]}',
                                            stock,
                                            买入金额=float(stock_buy.loc[j,columns[2]]),
                                            买入金额_占总成交比例=float(stock_buy.loc[j,columns[3]])
                                            )
                        tx.create(real)
                
             
            
            

if __name__ == "__main__":
    s = time.time()
    # stock_lhb_detail_em_df = stock_lhb_detail_em(
    #     start_date="20240725", end_date="20240725"
    # )
    # stock_lhb_detail_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)
    # print(stock_lhb_detail_em_df)

    # stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近一月")
    # stock_lhb_stock_statistic_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)
    # print(stock_lhb_stock_statistic_em_df)

    # stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近三月")
    # print(stock_lhb_stock_statistic_em_df)
    

    # stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近六月")
    # print(stock_lhb_stock_statistic_em_df)

    # stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近一年")
    # print(stock_lhb_stock_statistic_em_df)

    # stock_lhb_jgmmtj_em_df = stock_lhb_jgmmtj_em(
    #      start_date="20240725", end_date="20240725"
    # )
    # stock_lhb_jgmmtj_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)
    # # print(stock_lhb_jgmmtj_em_df)

    # stock_lhb_jgstatistic_em_df = stock_lhb_jgstatistic_em(symbol="近一月")
    # print(stock_lhb_jgstatistic_em_df)
    # stock_lhb_jgstatistic_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)

    

    
    ##构建营业部和股票的关系图
    lhb_yyb_stock_daily_work(start_date="20240729", end_date="20240729")
    
    

    # print(stock_lhb_hyyyb_em_df)
    

    # stock_lhb_yybph_em_df = stock_lhb_yybph_em(symbol="近一月")
    # print(stock_lhb_yybph_em_df)
    # stock_lhb_yybph_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)

    # stock_lhb_traderstatistic_em_df = stock_lhb_traderstatistic_em(symbol="近一月")
    # print(stock_lhb_traderstatistic_em_df)
    # stock_lhb_traderstatistic_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)


    # stock_lhb_stock_detail_date_em_df = stock_lhb_stock_detail_date_em(symbol="002901")
    # print(stock_lhb_stock_detail_date_em_df)

    # stock_lhb_stock_detail_em_df = stock_lhb_stock_detail_em(
        # symbol="002901", date="20221012", flag="买入"
    # )
    # stock_lhb_stock_detail_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)
    # print(stock_lhb_stock_detail_em_df)
    

    # stock_lhb_stock_detail_em_df = stock_lhb_stock_detail_em(
    #     symbol="600611", date="20240725", flag="卖出"
    # )
    # # print(stock_lhb_stock_detail_em_df)
    # stock_lhb_stock_detail_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)


    print(f"it cost: {time.time() - s} seconds.")