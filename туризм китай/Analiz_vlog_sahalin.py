#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
df = pd.read_excel('Sahalin_g3.xlsx', header=None, names=['Заголовок', 'Ссылка'])

df.head(5)


# In[4]:


import re 

def clean(text):
    if not isinstance(text, str):
        return ''
    text = re.sub(r'[^\u4e00-\u9fff\w\s]', '', text)
    return re.sub(r'\s+', '', text).strip()

df['Заголовок чистый'] = df['Заголовок'].apply(clean)


# In[5]:


import jieba as j

cleaned = ''.join(df['Заголовок чистый'].dropna())
char = j.lcut(cleaned)

sw = {'萨哈林', '库页岛', '俄罗斯'}
filtered = [c for c in char if len(c)>1 and c not in sw]
cloud = ' '.join(filtered)


# In[7]:


from wordcloud import WordCloud #само облако слов
import matplotlib.pyplot as plt #для визуализации

wc = WordCloud(font_path='NotoSansSC-Regular.ttf', 
               background_color='white', 
               width=1200, height=600, 
               colormap='Reds').generate(cloud)

plt.figure(figsize=(14, 7))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('Облако слов: Сахалин в Китайском медиа', fontsize=18, pad=20)
plt.tight_layout()
plt.show()
#colormap='viridis'   фиолетово-жёлтая
#colormap='plasma'    оранжево-розовая
#colormap='Blues'     голубая палитра
#colormap='Greens'    зелёная палитра
#colormap='Wistia'    жёлто-оранжевая
#colormap='magma'     оранжевая + черная


# In[7]:


from collections import Counter

w_count = Counter(filtered)
top10 = w_count.most_common(10)
df_top = pd.DataFrame(top10, columns=['Название', 'Частота'])

import matplotlib.font_manager as fm

fontRU = fm.FontProperties(fname='NotoSans-Regular.ttf')
fontCH = fm.FontProperties(fname='NotoSansSC-Regular.ttf')

plt.figure(figsize=(10, 6))
plt.bar(df_top['Название'], df_top['Частота'], color='#CD5C5C')
plt.xticks(fontproperties=fontCH)
y = df_top['Частота'].max()
plt.yticks(range(0, y + 1))
plt.title('Топ 15', fontproperties=fontRU, fontsize=14)
plt.xlabel('Частота', fontproperties=fontRU)
plt.tight_layout()
plt.show()


# In[8]:


d = {
    'Маяк': ['阿尼瓦', '灯塔', '灯台'],
    'Южно-Сахалинск': ['南萨哈林斯克', '南萨'],
    'Музей': ['博物馆', '地方志'],
    'Горы': ['契诃夫峰', '巨人角', '徒步'],
    'История и Политика': ['故土', '石碑', '日本', '历史', '主权', '日治', '中华'],
    'Природа и Животные': ['棕熊', '海狮', '帝王蟹', '森林', '海边', '秋天', '冬天'],
    'Острова' : ['岛屿', '北方四岛', '巨人島', '南千岛群岛', '千岛群岛']
}

ment = {}

for key, objectt in d.items():
    count = 0
    for title in df['Заголовок чистый']:
        for obj in objectt:
            if obj in title:
                count = count + 1
                break
    ment[key] = count

plt.figure(figsize=(8, 8))
plt.pie(ment.values(), 
        labels = ment.keys(), 
        autopct='%1.0f%%', 
        colors= ['#CD5C5C', '#F08080', '#FA8072', '#E9967A', '#FFA07A', '#F4A460', '#F0143C'])
plt.title('Распределение упоминаний')
plt.show()


# In[ ]:





# In[ ]:




