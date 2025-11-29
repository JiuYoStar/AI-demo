import pandas as pd
from sklearn.metrics.pairwise import linear_kernel  # → 计算余弦相似度
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import matplotlib.pyplot as plt
import os
from constants import ENGLISH_STOPWORDS

pd.options.display.max_columns = 30

# 支持中文
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签

# 读取数据 + 探索
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "Seattle_Hotels.csv")
df = pd.read_csv(csv_path, encoding="latin-1")

print(df.head())
print("数据集中的酒店个数：", len(df))

def print_description(index):
    example = df[df.index == index][["desc", "name"]].values[0]
    if len(example) > 0:
        print(example[0])
        print("Name:", example[1])


print("第10个酒店的描述：")
print_description(10)


# 得到酒店描述中n-gram特征中的TopK个
def get_top_n_words(corpus, n=1, k=None):
    # 统计ngram词频矩阵，使用自定义停用词列表 → 词频统计
    vec = CountVectorizer(ngram_range=(n, n), stop_words=list(ENGLISH_STOPWORDS)).fit(
        corpus
    )
    bag_of_words = vec.transform(corpus)
    """
    print('feature names:')
    print(vec.get_feature_names())
    print('bag of words:')
    print(bag_of_words.toarray())
    """
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    print(f"{words_freq} <<< n-gram 在所有酒店描述中出现的次数")
    # 按照词频从大到小排序
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:k]


common_words = get_top_n_words(df["desc"], n=3, k=20)
print(common_words)


df1 = pd.DataFrame(common_words, columns=["desc", "count"])
df1.groupby("desc").sum()["count"].sort_values().plot(
    kind="barh", title="去掉停用词后，酒店描述中的Top20单词"
)

# plt.show() 👉🏻 可视化

# 文本预处理
REPLACE_BY_SPACE_RE = re.compile(r"[/(){}\[\]\|@,;]")
BAD_SYMBOLS_RE = re.compile("[^0-9a-z #+_]")
# 使用自定义的英文停用词列表替代nltk的stopwords
STOPWORDS = ENGLISH_STOPWORDS


# 对文本进行清洗
def clean_text(text):
    # 全部小写
    text = text.lower()
    # 用空格替代一些特殊符号，如标点
    text = REPLACE_BY_SPACE_RE.sub(" ", text)
    # 移除BAD_SYMBOLS_RE
    text = BAD_SYMBOLS_RE.sub("", text)
    # 从文本中去掉停用词
    text = " ".join(word for word in text.split() if word not in STOPWORDS)
    return text


# 对desc字段进行清理，apply针对某列
df["desc_clean"] = df["desc"].apply(clean_text)
# print(df['desc_clean'])

# 建模
df.set_index("name", inplace=True)
# 使用TF-IDF提取文本特征，使用自定义停用词列表
tf = TfidfVectorizer(
    analyzer="word", ngram_range=(1, 3), min_df=0.01, stop_words=list[str](ENGLISH_STOPWORDS)
)
# 针对desc_clean提取tfidf
tfidf_matrix = tf.fit_transform(df["desc_clean"])
print("TFIDF feature names:")
# print(tf.get_feature_names_out())
print(len(tf.get_feature_names_out()))
print('tfidf_matrix:', tfidf_matrix)
print(tfidf_matrix.shape)
# 计算余弦相似度（线性核函数）
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
# print(cosine_similarities)
print(cosine_similarities.shape)
indices = pd.Series(df.index)  # df.index是酒店名称


# 基于相似度矩阵和指定的酒店name，推荐TOP10酒店
def recommendations(name, cosine_similarities=cosine_similarities):
    recommended_hotels = []
    # 找到想要查询酒店名称的idx
    idx = indices[indices == name].index[0]
    print("idx=", idx)
    # 对于idx酒店的余弦相似度向量按照从大到小进行排序
    score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending=False)
    # 取相似度最大的前10个（除了自己以外）
    top_10_indexes = list(score_series.iloc[1:11].index)
    # 放到推荐列表中
    for i in top_10_indexes:
        recommended_hotels.append(list(df.index)[i])
    return recommended_hotels


print(recommendations("Hilton Seattle Airport & Conference Center"))
print(recommendations("The Bacon Mansion Bed and Breakfast"))
