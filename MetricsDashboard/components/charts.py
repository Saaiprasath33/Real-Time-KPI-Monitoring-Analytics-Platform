import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import config

def create_real_time_line_chart(data, x_col, y_col, title, color=None):
    """Create a real-time line chart"""
    if color is None:
        color = config.COLORS['primary']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode='lines+markers',
        name=title,
        line=dict(color=color, width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title=y_col.replace('_', ' ').title(),
        height=300,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False
    )
    
    return fig

def create_gauge_chart(value, title, max_value=100, threshold=None):
    """Create a gauge chart for KPI display"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': config.COLORS['primary']},
            'steps': [
                {'range': [0, max_value * 0.7], 'color': "lightgray"},
                {'range': [max_value * 0.7, max_value * 0.9], 'color': "yellow"},
                {'range': [max_value * 0.9, max_value], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': threshold if threshold else max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_multi_metric_chart(data, metrics, title):
    """Create a chart with multiple metrics"""
    fig = make_subplots(
        rows=len(metrics), cols=1,
        subplot_titles=metrics,
        vertical_spacing=0.1
    )
    
    colors = [config.COLORS['primary'], config.COLORS['secondary'], 
              config.COLORS['success'], config.COLORS['warning']]
    
    for i, metric in enumerate(metrics):
        if metric in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data['timestamp'],
                    y=data[metric],
                    mode='lines',
                    name=metric,
                    line=dict(color=colors[i % len(colors)])
                ),
                row=i+1, col=1
            )
    
    fig.update_layout(
        title=title,
        height=150 * len(metrics),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

def create_bar_chart(data, x_col, y_col, title, color=None):
    """Create a bar chart"""
    if color is None:
        color = config.COLORS['info']
    
    fig = px.bar(data, x=x_col, y=y_col, title=title, color_discrete_sequence=[color])
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
    return fig

def create_pie_chart(labels, values, title):
    """Create a pie chart"""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3
    )])
    
    fig.update_layout(
        title=title,
        height=300,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig
