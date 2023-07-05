// 模拟数据, 计算全部放在后台
export const demo_lable = {
    "name": "media/images/tests/srep40550_fig2.jpg",   //如果name 后台请求应该是url路径才对 模拟数据就先从前端取
    "bars": [
        {
            "id": 8,
            "points": [
                [
                    611,
                    465
                ],
                [
                    743,
                    453
                ]
            ],
            "length":0
        },
        {
            "id": 12,
            "points": [
                [
                    1404,
                    466
                ],
                [
                    1540,
                    453
                ]
            ],
            "length":0
        },
        {
            "id":15,
            "points": [
                [
                    738,
                    211
                ],
                [
                    639,
                    198
                ]
            ],
            "length":0
        },
        {
            "id": 3,
            "points": [
                [
                    916,
                    1473
                ],
                [
                    1007,
                    1461
                ]
            ],
            "length":0
        }
    ],
    "labels": [
        {
            "id": 9,
            "points": [
                [
                    732,
                    523
                ],
                [
                    621,
                    475
                ]
            ],
            "text": "1 um",
            "number": 1,
            "unit": "um"
        },
        {
            "id": 16,
            "points": [
                [
                    760,
                    261
                ],
                [
                    611,
                    223
                ]
            ],
            "text": "200 nm",
            "number": 200,
            "unit": "nm"
        },
        {
            "id": 13,
            "points": [
                [
                    1526,
                    474
                ],
                [
                    1414,
                    525
                ]
            ],
            "text": "1 um",
            "number": 1,
            "unit": "um"
        }
    ],
    "meta": {
        "title": "Tailoring Mechanically Robust Poly(m-phenylene isophthalamide) Nanofiber/nets for Ultrathin High-Efficiency Air Filter | Scientific Reports",
        "article_url": "https://www.nature.com/articles/srep40550",
        "image_url": "https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fsrep40550/MediaObjects/41598_2017_Article_BFsrep40550_Fig2_HTML.jpg",
        "license": "http://creativecommons.org/licenses/by/4.0/",
        "openAccess": true
    },
    "width": 1575,
    "height": 1574,
    "ppi":0,   // 如果是整个大图没有固定ppi就设置为0
    "figures": [
        {
            "id": 1,
            "points": [
                [
                    1.9166666666667425,
                    1064.5
                ],
                [
                    1572,
                    1573
                ]
            ],
            "ppi":0
        },
        {
            "id": 4,
            "points": [
                [
                    6.083333333333371,
                    608.25
                ],
                [
                    1574,
                    1056
                ]
            ],
            "ppi":0
        },
        {
            "id": 6,
            "points": [
                [
                    785.25,
                    545.75
                ],
                [
                    7,
                    0
                ]
            ],
            "ppi":0
        },
        {
            "id": 10,
            "points": [
                [
                    793.5833333333335,
                    545.75
                ],
                [
                    1574,
                    0
                ]
            ],
            "ppi":0
        },
        {
            "id": 14,
            "points": [
                [
                    389.41666666666674,
                    279.08333333333337
                ],
                [
                    778,
                    0
                ]
            ],
            "ppi":0
        }
    ],
    "figure_nos":[
        {
            "id": 2,
            "points": [
                [
                    1.9166666666667425,
                    1064.5
                ],
                [
                    100.9166666666667425,
                    1154
                ]
            ],
            "text":"d"
        },
        {
            "id": 5,
            "points": [
                [
                    6.083333333333371,
                    608.25
                ],
                [
                    106,
                    708
                ]
            ],
            "text":"c"
        },
        {
            "id": 7,
            "points": [
                [
                    107,
                    100
                ],
                [
                    7,
                    0
                ]
            ],
            "text":"a"
        },

    ],
    "relations":[
        [1,2,3,0],
        [4,5,0,0],
        [6,7,8,9],
        [14,0,15,16],
    ],
    // "relations":{
    //     "figures":[1,2,3,4,5],   // 他们四者是一一对应的，按照figure来,一个figure下面可能有多个其他的。 但应该只有一个，多个的情况说明有问题。
    //     "figure_nos":[[1],[2],[3],[0],[0]],
    //     "bars":[[4],[0],[1],[2],[3]],    // 一个bar只能对应一个label,
    //     "labels":[[0],[0],[1],[3],[2]],
    // } [10,0,12,13],
}

export const blankStdJson = {
    "name": "",   //如果name 后台请求应该是url路径才对 模拟数据就先从前端取
    "meta": {},
    "width": 0,
    "height": 0,
    "ppi":0,   // 如果是整个大图没有固定ppi就设置为0

    "figures": [],
    "figure_nos":[],
    "bars": [],
    "labels": [],
    "relations":[]
}