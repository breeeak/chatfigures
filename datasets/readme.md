# 

## The largest figure separation and label extraction dataset !



### Introduction

The dataset contains 13,462 images with more than 160,000 annotated objects, including bounding boxes and text annotations of subfigures and subfigure labels. Images in this dataset are from the ImageCLEF 2016 dataset and scientific publications. 



As far as we know, this is the largest compound figure separation and label recognition dataset. 

Considering copyright issues, we do not provide the images but their original downloading links and annotations.  If the image does not have a downloading link, we provide the original image.

> For ImageCLEF 2016 you can follow the instruction of the official website to get the images.
>
> https://www.imageclef.org/2016/medical
>
> For the downloading links, if you want to download the image, please follow the instruction of ScienceDirect TDM. 
>
> https://www.elsevier.com/about/policies/text-and-data-mining

 

### Labelling rules

**Approach 1**) decomposing compound figures into the smallest possible figures; **Approach 2**) decomposing compound figures according to the indices (subfigure labels, i.e., "A", "a", "1", "III", etc.).   

Both approaches are adopted.  The relationships between subfigures and subfigure labels are also annotated. It should be noted that many subfigures are overlapped, and the size of the subfigures and subfigure labels varies greatly in this dataset. 

This dataset can be used for object detection, text detection and text recognition.

**Dense overlapped and small object detection**



### Example

``` json
{
  "name": "1471-213X-11-45-2.jpg",
  "meta": {
    "source": "ImageCLEF2016_train"		
  },
  "width": 600,
  "height": 582,
  "figures": [
    {
      "points": [
        [
          403.8020324707031,
          2.097679376602173
        ],
        [
          600,
          176.4241943359375
        ]
      ],
      "id": 1
    },
    {
      "points": [
        [
          211.2995147705078,
          2.6916658878326416
        ],
        [
          393.2584228515625,
          175.1217498779297
        ]
      ],
      "id": 2
    },
    ...
  ],
  "figure_nos": [
    {
      "points": [
        [
          215.65261840820312,
          7.590041160583496
        ],
        [
          233.61407470703125,
          30.53278350830078
        ]
      ],
      "id": 5,
      "text": "b",
    },
    {
      "points": [
        [
          407.72491455078125,
          7.423089981079102
        ],
        [
          426.86553955078125,
          30.454816818237305
        ]
      ],
      "id": 6,
      "text": "c",
    },
    ...
  ],
  "relations": [
    [
      1,
      6,
      0,
      0
    ],
    [
      2,
      5,
      0,
      0
    ],
    ...
  ]
}
another example
"meta": {
    "open_access": false,
    "article_url": "https://api.elsevier.com/content/object/pii/B9780128044537000318?view=META",
    "img_url": "https://api.elsevier.com/content/object/eid/3-s2.0-B9780128044537000318-bm96-9780128044537.jpg?httpAccept=%2A%2F%2A",
    "title": "Appendix: Figures, Charts, Graphs, and Surveys",
    "identifier": "DOI:10.1016/B978-0-12-804453-7.00031-8",
    "source": "ScienceDirectTDM"
},

```

### Download

dataset download link: [onedrive](https://portland-my.sharepoint.com/:u:/g/personal/shuomeng2-c_my_cityu_edu_hk/EZEbSfiIb-5Kkp0uI2aR7rEBwOX3snh6hz22eapyFlnvkg?e=Y33AFL)


If you have any question, please email to shoumeng2-c@my.cityu.edu.hk









