# coding=utf-8
import os
import sys
import joblib
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Input, GlobalMaxPooling1D
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Embedding
from tensorflow.keras.models import Model
from tensorflow.keras.initializers import Constant
from tensorflow.keras.callbacks import ModelCheckpoint
import moxing as mox
import argparse

# BASE_DIR = 'G:\\trainingdata'


parser = argparse.ArgumentParser(description='CNN Example')
parser.add_argument('--data_url', type=str, default="./Data",
                    help='path where the dataset is saved')
parser.add_argument('--train_url', type=str, default="./Model", help='model path')
args = parser.parse_args()
# BASE_DIR为训练集根目录，这里设置为桶的dataset目录
BASE_DIR = args.data_url


# 文本语料路径
TEXT_DATA_DIR = os.path.join(BASE_DIR, '20_newsgroup')
MAX_SEQUENCE_LENGTH = 1000
MAX_NUM_WORDS = 20000
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.2

# 将词变为词向量
print('Indexing word vectors.')
print(TEXT_DATA_DIR)
embeddings_index = {}
with open(os.path.join(BASE_DIR, 'glove.6B.100d.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        word, coefs = line.split(maxsplit=1)
        coefs = np.fromstring(coefs, 'f', sep=' ')
        embeddings_index[word] = coefs

texts = []  # list of text samples
labels_index = {}  # dictionary mapping label name to numeric id
labels = []  # list of label ids
for name in sorted(os.listdir(TEXT_DATA_DIR)):
    path = os.path.join(TEXT_DATA_DIR, name)
    if os.path.isdir(path):
        label_id = len(labels_index)
        labels_index[name] = label_id
        for fname in sorted(os.listdir(path)):
            if fname.isdigit():
                fpath = os.path.join(path, fname)
                args = {} if sys.version_info < (3,) else {'encoding': 'latin-1'}
                with open(fpath, **args) as f:
                    t = f.read()
                    i = t.find('\n\n')  # skip header
                    if 0 < i:
                        t = t[i:]
                    texts.append(t)
                labels.append(label_id)
print('Found %s texts.' % len(texts))

tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
word_index = tokenizer.word_index
joblib.dump(tokenizer, 'token_result.pkl')

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
print(data)
labels = to_categorical(np.asarray(labels))
print(labels)
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)
indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
print(data)
labels = labels[indices]
print(labels)
num_validation_samples = int(VALIDATION_SPLIT * data.shape[0])
print(data.shape[0])
x_train = data[:-num_validation_samples]
y_train = labels[:-num_validation_samples]
x_val = data[-num_validation_samples:]
y_val = labels[-num_validation_samples:]

print('Preparing embedding matrix.')
num_words = min(MAX_NUM_WORDS, len(word_index) + 1)
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, i in word_index.items():
    if i >= MAX_NUM_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        # 从预训练模型的词向量到语料库的词向量映射
        embedding_matrix[i] = embedding_vector

embedding_layer = Embedding(num_words,
                            EMBEDDING_DIM,
                            embeddings_initializer=Constant(embedding_matrix),
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)
print('Training model.')

sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedded_sequences = embedding_layer(sequence_input)

#请从此开始补充定义CNN和LSTM模型

# Your codes
model = keras.Sequential([
  embedding_layer,
  keras.layers.Conv1D(128, 5, activation='relu'),
  keras.layers.MaxPooling1D(5),
  keras.layers.Conv1D(128, 5, activation='relu'),
  keras.layers.MaxPooling1D(5),
  keras.layers.Conv1D(128, 5, activation='relu'),
  keras.layers.GlobalMaxPooling1D(),
  keras.layers.Dense(64, activation='relu'),
  keras.layers.Dropout(0.5),
  keras.layers.Dense(20, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#补充代码ending


history = model.fit(x_train, y_train,
                    batch_size=128,
                    epochs=2,
                    validation_data=(x_val, y_val))

# 先在虚拟机上保存模型，再将模型拷贝至桶的输出路径下。
Model_DIR = os.path.join(os.getcwd(), 'mytextcnn_model.h5')
model.save(Model_DIR)
print('Saved model to disk'+Model_DIR)
# 第二个参数需要根据实验者的桶路径修改
mox.file.copy_parallel(Model_DIR,'obs://bucket-gp/proj-one/model/mytextcnn_model.h5')
