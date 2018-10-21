import argparse
import gensim
import os
import konlpy
import tqdm
from chardet.universaldetector import UniversalDetector
tagger = konlpy.tag.Mecab()
detector = UniversalDetector()


class doc2wv(object):
    def __init__(self):
        self.model = None
        # parameter for gensim word2vec
        '''
        아래 파라메타들은 gensim에서 word2vec을 수행하기 위한 기본 인지값들.
        '''
        self.window = 5
        self.worker = 4
        self.size = 300
        self.min_count = 5

    def build_model(self, list_dir, model_name, **kwargs):
        file_list = os.listdir(list_dir)
        pos_lines =[]
        for file in file_list:
            file_name = os.path.join(list_dir, file)
            detector.reset()
            lines = open(file_name, "rb")
            for line in lines :
                detector.feed(line)
                if detector.done: break
                detector.close()
            lines.close()
            lines = open(file_name, "r", encoding=detector.result["encoding"])

            for line in lines:
                pos_line = tagger.pos(line)
                pos_line = pos_line[1:-2]
                pos_line = " ".join(["/".join(element) for element in pos_line])
                pos_lines.append(pos_line)

        '''
        kwargs로 인자를 받으면 입력 받은 인자를 사용한다.
        그렇지 않을 때 클래스 정의에 있는 인자를 사용
        '''
        if "window" in kwargs:
            self.window = kwargs["window"]
        if "worker" in kwargs:
            self.worker = kwargs["worker"]
        if "size" in kwargs:
            self.size = kwargs["size"]
        if "min_count" in kwargs:
            self.min_count = kwargs["min_count"]

        self.model = gensim.models.Word2Vec(pos_lines, size=self.size, window=self.window,
                                            min_count=self.min_count, workers=self.worker)
        self.model.save(model_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("list_dir",    type=str, default="./dataset", help="path for dataset")
    parser.add_argument("model_name",  type=str, default="./model", help="model name for word2vec model")
    parser.add_argument("--window",    type=int, default=5, help="gensim word2vec window size")
    parser.add_argument("--worker",    type=int, default=4, help="gensim word2vec worker count")
    parser.add_argument("--size",      type=int, default=300, help="gensim word2vec size ")
    parser.add_argument("--min_count", type=int, default=5, help="gensim word2vec df min count")
    args = parser.parse_args()

    model = doc2wv()
    model.build_model(list_dir=args.list_dir,
                      model_name=args.model_name,
                      window=args.window,
                      worker=args.worker,
                      size=args.size,
                      min_count=args.min_count)