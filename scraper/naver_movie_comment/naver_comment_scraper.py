
import argparse
import requests
import lxml.html
import lxml.etree as etree
from Comment import MovieComment
import datetime

def elements2list(elements, mc_list):
    for idx, element in enumerate(elements) :
        subroot = lxml.html.fromstring(etree.tostring(element, encoding="unicode"))
        no = subroot.xpath('//td[@class="ac num"]')
        if len(no) == 0:
            # table의 첫번째 row가 타이틀로 표시 되는 경우가 많음
            continue
        no = no[0].text.strip()
        score = subroot.xpath('//td[@class="point"]')[0].text.strip()
        movie_name = subroot.xpath('//td[@class="title"]/a[@class="movie"]')[0].text.strip()
        comment = etree.tostring(subroot.xpath('//td[@class="title"]/br')[0], encoding="unicode")
        comment = comment.replace("<br/>","").replace("&#13;","\n").strip()
        mc= MovieComment()
        mc.no = no
        mc.score = score
        mc.movie_name = movie_name
        mc.comment = comment
        mc_list.append(mc)


def get_naver_comment_element(idx):
    site = "https://movie.naver.com/movie/point/af/list.nhn?&page={}".format(idx)
    res = requests.get(site)
    root = lxml.html.fromstring(res.text)
    elements = root.xpath("//table[@class='list_netizen']//tr")
    mc_list = []
    elements2list(elements, mc_list)
    import json
    json_list = []
    for mc in mc_list:
        json_list.append(json.dumps(mc.dict, ensure_ascii=False))

    filename1 = "./dataset/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".json"
    comment_file_pt = open(filename1, "w")
    for entry in json_list:
        comment_file_pt.write(entry)
        comment_file_pt.write("\n")
    comment_file_pt.close()



from time import sleep
from tqdm import tqdm, trange

def do_process(args):
    for i in tqdm(range(args.begin, args.end)):
        get_naver_comment_element(i)
        sleep(10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("begin", type=int, default=0, help="begin number of naver comment index")
    parser.add_argument("end", type=int, default=10, help="end number of naver commment index")
    # parser.add_argument("step", type=int, help="how many element to save")
    args = parser.parse_args()
    do_process(args)
