import re

class Hmm_model(object):
    def __init__(self):
        self.init_p = {}     #初始概率
        self.emis_p = {}     #发射概率
        self.tran_p = {}     #转换概率
        self.pinyin_dict = {}#拼音字典
        self.uni_word = {}   #字频数字典
        self.bin_word = {}   #词频数字典
        self.cnt = 0         #所有字的总数
        self.global_right_word = 0      #全局匹配正确字个数
        self.global_right_sentence = 0  #全局全局匹配正确个数
        self.global_words = 0
        self.global_sentences = 0

    #将每个拼音对应的字分别储存起来，在拼音转汉字时使用
    def getPinyin_dict(self):
        f = open('C:\\homework\\up3\\NLP\\LAB\\LAB1\\matertial\\pinyin2hanzi.txt', mode = 'r', encoding = 'utf-8-sig') #utf--sig可以除去开头\ufeff的BOM
        for i in f.readlines():
            i = i.strip().split()  #将每一行按照空格分开
            self.pinyin_dict[i[0]] = i[1] #得到拼音字典
        f.close()

    #从训练集中获取每个字和二字词出现的频数
    def getFrequency(self):
        f = open('C:\\homework\\up3\\NLP\\LAB\\LAB1\\matertial\\toutiao_cat_data.txt', mode = 'r', encoding = 'utf-8-sig')
        #填充频数字典
        for i in f.readlines():
            #正则表达式从读取的每一行匹配中文字符，其中中文字符按照原句中的其他非中文字符分割
            sentence = re.findall('[\u4e00-\u9fa5]+' , i)
            for words in sentence:
                prefix = ' '    
                for word in words:
                    #填充字频数字典
                    if word in self.uni_word:
                        self.uni_word[word] += 1
                    else:
                        self.uni_word[word] = 1
                    #填充词频数字典
                    if prefix != ' ':
                        tmp = prefix + word
                        # print(tmp)
                        if tmp in self.bin_word:
                            self.bin_word[tmp] += 1
                        else:
                            self.bin_word[tmp] = 1
                    #上一个词的结尾变为下一词的开头
                    prefix = word
                    self.cnt += 1

    #训练初始概率和转移概率
    def train1(self):
        # print(self.uni_word)
        for k , v in self.uni_word.items():
            # print(k , v)
            #初始概率为每一个字占总字数的比例
            self.init_p[k] = v / self.cnt
        for k , v in self.bin_word.items():
            # print(k , v)
            #对于一个词里面的转移概率（前一个字转到下一个字）等于该词出现的次数比第一个字出现的次数
            self.tran_p[k] = v / self.uni_word[k[0]]

    #训练发射概率
    #这里的发射概率我们直接从拼音字典中采用简单平均
    def train2(self):
        # key为拼音  value为该拼音对应的汉字
        for k , v in self.pinyin_dict.items():
            for i in range(len(v)):
                if v[i] not in self.emis_p:
                    self.emis_p[v[i]] = {}
                    self.emis_p[v[i]][k] = 1
                else:
                    if k not in self.emis_p[v[i]]:
                        self.emis_p[v[i]][k] = 1
                    else:
                        self.emis_p[v[i]][k] += 1
        # 现已经得到了每一个字有哪些读音，接下来对每个字的每一个读音求概率
        # print(self.emis_p)
        for k , v in self.emis_p.items():
            total = sum(v.values())
            for k1 , v1 in v.items():
                self.emis_p[k][k1] = self.emis_p[k][k1] / total

    # 维特比算法
    def viterbi(self, pinyin, label):
        """
        pinyin: 要转换的拼音，放在数组中
        label:  正确语句
        """

        # 总共有T个时刻
        T = len(pinyin)
        # 每一个时刻最大的状态数
        q = max(len(self.pinyin_dict[pinyin[i]]) for i in range(T))
        # 创建动态规划表  q行T列
        dp = [[0 for col in range(q)] for row in range(T)]
        MAXi = [[0 for col in range(q)] for row in range(T)]

        # 初始化
        for n in range(len(self.pinyin_dict[pinyin[0]])):
            if self.pinyin_dict[pinyin[0]][n] not in self.init_p:
                dp[0][n] = 0
            else:
                emis_pro = self.emis_p[self.pinyin_dict[pinyin[0]][n]][pinyin[0]]
                init_pro = self.init_p[self.pinyin_dict[pinyin[0]][n]]
                # print(emis_pro)
                # print(init_pro)
                dp[0][n] = emis_pro * init_pro

        for i in range(1 , T):
            word_list = self.pinyin_dict[pinyin[i]]
            j_max = len(word_list)
            for j in range(j_max):
                MAX = 0
                # 回溯标记
                fla = 0
                # 计算发射概率
                emis_pro = self.emis_p[word_list[j]][pinyin[i]]
                # print("emis: " + str(emis_pro))
                pre_words = self.pinyin_dict[pinyin[i-1]]
                # 计算转移概率
                for k in range(len(pre_words)):
                    bin_word = pre_words[k] + word_list[j]
                    # print(bin_word)
                    # 如果这两个字没有连续出现
                    if bin_word not in self.tran_p:
                        tran_pro = 0
                    else:
                        tran_pro = self.tran_p[bin_word]
                    # print("tran: " + str(tran_pro))
                    TMP = tran_pro * dp[i-1][k] * emis_pro

                    if TMP > MAX:
                        MAX = TMP
                        fla = k
                dp[i][j] = MAX
                MAXi[i][j] = fla
        # print(dp)
        # 开始回溯
        seq = [0] * T
        tmp_p = 0
        seq[T - 1] = 1

        for i in range(q):
            if tmp_p < dp[T - 1][i]:
                tmp_p = dp[T - 1][i]
                seq[T - 1] = i
        # 从后往前回溯
        for j in range(T - 2 , -1 , -1):
            seq[j] = MAXi[j + 1][seq[j + 1]]

        final_word = ""
        right_word = 0
        right_sentence = 1
        self.global_words += T
        self.global_sentences += 1
        for k in range(T):
            final_word += self.pinyin_dict[pinyin[k]][seq[k]]
            if self.pinyin_dict[pinyin[k]][seq[k]] == label[k]:
                right_word += 1
                self.global_right_word += 1
            else:
                right_sentence = 0
        self.global_right_sentence += right_sentence
        
        print('原句：', label)
        print('转换：', final_word)
        print('该句准确率：{:.4f}'.format(right_word*1.0/T))
        print('\n')

    def test(self):
        # 这里用GDK编码打开是因为utf-8会出现乱码
        f = open('C:\\homework\\up3\\NLP\\LAB\\LAB1\\matertial\\testset.txt', mode = 'r', encoding = 'gbk')  
        lines = f.readlines()
        # 分别存放测试拼音和对应语句
        pinyin_list = []
        label_list  = []
        # 标记读取的是拼音还是汉字
        mark = 0;
        for line in lines:
            # 如果读取的拼音
            if not mark:
                # 将拼音按照空格分开
                line = line.lower()
                pinyin_list.append(line.split())
                mark = 1
            else:
                label_list.append(line.strip('\n'))
                mark = 0
        # 开始逐条测试
        for i in range(len(pinyin_list)):
            pinyin = pinyin_list[i]
            label  = label_list[i]
            self.viterbi(pinyin , label)

        print("--------------test finished--------------")
        print("全局句准确率为： {:.5f}".format(self.global_right_sentence / self.global_sentences))
        print("全局字准确率为： {:.5f}".format(self.global_right_word / self.global_words))

if __name__ == '__main__':
    # test = ['wo','ai','zhong','guo']
    # test1= "我爱中国"
    hmm = Hmm_model()
    hmm.getPinyin_dict()
    hmm.getFrequency()
    hmm.train1()
    hmm.train2()
    # hmm.viterbi(test, test1)
    hmm.test()
    