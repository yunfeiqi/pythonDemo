#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   visdom_demo.py
@Time    :   2021/11/12 20:06:29
@Author  :   Sam.Qi 
@Version :   1.0
@Contact :   samqi1122@126.com
'''

import visdom

import numpy as np 

vis = visdom.Visdom()
vis.text("Hello,World！")
vis.image(np.ones((3,10,10)))

import visdom
vis = visdom.Visdom()

trace = dict(x=[1, 2, 3], y=[4, 5, 6], mode="markers+lines", type='custom',
             marker={'color': 'red', 'symbol': 104, 'size': "10"},
             text=["one", "two", "three"], name='1st Trace')
layout = dict(title="First Plot", xaxis={'title': 'x1'}, yaxis={'title': 'x2'})

vis._send({'data': [trace], 'layout': layout, 'win': 'mywin'})
