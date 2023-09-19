

import re
from nltk.stem import SnowballStemmer
import numpy as np
import nltk 
# nltk.download('stopwords')
# We filter out the english language stopwrds
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
stop_words = stopwords.words('english')
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
lem=WordNetLemmatizer()


def clean_tweets(text):
  # Text passed to the regex equatio
  text_cleaning_regex = r'@[A-Za-z0-9]+|https?:\/\/\S+|[#]+|RT[\s]+|[0-9]+|[^A-Za-z\s]+|\s+'
  text = re.sub(text_cleaning_regex, ' ', str(text).lower()).strip()
  # Empty list created to store final tokens
  tokens = []
  for token in text.split():
    # check if the token is a stop word or not
    if token not in stop_words:
      # Paased to the snowball stemmer
      tokens.append(lem.lemmatize(token))
  return tokens

def word_cloud(data):
  mask=np.array(Image.open('image/newtwi.jpeg'))
  # Assuming you have defined the 'mask' variable
  mwc =  WordCloud(max_words = 1000 , width = 1600 , height = 800,
                collocations=False,background_color='black',mask=mask)
  string_word=" ".join(data)
  mwc.generate(string_word)  # Concatenate all text data into a single string
  return mwc
  
  # plt.figure(figsize=(8, 8))
  # plt.imshow(mwc, interpolation='bilinear')  # Use 'interpolation' parameter for smoother rendering
  # plt.title("Vibes For Word "+f"{hashtag}")
  # plt.axis('off')  # Use string 'off' instead of off
  # plt.show()


def status_saver(action,hashtag):
  if action =="r" or action =="w":
    with open("flag.txt",action) as file :
      if action=="r":
        return file.readline()[0]
      elif action=="w":
        file.write(f"True,\n{hashtag}")
  elif action=="clean":
    with open("flag.txt","w") as file :
      file.write(f"False,\n{hashtag}")

