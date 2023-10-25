import re
import numpy as np
import pypinyin


'''HMM模型'''
class HMM(object):

    '''初始化函数'''

    def __init__(self, ):
        self.init_pro = {}  # 初始概率
        self.emiss_pro = {}  # 发射概率
        self.trans_pro = {}  # 转移概率
        self.pinyin_to_chinese = {}  # 拼音字典


    '''获得拼音字典函数'''
    def get_pinyin_dict(self, pinyin2hanzi_path):
        f = open(pinyin2hanzi_path, encoding='utf-8')
        #按行读取
        for line in f.readlines():
            #将每行拼音与汉字之间的零宽/不换行/空格换为普通空格
            line = re.sub(r'[\ufeff]', '', line)
            #将每行按空格切分并放入line列表中，一共两个部分，line[0]为拼音，line[1]为对应汉字
            line = line.strip().split()
            #存入拼音字典
            self.pinyin_to_chinese[line[0]] = line[1]
        f.close()

    '''训练初始概率/转移概率函数'''
    def train_init_trans_pro(self, toutiao_path,):
        f = open(toutiao_path, encoding='utf-8')

        single_word = {} #存放单个词的频数
        double_word = {} #存放两个词的频数
        num = 0

        for line in f.readlines():
            temp = re.findall('[\u4e00-\u9fa5]+', line)
            for words in temp:
                pre = ' '
                for word in words:
                    #计算单个词的频数
                    if word in single_word:
                        single_word[word] += 1
                    else:
                        single_word[word] = 1
                    #计算两个词的频数
                    if pre != ' ':
                        if pre+word in double_word:
                            double_word[pre+word] += 1
                        else:
                            double_word[pre+word] = 1
                    pre = word
                num += 1
        f.close()

        #求初始概率
        for i in single_word.keys():
            #为避免出现概率过小，可取对数运算：
            # self.init_pro[i] = np.log(single_word[i]/num)
            self.init_pro[i] = single_word[i]/num

        #求转移概率
        for i in double_word:
            # self.trans_pro[i] = np.log(double_word[i]/single_word[i[0]])
            self.trans_pro[i] = double_word[i]/single_word[i[0]]


    '''汉字转拼音函数'''
    def word2pinyin(self, text):
        py = pypinyin.lazy_pinyin(text)
        return py


    '''训练发射概率函数'''
    def train_emiss_pro(self, toutiao_path):
        f = open(toutiao_path, encoding='utf-8')

        for line in f.readlines():
            temp = re.findall('[\u4e00-\u9fa5]+', line)
            for words in temp:
                ans = self.word2pinyin(words)
                for i in range(len(ans)):
                    if ans[i] not in self.emiss_pro:
                        self.emiss_pro[ans[i]] = {}
                        self.emiss_pro[ans[i]][words[i]] = 1
                    else:
                        if words[i] not in self.emiss_pro[ans[i]]:
                            self.emiss_pro[ans[i]][words[i]] = 1
                        else:
                            self.emiss_pro[ans[i]][words[i]] += 1
        f.close()

        for key in self.emiss_pro:
            s = sum(self.emiss_pro[key].values())
            for key2 in self.emiss_pro[key]:
                # self.emiss_pro[key][key2] = np.log(self.emiss_pro[key][key2]/s)
                self.emiss_pro[key][key2] = self.emiss_pro[key][key2]/s


    '''维特比算法'''
    def viterbi(self, word_list, pinyin_list, n, id2word, label_list):
        """
        维特比算法求解最大路劲问题
        :param word_list: 每个拼音对应的隐藏状态矩阵
        :param n: 可能观察到的状态数，对应为汉字数量
        :param id2word: id到汉字的映射
        :return:
        """
        T = len(word_list) #观察状态的长度

        delta = np.zeros((T, n))
        #保存转移下标值
        psi = np.zeros((T, n), dtype=int)

        #初始化第一个字符的转移概率，设置为每个词在词典中的单独出现的概率
        words = word_list[0]
        for w in words:
            if id2word[w] not in self.init_pro:
                delta[0][w] = 0
            else:
                delta[0][w] = self.init_pro[id2word[w]]

        #动态规划计算
        for idx in range(1, T):
            words = word_list[idx]
            for i in range(len(words)):
                max_value = 0
                pre_words = word_list[idx-1]
                index = 0
                for j in range(len(pre_words)):
                    tmp_key = id2word[pre_words[j]] + id2word[words[i]]
                    # 获得转移概率，如果不存在，则转移概率为0
                    if tmp_key in self.trans_pro:
                        prob = self.trans_pro[tmp_key]
                    else:
                        prob = 0

                    tmp_value = delta[idx-1][pre_words[j]] * prob

                    if max_value < tmp_value:
                        max_value = tmp_value
                        index = j

                # 计算观察状态到隐藏状态的概率
                # tmp_key = id2word[words[i]] + pinyin_list[idx]
                if pinyin_list[idx] not in self.emiss_pro:
                    emit_prob = 0
                elif id2word[words[i]] not in self.emiss_pro[pinyin_list[idx]]:
                    emit_prob = 0
                else:
                    emit_prob = self.emiss_pro[pinyin_list[idx]][id2word[words[i]]] * max_value

                delta[idx][words[i]] = emit_prob
                psi[idx][words[i]] = pre_words[index]

        prob = 0
        path = np.zeros(T, dtype=int)
        path[T-1] = 1
        #获取最大的转移至
        for i in range(n):
            if prob < delta[T-1][i]:
                prob = delta[T-1][i]
                path[T-1] = i

        #最优路径回溯
        for t in range(T-2, -1, -1):
            path[t] = psi[t+1][path[t+1]]

        #生成解析结果
        final_word = ""
        a = 0
        for i in range(T):
            final_word += id2word[path[i]]
            if id2word[path[i]] == label_list[i]:
                a += 1

        print('原句：', label_list)
        print('转换：', final_word)
        print('准确率：', a*1.0/T)
        print('\n')


    '''测试函数'''
    def accuracy(self, test_path,):
        f = open(test_path, encoding='gb2312')
        lines = f.readlines()

        flag = 1
        pinyin = []
        label = []
        for line in lines:
            if flag == 1:
                line = line.lower()
                line = line.split()
                pinyin.append(line)
                flag = 0
            else:
                label.append(line.strip('\n'))
                flag = 1

        for i in range(len(pinyin)):
            pinyin_list = pinyin[i]
            label_list = label[i]

            word_list = []
            for i in pinyin_list:
                temp = re.findall(r'[\u4200-\u9fa5]', self.pinyin_to_chinese[i])
                word_list.append(temp)

            words = set()
            for wl in word_list:
                for w in wl:
                    words.add(w)

            word2idx = dict()
            id2word = dict()
            idx = 0
            for w in words:
                word2idx[w] = idx
                id2word[idx] = w
                idx += 1

            # 将各个汉字转化为id表示
            word_id_list = [None] * len(word_list)
            for i,wl in enumerate(word_list):
                word_id_list[i] = [None] * len(wl)
                for j,w in enumerate(wl):
                    word_id_list[i][j] = (word2idx[w])


            self.viterbi(word_id_list, pinyin_list, len(words), id2word, label_list,)


'''主函数'''
if __name__=='__main__':
    pinyin2hanzi_path = "C:/Users/DELL/Desktop/助教/Test1/pinyin2hanzi.txt" #路径，用/区分块 pinyin2hanzi.txt
    toutiao_path = "C:/Users/DELL/Desktop/助教/Test1/toutiao_cat_data.txt" #toutiao_cat_data.txt
    test_path = "C:/Users/DELL/Desktop/助教/Test1/test.txt" #测试集.txt
    hmm = HMM()
    hmm.get_pinyin_dict(pinyin2hanzi_path)
    hmm.train_init_trans_pro(toutiao_path)
    hmm.train_emiss_pro(toutiao_path)
    hmm.accuracy(test_path)


