#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2021/03/09 16:44:20
@Author  :   sam.qi
@Version :   1.0
@Desc    :   Dgraph 测试代码
'''

import pydgraph 
import json 
import numpy as np 
import threading
import time



class Task(threading.Thread):
    def __init__(self):
        super().__init__()
        self.time = 0 
        self.error = 0
    
    def run(self):
        start = time.time()
        try:
            client_stub = pydgraph.DgraphClientStub('192.168.86.103:9080')
            client = pydgraph.DgraphClient(client_stub)

            txn = client.txn(read_only=True)


            # Run query.
            query = """{
            people(func: has(test)){
                name
                a1
                a2
                a3
                test {
                    name
                    value
            }
            }
            }"""

            res = txn.query(query)

            # If not doing a mutation in the same transaction, simply use:
            # res = client.txn(read_only=True).query(query, variables=variables)

            ppl = json.loads(res.json)

            # Print results.
            # print('Number of people named "Alice": {}'.format(len(ppl['people'])))
            for person in ppl['people']:
                print(person)
            end = time.time()
            self.time = end-start
        except Exception as e:
            self.error = 1
        # print(self.time)
    


if __name__ == "__main__":

    repeat = 1

    mean = []
    es = []
    for rep in range(repeat):
        ts = []
        errors = 0
        for i in range(1):
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


    
    