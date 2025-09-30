import streamlit as st
import preprocessor
import helper
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title='WhatsApp Analyzer',
    page_icon='💬',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title('💬 WhatsApp Chat Analyzer')
st.markdown('---')

# Sidebar
st.sidebar.markdown("Createdwith❤️byLakhan")
st.sidebar.title('📱 WhatsApp Chat Analyzer')
st.sidebar.markdown('Upload your WhatsApp chat export file to get started!')

uploaded_file = st.sidebar.file_uploader('Choose a file', type=['txt'])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8') 
    df = preprocessor.process_data(data)

    # Fetch unique users
    user_list = df['username'].unique().tolist()
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox('Show Analysis for:', user_list)

    if st.sidebar.button('🔍 Show Analysis', use_container_width=True):
        
        # ==================== OVERALL SUMMARY ====================
        st.header('📊 Overall Summary')
        num_message, words, num_media, links = helper.featch_states(selected_user, df)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric(
                label="💬 Total Messages",
                value=f"{int(num_message):,}",
                delta=None
            )
        with c2:
            st.metric(
                label="📝 Total Words",
                value=f"{int(words):,}",
                delta=None
            )
        with c3:
            st.metric(
                label="📷 Media Shared",
                value=f"{int(num_media):,}",
                delta=None
            )
        with c4:
            st.metric(
                label="🔗 Links Shared",
                value=f"{int(links):,}",
                delta=None
            )
        
        st.markdown('---')
        
        # ==================== MONTHLY TIMELINE ====================
        st.header('📅 Monthly Timeline')
        
        # Month mapping
        month_map = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        
        month_trend = helper.monthly_timeline(selected_user, df)
        month_trend['month_name'] = month_trend['time'].str.split('-').str[0]
        month_trend['month_num'] = month_trend['month_name'].map(month_map)
        timeline_sorted = month_trend.sort_values('month_num')
        
        fig_month = go.Figure()
        fig_month.add_trace(go.Scatter(
            x=timeline_sorted['time'],
            y=timeline_sorted['message'],
            mode='lines+markers',
            name='Messages',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=8, color='#FF6B6B'),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.2)'
        ))
        
        fig_month.update_layout(
            height=400,
            xaxis_title="Month",
            yaxis_title="Number of Messages",
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='lightgray')
        )
        
        st.plotly_chart(fig_month, use_container_width=True)
        
        # ==================== DAILY TIMELINE ====================
        st.header('📆 Daily Timeline')
        daily_time = helper.daily_timeline(selected_user, df)
        
        fig_daily = go.Figure()
        fig_daily.add_trace(go.Scatter(
            x=daily_time['date_new'],
            y=daily_time['message'],
            mode='lines',
            name='Messages',
            line=dict(color='#4ECDC4', width=2),
            fill='tozeroy',
            fillcolor='rgba(78, 205, 196, 0.2)'
        ))
        
        fig_daily.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Number of Messages",
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='lightgray')
        )
        
        st.plotly_chart(fig_daily, use_container_width=True)
        
        # ==================== DAY-WISE ACTIVITY ====================
        st.header('📊 Day-wise Activity Analysis')
        day_timeline = helper.dayname_timeline(selected_user, df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Messages by Day')
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=day_timeline['day'],
                y=day_timeline['message'],
                marker=dict(
                    color=day_timeline['message'],
                    colorscale='Viridis',
                    showscale=True
                ),
                text=day_timeline['message'],
                textposition='auto'
            ))
            
            fig_bar.update_layout(
                height=400,
                xaxis_title="Day of Week",
                yaxis_title="Number of Messages",
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=False
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            st.subheader('Distribution by Day')
            fig_pie = go.Figure()
            fig_pie.add_trace(go.Pie(
                labels=day_timeline['day'],
                values=day_timeline['message'],
                hole=0.4,
                marker=dict(colors=px.colors.qualitative.Set3),
                textinfo='label+percent',
                textfont_size=12
            ))
            
            fig_pie.update_layout(
                height=400,
                showlegend=True,
                legend=dict(orientation="v", yanchor="middle", y=0.5)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # ==================== ACTIVITY HEATMAP ====================
        st.header('🔥 Activity Heatmap')

        user_heatmap = helper.user_activity_map(selected_user, df)
        period_order = [
            '00-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10',
            '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20',
            '20-21', '21-22', '22-23', '23-00'
        ]
        user_heatmap = user_heatmap.reindex(columns=period_order)
        fig, ax = plt.subplots(figsize=(8,3))
        ax = sns.heatmap(
            user_heatmap,
            cmap="viridis",   
            linewidths=0.5,   
            linecolor='white'   
        )

        ax.tick_params(axis='x', labelsize=6)
        ax.tick_params(axis='y', labelsize=6)

        st.pyplot(fig)

        # ==================== MOST ACTIVE USERS ====================
        if selected_user == 'Overall':
            st.header('🏃‍♀️ Most Active Users')
            
            x, df_new = helper.most_busy_user(df)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig_users = go.Figure()
                fig_users.add_trace(go.Bar(
                    x=x.index.astype(str),
                    y=x.values,
                    marker=dict(
                        color=x.values,
                        colorscale='Plasma',
                        showscale=True
                    ),
                    text=x.values,
                    textposition='auto'
                ))
                
                fig_users.update_layout(
                    height=400,
                    xaxis_title="Users",
                    yaxis_title="Number of Messages",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    showlegend=False,
                    xaxis=dict(
                    type='category',  # Force categorical x-axis
                    tickangle=45)
                )
                
                st.plotly_chart(fig_users, use_container_width=True)
            
            with col2:
                st.dataframe(
                    df_new.style.background_gradient(cmap="RdYlGn"),
                    height=400
                )
        
        # ==================== WORD CLOUD ====================
        st.header('🌥️ Word Cloud - Most Common Words')
        try:
            import matplotlib.pyplot as plt
            df_wc = helper.create_word_cloud(selected_user, df)
            
            fig_wc, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(df_wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig_wc)
        except ValueError:
            st.info('📝 No words to display')
        
        # ==================== MOST COMMON WORDS ====================
        st.header('🔠 Most Common Words')
        common_words = helper.most_common_word(selected_user, df)
        
        if not common_words.empty:
            fig_words = go.Figure()
            fig_words.add_trace(go.Bar(
                x=common_words[1].head(20),
                y=common_words[0].head(20),
                orientation='h',
                marker=dict(
                    color=common_words[1].head(20),
                    colorscale='Greens',
                    showscale=True
                ),
                text=common_words[1].head(20),
                textposition='outside'
            ))
            
            fig_words.update_layout(
                height=600,
                xaxis_title="Frequency",
                yaxis_title="Words",
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis={'categoryorder': 'total ascending'}
            )
            
            st.plotly_chart(fig_words, use_container_width=True)
        else:
            st.info('📝 No common words found')
        
        # ==================== EMOJI ANALYSIS ====================
        st.header('😊 Emoji Analysis')
        emoji_df = helper.get_emojis(selected_user, df)
        
        if not emoji_df.empty:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.dataframe(
                    emoji_df.head(10).style.background_gradient(cmap="YlOrRd"),
                    height=400
                )
            
            with col2:
                fig_emoji = go.Figure()
                fig_emoji.add_trace(go.Pie(
                    labels=emoji_df[0].head(10),
                    values=emoji_df[1].head(10),
                    hole=0.3,
                    textinfo='label+percent',
                    textfont_size=16,
                    marker=dict(colors=px.colors.qualitative.Pastel)
                ))
                
                fig_emoji.update_layout(
                    height=400,
                    showlegend=True,
                    title="Top 10 Emojis Used"
                )
                
                st.plotly_chart(fig_emoji, use_container_width=True)
        else:
            st.info('😔 No emojis were used in the chat')
        
        # ==================== FOOTER ====================
        st.markdown('---')
        st.markdown(
            """
            <div style='text-align: center; color: gray; padding: 20px;'>
                <p>💡 Created with ❤️ by Lakhan</p>
                <p style='font-size: 12px;'>WhatsApp Chat Analyzer • Interactive Analytics Dashboard</p>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    # Landing page when no file is uploaded
    st.info('👈 Please upload a WhatsApp chat export file from the sidebar to begin analysis')
    
    with st.expander("📖 How to export WhatsApp chat?"):
        st.markdown("""
        ### Steps to export WhatsApp chat:
        
        1. Open WhatsApp on your phone
        2. Go to the chat you want to analyze
        3. Tap on the three dots (⋮) at the top right
        4. Select **More** → **Export chat**
        5. Choose **Without media**
        6. Save the file and upload it here
        
        **Note:** The chat export should be in `.txt` format
        """)
    
    st.markdown('---')
    st.subheader('✨ Features')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📊 Statistics**
        - Total messages
        - Word count
        - Media & links
        """)
    
    with col2:
        st.markdown("""
        **📈 Visualizations**
        - Timeline analysis
        - Activity heatmaps
        - Word clouds
        """)
    
    with col3:
        st.markdown("""
        **👥 User Analysis**
        - Most active users
        - Common words
        - Emoji usage
        """)