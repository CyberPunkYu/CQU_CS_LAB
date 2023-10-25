import re
class predict(object):
    def __init__(self):
        self.bin_word = {}
        self.uni_word = {}
        self.p = {}

    # 从训练集中获取频数
    def  getFrequency(self):
        f = open('news.txt' , mode = 'r' , encoding = 'utf-8-sig')
        for i in f.readlines():
            sentence = re.findall('[\u4e00-\u9fa5]+' , i)
            for words in sentence:
                tmp = ' '
                for word in words:
                    if word in self.uni_word:
                        self.uni_word[word] += 1
                    else:
                        self.uni_word[word] = 1
                    if tmp != ' ':
                        bin = tmp + word
                        if bin in self.bin_word:
                            self.bin_word[bin] += 1
                        else:
                            self.bin_word[bin] = 1
                    tmp = word

    # 加一法
    def smooth(self):
        # 词汇量
        V = len(self.uni_word)
        for key1, v1 in self.uni_word.items():
            self.p[key1] = {}
            for key2 , v2 in self.uni_word.items():
                tmp_k = key1 + key2
                if tmp_k in self.bin_word:
                    self.p[key1][key2] = (1 + self.bin_word[tmp_k]) / (V + self.uni_word[key1])
                else:
                    self.p[key1][key2] = 1 / (V + self.uni_word[key1])
            tmp = sorted(self.p[key1].items(), key = lambda item: -item[1])
            self.p[key1] = {k:v for k, v in tmp}
    def search(self, string):
        kw = string[len(string) - 1]
        # print (kw)
        pre = []
        for k , v in self.p[kw].items():
            pre.append(k)
        print("下一个可能输入的字为")
        print(pre[: 7])
        return pre[ : 7]

if __name__ == '__main__':
    model = predict()
    model.getFrequency()
    model.smooth()
    string  = input("请输入你要搜索的内容:     ")
    pre = model.search(string)
    while(True):
        num = int(input("请从上面五个字中选择你要输入的汉字0-6:     "))
        if num == 7:
            print("已完成输入:     ", string)
            break
        else:
            string += pre[num]
            pre = model.search(string)