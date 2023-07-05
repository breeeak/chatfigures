from elsapy.elsclient import ElsClient, version,logger
from elsapy.elssearch import ElsSearch
import json
import requests
import os
import time
import random
import re
from tqdm import tqdm


def delete_boring_characters(sentence):
    return re.sub('[!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\n]+', "", sentence)

def demo_test():
    ## Load configuration
    con_file = open("config.json")
    config = json.load(con_file)
    con_file.close()

    ## Initialize client
    client = ElsClient(config['apikey'])

    ## Initialize doc search object using ScienceDirect and execute search,
    #   retrieving all results
    doc_srch = ElsSearch("star trek vs star wars", 'sciencedirect')  # 关键词和数据库  sciencedirect和scopus数据库
    # https://www.sciencedirect.com/search?qs=star%20trek%20vs%20star%20wars&show=25&offset=25  参考官网 给的结果是一样的 都是199条

    # get_all 是否得到所有结果
    # count = 每次查询的结果数
    # 轮次查询 直到填满整个结果数目
    doc_srch.execute(client, get_all=True, count=50)
    """
    els_client = None,
    get_all = False, 
    use_cursor = False,
    view = None,
    count = 25,
    fields = []
    
    """
    print("doc_srch has", len(doc_srch.results), "results.")



class ImageScraper:
    def __init__(self, options):
        self.query = None

        self.client = ElsClient(options['apikey'])
        self.search = None
        self.options = options
        self.img_resolution = options["img_resolution"]

        self.used_identifier = [] # 已经访问的identifier列表
        if os.path.exists(options["used_identifier_path"]):
            with open(options["used_identifier_path"], "r") as f:
                for line in f:
                    self.used_identifier.append(line.replace("\n", ""))

        self.base_url = u'https://api.elsevier.com/content/object/pii/'
        self.img_headers = {
            "X-ELS-APIKey": options["apikey"],
            "User-Agent": "elsapy-v%s" % version,
        }
        self.out_root = "query_results"
        if options["out_root"]:
            self.out_root = options["out_root"]
        os.makedirs(self.out_root, exist_ok=True)
        self.out_dir = None

    def get_article_results(self, query):
        print(f"Do query: {query}")
        logger.info(f"Do query ${query}")

        self.query = query
        self.out_dir = os.path.join(self.out_root, delete_boring_characters(self.query))
        os.makedirs(self.out_dir,exist_ok=True)   #如果存在这个路径说明这个查询已经查过了
        os.makedirs(os.path.join(self.out_dir, "imgs"), exist_ok=True)  #
        os.makedirs(os.path.join(self.out_dir, "img_metas"), exist_ok=True)     # 每一图片的meta单独保存
        # 建立查询
        self.search = ElsSearch(self.query, self.options['index'])
        # 执行查询
        self.search.execute(self.client, get_all=self.options["get_all"], count=self.options["count"])

        if self.options["save_ori_json"]:
            out_json_name ="article_results.json"
            with open(os.path.join(self.out_dir, out_json_name), 'w') as f:
                f.write(json.dumps(self.search.results, indent=2))
        return self.search.results

    def download_img(self, result):
        identifier = result["dc:identifier"]
        img_metas = []
        if identifier in self.used_identifier:
            print(f"The article:{identifier} has been required")
            logger.info(f"The article:{identifier} has been required")
            return img_metas
        else:
            print(f"Downloading:{identifier}")
            logger.info(f"Downloading:{identifier}")
            self.used_identifier.append(identifier)
            with open(options["used_identifier_path"], "a") as file:        # 每次都写入访问过的identifier
                file.write(identifier+"\n")
        title = result["dc:title"]
        open_access = result["openaccess"]
        pii = result["pii"]
        # 请求路径如下： https://api.elsevier.com/content/object/pii/S0167527308011704?view=META
        obj_url = self.base_url + pii + "?view=META"
        api_response = self.client.exec_request(obj_url)
        attachments = api_response['attachment-metadata-response']['attachment']
        if len(attachments) > 0:
            for attachment in attachments:
                if attachment["type"] == self.img_resolution:
                    img_url = attachment["prism:url"]
                    eid = attachment["eid"]
                    width = attachment["width"]
                    height = attachment["height"]
                    name = ".".join(str(eid).split(".")[:-1])
                    # 进行下载
                    try:
                        print(f"Downloading img {img_url}")
                        logger.info('Sending GET request to ' + img_url)
                        download_r = requests.get(img_url, headers=self.img_headers)
                        download_r.raise_for_status()
                        with open(os.path.join(self.out_dir, "imgs",eid), "wb+") as temp:
                            temp.write(download_r.content)

                        img_meta = {"name": eid, "width": width, "height": height, "identifier": identifier,
                                    "title": title, "img_url": img_url, "article_url": obj_url,
                                    "open_access": open_access
                                    }
                        with open(os.path.join(self.out_dir, "img_metas", name + ".json"), "w+") as temp:
                            temp.write(json.dumps(img_meta, indent=2))
                    except Exception as e:
                        print(f"Downloading img error{e}")
                        continue





if __name__ == '__main__':
    used_identifier_path = "used_identifier.txt"
    query_list_path = "query_list.txt"
    ## Load configuration
    con_file = open("config.json")
    config = json.load(con_file)
    con_file.close()
    options = {
        "apikey": config['apikey'],
        "index": "sciencedirect",
        "get_all": True,
        "count": 50,
        "save_ori_json": True,
        "used_identifier_path": used_identifier_path,
        "out_root": None,
        "img_resolution": "IMAGE-HIGH-RES"
    }
    # IMAGE-THUMBNAIL (smallest), IMAGE-DOWNSAMPLED (regular), and IMAGE-HIGH-RES (high resolution)

    isp = ImageScraper(options)
    query_list = []
    with open(query_list_path, "r") as f:
        for line in f:
            query_list.append(line.replace("\n", ""))
    for query in tqdm(query_list):
        try:
            article_results = isp.get_article_results(query)
        except Exception as e:
            print(f"error {e} for query {query}")
            logger.error(f"error {e} for query {query}")
            continue
        for article_result in tqdm(article_results):
            # time.sleep(random.randint(1, 10))  # 每一篇文章停止一段时间再访问 防止被封
            try:
                isp.download_img(article_result)
            except Exception as e:
                print(f"error {e} for img download")
                logger.error(f"error {e} for img download")

