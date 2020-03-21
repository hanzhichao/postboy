#!/bin/env/python
# coding=utf-8
from highcharts import Highchart



def save_map():
    chart = Highchart()

    chart.set_options('chart', {'inverted': True})

    options = {
        'title': {
            'text': 'LoadBoy 接口负载图'
        },
        'subtitle': {
            'text': '响应时间/吞吐量/线程数'
        },
        'xAxis': {
            'reversed': False,
            'title': {
                'enabled': True,
                'text': '响应时间'
            },
            'labels': {
                'formatter': 'function () {\
                    return this.value + " t/s";\
                }'
            },
            'maxPadding': 0.05,
            'showLastLabel': True
        },
        'yAxis': {
            'title': {
                'text': '线程数'
            },
            'labels': {
                'formatter': "function () {\
                    return this.value + '';\
                }"
            },
            'lineWidth': 2
        },
        'legend': {
            'enabled': False
        },
        'tooltip': {
            'headerFormat': '<b>{series.name}</b><br/>',
            'pointFormat': ''
        }
    }

    chart.set_dict_options(options)

    global rt2
    global tps
    global t_num
    tps_data = list(zip(tps, t_num))
    chart.add_data_set(tps_data, 'spline', 'tps', marker={'enabled': False}) 

    rt_data = list(zip(rt2, t_num))
    chart.add_data_set(rt_data, 'line', 'rt', marker={'enabled': False}) 

    chart.save_file()
