import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def display_metrics_box(value, title, unit="", prefix_unit=False):
    value = f'{value:,}' if not isinstance(value, str) else value
    st.markdown(
        f'''
        <div style="text-align: center; border-radius: 5px">
            <p style="font-family: Monospace; font-size: 12px">{title}</p>
            <h1 style="padding-top: 5px">{unit if prefix_unit else ""}{value}{unit if not prefix_unit else ""}</h1>
        </div>
        ''', 
        unsafe_allow_html=True
    )


def get_monthly_stats(df):
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['month_name'] = pd.to_datetime(df['date']).dt.month_name()


    monthly_stats = df.groupby(['month', 'month_name']).agg(total_spendings=('amount', 'sum')).reset_index().sort_values('month', ascending=False)
    monthly_stats['marker_color'] = np.where(
        monthly_stats.index == monthly_stats['total_spendings'].idxmax(),
        '#b71c1c',
        '#b0bec5'
    )
    return monthly_stats

def get_monthly_stats_fig(df):
    monthly_stats = get_monthly_stats(df)

    fig = px.bar(
        monthly_stats, 
        y='month_name', 
        x='total_spendings',
        height=600,
        text='total_spendings'
    )

    fig.update_traces(
        textposition='inside',
        textfont_size=14,
        texttemplate='&#8377;%{text}',
        marker=dict(
            color=monthly_stats['marker_color'].tolist()
        )
    )

    return fig