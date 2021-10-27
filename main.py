import streamlit as st
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
# nltk.download("punkt")
# nltk.download("stopwords")
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import requests
import matplotlib.pyplot as plt
import wordcloud
import json
import main_functions
from wordcloud import WordCloud
import pandas as pd

for x in range(11,41):
    print(x)
st.title("COP4813 Web Application Programming")
st.title("Project 1")
st.subheader("Part A")


api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_api_key"]

user = st.text_input("Please enter your name:")
st.write("Hello {}".format(user.capitalize()))
options = st.selectbox(f"{user.capitalize()}" " Please pick one of the options: ",["arts", "automobiles", "books", "business", "fashion", "food", "health", "home", "insider", "magazine", "movies", "nyregion", "obituaries", "opinion", "politics", "realestate", "science", "sports", "sundayreview", "technology", "theater", "t-magazine", "travel", "upshot", "us", "world"])
st.write("You selected {}".format(options))


url = "https://api.nytimes.com/svc/topstories/v2/" + options + ".json?api-key=" + api_key

response = requests.get(url).json()

main_functions.save_to_file(response, "JSON_Files/response.json")

my_articles = main_functions.read_from_file("JSON_Files/response.json")


str1 = ""
for i in my_articles["results"]:
    str1 = str1 + i["abstract"]

sentences = sent_tokenize(str1)
words = word_tokenize(str1)

# find/remove punctuations
words_no_punc = []
for w in words:
    if w.isalpha():
        words_no_punc.append(w.lower())

stopwords = stopwords.words("english")

clean_words = []
for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)

fdist3 = FreqDist(clean_words)


if st.checkbox("<-- Press the box to show the frequency distribution"):
    if options == options:
        df = pd.DataFrame(fdist3.most_common(10), columns=['Words', 'Frequency'])
        df = df.set_index('Words')
        st.line_chart(df)
if st.checkbox("<-- Press the box to show the WordCloud chart"):
    wordcloud = WordCloud().generate(str1)
    st.image(wordcloud.to_array())

st.subheader("Part B:")

aType = st.selectbox(f"{user.capitalize()}" " Please pick one of the options: ",["shared", "emailed", "viewed"])
st.write("You selected {}".format(aType))
aPeriod = st.selectbox(f"{user.capitalize()}" " Please pick one of the options: ",["1", "7", "30"])
st.write("You selected {}".format(aPeriod))
url2 = "https://api.nytimes.com/svc/mostpopular/v2/" + aType + "/" + aPeriod + ".json?api-key=" + api_key

response2 = requests.get(url2).json()
main_functions.save_to_file(response2, "JSON_Files/response2.json")
my_articles2 = main_functions.read_from_file("JSON_Files/response2.json")

str2 = ""
for i in my_articles2["results"]:
    str2 = str2 + i["abstract"]

sentences2 = sent_tokenize(str2)
words2 = word_tokenize(str2)

# find/remove punctuations
words_no_punc2 = []
for w in words2:
    if w.isalpha():
        words_no_punc2.append(w.lower())
clean_words2 = []
for w in words_no_punc2:
    if w not in stopwords:
        clean_words2.append(w)
fdist4 = FreqDist(clean_words2)

wordcloud2 = WordCloud().generate(str2)
st.image(wordcloud2.to_array())
