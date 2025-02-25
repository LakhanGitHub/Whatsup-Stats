import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
st.set_page_config('🟢WhatsApp Analyzer',layout='wide')
st.header('WhatsApp Chat Analysis💬', divider='rainbow')
st.sidebar.title('WhatsApp Chat Analyzer📱')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8') 
    df = preprocessor.process_data(data)
    #st.dataframe(df)

#featch unique users
    user_list = df['username'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox('Show Analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):
        st.header('Overall summary')
        num_message,words,num_media,links = helper.featch_states(selected_user,df)
        c1,c2,c3,c4 = st.columns(4)
        with c1:
            c1.subheader('Total Chats')
            st.title(num_message)
            #st.markdown(f"<h1 style='color: black;'>📩 {num_message}</h1>", unsafe_allow_html=True)
        with c2:
            c2.subheader('Total Words')
            st.title(words)
            #st.markdown(f"<h1 style='color: black;'>📄 {words}</h1>", unsafe_allow_html=True)
        with c3:
            c3.subheader('Media shared')
            st.title(num_media)
            #st.markdown(f"<h1 style='color: black;'>📷 {num_media}</h1>", unsafe_allow_html=True)
        with c4:
            c4.subheader('Link shared')
            st.title(links)
            #st.markdown(f"<h1 style='color: black;'> 🔗{links}</h1>", unsafe_allow_html=True)
        #Monthly trend
        st.header('Monthly Timeline', divider=True)
        month_trend = helper.monthly_timeline(selected_user, df)
        fig,ax  = plt.subplots(figsize=(8,3))
        ax.plot(month_trend['time'],month_trend['message'],color='orange')
        plt.xticks(rotation='vertical')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.2, color='gray')
        ax.tick_params(axis='x', labelsize=6)  # Change X-axis tick font size
        ax.tick_params(axis='y', labelsize=6)
        st.pyplot(fig)

        #daily timeline trend
        st.header('Daily Timeline')
        daily_time = helper.daily_timeline(selected_user, df)
        fig,ax  = plt.subplots(figsize=(8,3))
        ax.plot(daily_time['date_new'],daily_time['message'],color='orange')
        plt.xticks(rotation='vertical')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.2, color='gray')
        ax.tick_params(axis='x', labelsize=6)  # Change X-axis tick font size
        ax.tick_params(axis='y', labelsize=6)
        st.pyplot(fig)

        #day wise activity
        st.header('Daywise Activity')
        s1, s2 = st.columns(2)
        with s1:
            day_timeline =helper.dayname_timeline(selected_user, df)
            fig,ax  = plt.subplots(figsize=(4,3))
            sns.barplot(x=day_timeline['day'],y=day_timeline['message'], ax=ax,palette=['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'pink'])
            plt.xticks(rotation='vertical')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.2, color='gray')
            ax.tick_params(axis='x', labelsize=6)  # Change X-axis tick font size
            ax.tick_params(axis='y', labelsize=6)
            ax.set_xlabel('')
            ax.set_ylabel('')
            st.pyplot(fig)
        #pie chart
        with s2:
            day_timeline =helper.dayname_timeline(selected_user, df)
            max_index = np.argmax(day_timeline['message'])
            explode = [.1 if i==max_index else 0 for i in range(len(day_timeline['message']))]
            fig,ax  = plt.subplots(figsize=(6,3))
            sizes = day_timeline['message'].to_list()
            total = sum(sizes)
            angle = (sum(sizes[:max_index]) + sizes[max_index] / 2) / total * 360  # Midpoint of the max slice
            startangle = 90 - angle  # Adjust to bring max slice to the top
            ax.pie(day_timeline['message'],labels=day_timeline['day'],explode=explode,autopct='%1.1f%%',textprops={'fontsize': 6},startangle=startangle,
        colors=['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'pink'])
            st.pyplot(fig)

        #user activity heatmap
        st.header('Users Activity heatmap')
        user_heatmap = helper.user_activity_map(selected_user,df)
        fig,ax = plt.subplots(figsize=(8,3))
        ax = sns.heatmap(user_heatmap)
        ax.tick_params(axis='x', labelsize=6)  # Change X-axis tick font size
        ax.tick_params(axis='y', labelsize=6)
        st.pyplot(fig) 

        #find most busy person
        st.header('Most Active Users😊', divider=True)
        
        if selected_user == 'Overall':
            #st.header('Most Busy Persons')
            x,df_new = helper.most_busy_user(df)
            fig, ax  = plt.subplots(figsize=(4,3))

            co1, co2 = st.columns(2)

            with co1:
                sns.barplot(x=x.index, y=x.values, color='red',ax=ax, palette='Spectral')
                #for i in ax.containers:
                    #ax.bar_label(i,) 
                plt.xticks(rotation='vertical')
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.2, color='gray')
                ax.tick_params(axis='x', labelsize=6)  # Change X-axis tick font size
                ax.tick_params(axis='y', labelsize=6)  
                ax.set_xlabel('')
                st.pyplot(fig)
            
            with co2:
                st.dataframe(df_new.style.background_gradient(cmap="Spectral"))
        #wordcloud
        st.header('Word Cloud - (Most common words used)',divider=True)
        try:
            df_wc = helper.create_word_cloud(selected_user, df)
        
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            ax.axis("off")
            st.pyplot(fig)
        except ValueError as e:
            st.write('No word')
            
        #most common words
        st.header('Most Common words',divider=True)
        common_words = helper.most_common_word(selected_user,df)
        #st.dataframe(common_words)
        if not common_words.empty:
            fig, ax = plt.subplots(figsize=(8,2))
            sns.barplot(x=common_words[0], y=common_words[1], color='green',ax=ax,palette='viridis')
            #for i in ax.containers:
            #    ax.bar_label(i,) 
            plt.xticks(rotation='vertical')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.2, color='gray')
            ax.set_xlabel('')
            ax.set_ylabel('')
            st.pyplot(fig)
        else:
            st.write('no word was used')

        #show emoji
        st.header('Emojis used😊', divider=True)
        emonji_ = helper.get_emojis(selected_user, df)
        co1, co2 = st.columns(2)
        with co1:
            if not emonji_.empty:
                st.dataframe(emonji_)
            else:
                st.write("No emojis were used.")
        with co2:
            if not emonji_.empty:
                fig, ax = plt.subplots(figsize=(6,6))
                ax.pie(emonji_[1], labels=emonji_[0], autopct='%1.1f%%', textprops={'fontsize': 14})
                st.pyplot(fig)
            else:
                st.write("No emojis were used.")

        
