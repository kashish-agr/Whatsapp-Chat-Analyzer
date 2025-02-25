import streamlit as st
import preprocessing , helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader('Upload  Your Whatsapp chats')
if uploaded_file is not None :
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessing.preprocess(data)
    # st.dataframe(df)

    user_list = df['Users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    seleted_user = st.sidebar.selectbox('Show analysis with' , user_list)
    if st.sidebar.button('Show Analysis'):


        # Message Stats
        st.title('Top Statistics')
        num_messages , num_words , shared_media ,link_shared ,  emojis_shared = helper.fetch_stats(seleted_user , df)
        col1, col2, col3, col4 , col5 = st.columns(5)
        with col1 :
            st.header('Total Messages')
            st.title(num_messages)
        with col2 :
            st.header('Total words')
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(shared_media)
        with col4:
            st.header('Link Shared')
            st.title(link_shared)

        with col5:
            st.header('Emojis Shared')
            st.title(emojis_shared)


        # Monthly Timeline Analysis
        st.title('Monthly Timeline Analysis')
        timeline = helper.monthly_analysis(df , seleted_user)
        fig,ax = plt.subplots()
        ax.bar(timeline['time'] , timeline['message'])
        plt.xticks(rotation= 90)
        st.pyplot(fig)


        # Daily Timeline Analysis
        st.title('Daily Timeline Analysis')
        daily_timeline = helper.daily_analysis(df, seleted_user)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['Date'], daily_timeline['message'])
        plt.xticks(rotation=90)
        st.pyplot(fig)


        # Most Busy Day
        st.title('Most Busy Day')
        day_timeline = helper.busy_day(df, seleted_user)
        fig, ax = plt.subplots()
        ax.bar(day_timeline['Day_name'], day_timeline['message'])
        plt.xticks(rotation=90)
        st.pyplot(fig)


        # Most Busy Month
        st.title('Most Busy Month')
        month_count = helper.busy_month(df, seleted_user)
        fig, ax = plt.subplots()
        ax.bar(month_count['month'], month_count['message'])
        plt.xticks(rotation=90)
        st.pyplot(fig)


        # Finding the busiest member in the chat
        if seleted_user =='Overall':
            st.title("Most Busy Users")
            x , table = helper.fetch_most_busy_user(df)
            fig , ax = plt.subplots()
            col1 , col2 = st.columns(2)
            with col1 :
                ax.bar(x.index , x.values)
                plt.xlabel("Users")
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2 :
                st.dataframe(table)

        #  HeatMap
        st.title('Heat Map')
        pt = helper.daily_activity_map(df, seleted_user)
        fig, ax = plt.subplots()
        ax= sns.heatmap(pt)
        st.pyplot(fig)


        #  World CLoud
        st.title('Word Cloud')
        image = helper.create_wordcloud(df , seleted_user)
        fig, ax = plt.subplots()
        ax.imshow(image)
        st.pyplot(fig)


        # Most Common Words
        top20_words = helper.top20(df, seleted_user)
        st.title("Top 20 Words of the Chat")
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.barh( top20_words['Word'], top20_words['Count'])
            st.pyplot(fig)
        with col2:
            st.dataframe(top20_words)


        # Emoji Analysis
        emo_df = helper.Emo_Analysis(df , seleted_user)
        st.title("Emojis Analysis")
        col1 , col2 = st.columns(2)
        with col1 :
            fig, ax = plt.subplots()
            ax.pie( emo_df['count'] , labels = emo_df['Emojis'])
            st.pyplot(fig)
        with col2 :
            st.dataframe(emo_df)









