#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2021/03/08 16:52:50
@Author  :   sam.qi
@Version :   1.0
@Desc    :   Neo4j 性能测试，对Neo4j并发读
             1. 连接Neo4j
             2. 读取指定节点的所有属性
             3. 计算读取时间
'''

import numpy as np 
import time 
import threading

from py2neo import Graph,Node,Relationship, NodeMatcher,RelationshipMatcher
 
##连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://192.168.86.103:7674',username='neo4j',password='neo4j')


nodematcher= NodeMatcher(graph)
# node = nodematcher.match("winner",**{"name":"雅安市蓝得信息技术有限公司"})



# node = nodematcher.get(241167)


# res = list(graph.match(nodes = (node,)   ))
# print(res)


# # node = node.first()
# relationmatcher = RelationshipMatcher(graph)
# res = relationmatcher.match((node,))
# print(list(res))


 
from neo4j import GraphDatabase
 
 
class Neo4jHandler:
    """
    Handler of graph database Neo4j reading and writing.
    """
    def __init__(self, driver):
        """
        Get Neo4j server driver.
        :param driver: driver object
            A driver object holds the detail of a Neo4j database including server URIs, credentials and other configuration, see
            " http://neo4j.com/docs/api/python-driver/current/driver.html ".
        """
        self.driver = driver
 
    def __repr__(self):
        # printer = 'o(>﹏<)o ......Neo4j old driver "{0}" carry me fly...... o(^o^)o'.format(self.driver)
        printer = ''
        return printer
 
    def listreader(self, cypher, keys):
        """
        Read data from Neo4j in specified cypher.
        Read and parse data straightly from cypher field result.
        :param cypher: string
            Valid query cypher statement.
        :param keys: list
            Cypher query columns to return.
        :return: list
            Each returned record constructs a list and stored in a big list, [[...], [...], ...].
        """
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                data = []
                result = tx.run(cypher)
                for record in result:
                    rows = []
                    for key in keys:
                        rows.append(record[key])
                    data.append(rows)
                return data
 
    def dictreader(self, cypher):
        """
        Read data from Neo4j in specified cypher.
        The function depends on constructing dict method of dict(key = value) and any error may occur if the "key" is invalid to Python.
        you can choose function dictreaderopted() below to read data by hand(via the args "keys").
        :param cypher: string
            Valid query cypher statement.
        :return: list
            Each returned record constructs a dict in "key : value" pairs and stored in a big list, [{...}, {...}, ...].
        """
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                data = []
                for record in tx.run(cypher).records():
                    item = {}
                    for args in str(record).split('>')[0].split()[1:]:
                        print("item.update(dict({0}))".format(args)) 
                    data.append(item)
                return data
 
    def dictreaderopted(self, cypher, keys=None):
        """
        Optimized function of dictreader().
        Read and parse data straightly from cypher field result.
        :param cypher: string
            Valid query cypher statement.
        :param keys: list, default : none(call dictreader())
            Cypher query columns to return.
        :return: list.
            Each returned record constructs an dict in "key : value" pairs and stored in a list, [{...}, {...}, ...].
        """
        if not keys:
            return self.dictreader(cypher)
        else:
            with self.driver.session() as session:
                with session.begin_transaction() as tx:
                    data = []
                    result = tx.run(cypher)
                    for record in result:
                        item = {}
                        for key in keys:
                            item.update({key : record[key]})
                        data.append(item)
                    return data
 
    def cypherexecuter(self, cypher):
        """
        Execute manipulation into Neo4j in specified cypher.
        :param cypher: string
            Valid handle cypher statement.
        :return: none.
        """
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run(cypher)
        session.close()
 

class Task(threading.Thread):
    def __init__(self):
        super().__init__()
        self.time = 0 
        self.error = 0
    
    def run(self):
        start = time.time()
        try:
            uri = "bolt://192.168.86.103:7788"
            driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))
            MyNH = Neo4jHandler(driver)
            print(MyNH)
            cypher_exec = """
                            CREATE (Neo:Crew {name:'Neo'}),
                                (Morpheus:Crew {name: 'Morpheus'}),
                                (Trinity:Crew {name: 'Trinity'}),
                                (Cypher:Crew:Matrix {name: 'Cypher'}),
                                (Smith:Matrix {name: 'Agent Smith'}),
                                (Architect:Matrix {name:'The Architect'}),
                                (Neo)-[:KNOWS]->(Morpheus),
                                (Neo)-[:LOVES]->(Trinity),
                                (Morpheus)-[:KNOWS]->(Trinity),
                                (Morpheus)-[:KNOWS]->(Cypher),
                                (Cypher)-[:KNOWS]->(Smith),
                                (Smith)-[:CODED_BY]->(Architect)
                        """  # "example cypher statement from http://console.neo4j.org/"
            cypher_read = """
                            MATCH(n:Person) -[r]- (v) return n,v
                        """
            # MyNH.cypherexecuter(cypher_exec)
            # print(MyNH.listreader(cypher_read, ['n', 'v']))
            MyNH.listreader(cypher_read, ['n', 'v'])
            # print(MyNH.dictreader(cypher_read))
            # print(MyNH.dictreaderopted(cypher_read, ['n']))
            end = time.time()
            self.time = end-start
        except Exception as e:
            self.error = 1
        # print(self.time)
    

if __name__ == "__main__":

    repeat = 10

    mean = []
    es = []
    for rep in range(repeat):
        ts = []
        errors = 0
        for i in range(2000):
            t = Task()
            t.start()
            ts.append(t)
        
        spans = []
        for t  in ts:
            t.join()
            spans.append(t.time)
            errors += t.error
        spans = np.array(spans)
        es.append(errors)
        mean.append(np.mean(spans))
    print(np.array(mean).mean())
    print(np.array(es).mean())


    
    