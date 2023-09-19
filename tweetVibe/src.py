import streamlit as st
from streamlit_option_menu import option_menu
from scrapper import scrap
from helper_functions import clean_tweets,word_cloud
from matplotlib import pyplot as plt
import pandas as pd
from spark_loaders import spark_predict
from cloud_functions import upload_file,read_file


# Center-aligned title with logo
st.markdown(
    """
    <div style="display: flex; flex-direction: column; align-items: center;">
        <img src="https://duet-cdn.vox-cdn.com/thumbor/0x0:3001x2001/640x427/filters:focal(1501x1001:1502x1002):format(webp)/cdn.vox-cdn.com/uploads/chorus_asset/file/24805886/STK160_X_Twitter_004.jpg" alt="Logo" style="width: 100px; height: 100px;">
        <h1 style="text-align: center;">TweetVibes</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# # Center-aligned title
# st.title("TweetVibes")

hashtag=st.text_input("#️⃣#️⃣#️⃣Enter The Hashtag you want#️⃣#️⃣#️⃣")
if hashtag:
#      st.snow()
        pass

choice =option_menu(None,("🐣TweeT🐣","😂Sentiment🥹","😜VibeS😇"),orientation="horizontal")
if choice=="🐣TweeT🐣":
    if st.button("search") and hashtag!="" :
        df=scrap(hashtag)
        flag=upload_file(df,"tweets.csv")
        if flag:
               spark_predict()
               st.table(df)
elif choice=="😂Sentiment🥹":
        # spark_predict()
        df_p=read_file(filename="predicted.csv")
        st.table(df_p)
else :
    if hashtag!="":
        plot_choice =option_menu(None,("WordCloud","BarPlot"),orientation="horizontal")
        if plot_choice=="WordCloud":
                st.header(f"WordCloud for {hashtag}")
                choice=option_menu(None,("Positive","Negative"),orientation="horizontal")
                if choice=="Positive":
                        df_p=read_file(filename="predicted.csv")
                        df_p["tweets_cleaned"]=df_p.tweets.apply(lambda x : " ".join(clean_tweets(x)))
                        # df_p.to_csv("text_csv")
                        mwc=word_cloud(df_p[df_p["prediction"]=="POSITIVE"]["tweets_cleaned"])
                        fig,ax=plt.subplots()
                        ax.axis('off')
                        plt.figure(figsize=(8, 8))
                        ax.imshow(mwc, interpolation='bilinear')  # Use 'interpolation' parameter for smoother rendering
                        # ax[1].scatter(x=range(len(df)),y=df.likes.astype("int8"))
                        st.pyplot(fig)
                else:
                        df_p=read_file(filename="predicted.csv")
                        df_p["tweets_cleaned"]=df_p.tweets.apply(lambda x : " ".join(clean_tweets(x)))
                        mwc=word_cloud(df_p[df_p["prediction"]=="NEGATIVE"]["tweets_cleaned"])
                        fig,ax=plt.subplots()
                        ax.axis('off')
                        plt.figure(figsize=(8, 8))
                        ax.imshow(mwc, interpolation='bilinear')  # Use 'interpolation' parameter for smoother rendering
                        # ax[1].scatter(x=range(len(df)),y=df.likes.astype("int8"))
                        st.pyplot(fig)
        elif plot_choice=="BarPlot":
                st.header(f"BarPlot for Sentiment of {hashtag} Related Tweet")
                df_p=read_file(filename="predicted.csv")
                count_=df_p["prediction"].value_counts()
                fig,ax=plt.subplots()
                ax.axis('on')
                plt.figure(figsize=(8, 8))
                ax.bar(x=count_.index,height=count_.values) # Use 'interpolation' parameter for smoother rendering
                # ax[1].scatter(x=range(len(df)),y=df.likes.astype("int8"))
                st.pyplot(fig)
























# import streamlit as st
# from streamlit_option_menu import option_menu
# from scrapper import scrap
# from helper_functions import clean_tweets,word_cloud,status_saver
# from matplotlib import pyplot as plt
# import pandas as pd
# from spark_loaders import spark_predict
# flag=0
# st.title("TweetVibes")
# col1,col2=st.columns([1,1])
# with col1:
#         hashtag=st.text_input("",placeholder="Enter #HASHTAG You want Tweets from")
# with col2:
#         search=st.button("Search")
# choice =option_menu(None,("TweeT","Sentiment","VibeS"),orientation="horizontal")
# if choice=="TweeT":
#         if search and hashtag!="":
#                 status_saver("w")
#         if status_saver("r") and hashtag!="":
#                 df=scrap(hashtag)
#                 df.to_csv("tweeets.csv")
#         if flag :
#                 st.table(df) 
#                 spark_predict()
#         else:
#                 st.error("Search Keywords First")
# elif choice=="Sentiment":
#         if flag :
#                 # spark_predict()
#                 df_p=pd.read_csv("predicted.csv")
#                 # df=pd.read_csv("tweeets.csv")
#                 # df_p=pd.concat([df[["userids","tweets","links"]],df_p["prediction"]],axis=1)
#                 st.table(df_p)
#         else:
#                 st.error("Search Keywords First")
        
# else :
#         if flag :
#                 st.header("Recent Tweets")
#                 df=pd.read_csv("tweeets.csv")
#                 df["tweets_cleaned"]=df.tweets.apply(lambda x : " ".join(clean_tweets(x)))
#                 df.to_csv("test_csv")
#                 mwc=word_cloud(df.tweets_cleaned)
#                 fig,ax=plt.subplots()
#                 ax.axis('off')
#                 plt.figure(figsize=(8, 8))
#                 ax.imshow(mwc, interpolation='bilinear')  # Use 'interpolation' parameter for smoother rendering
#                 # ax[1].scatter(x=range(len(df)),y=df.likes.astype("int8"))
#                 st.pyplot(fig)
                
#                 # ax.title("Vibes For Word "+f"{str(hashtag)}")
#                 # plt.imshow(mwc, interpolation='bilinear')  # Use 'interpolation' parameter for smoother rendering
#                 # plt.title("Vibes For Word "+f"{hashtag}")
#                 # plt.axis('off')  # Use string 'off' instead of off
#                 # plt.show()
#         else:
#                 st.error("Search Keywords First")
        
        



    