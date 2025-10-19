import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import config
from data_generator import DataGenerator
from alert_system import AlertSystem
from components.kpi_cards import display_system_metrics, display_business_metrics, display_server_metrics
from components.charts import create_real_time_line_chart, create_gauge_chart, create_multi_metric_chart

# Page configuration
st.set_page_config(
    page_title=config.DASHBOARD_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Sky Blue Theme and Feature Buttons
def load_custom_css():
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {
            background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 50%, #7DD3FC 100%);
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
        }
        
        /* Main Content Area */
        .main .block-container {
            padding-top: 1rem;
            background: transparent;
        }
        
        /* Custom Header with Logo */
        .dashboard-header {
            background: linear-gradient(135deg, #0EA5E9 0%, #38BDF8 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 15px 35px rgba(14, 165, 233, 0.4);
            animation: slideDown 0.8s ease-out;
            text-align: center;
        }
        
        .dashboard-title {
            color: white;
            font-size: 3.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
        }
        
        .dashboard-subtitle {
            color: #F0F9FF;
            font-size: 1.3rem;
            margin-top: 0.5rem;
            font-weight: 300;
        }
        
        .logo-container {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
        }
        
        .dashboard-logo {
            font-size: 5rem;
            margin-right: 1rem;
            animation: pulse 2s infinite;
            filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));
        }
        
        /* Feature Navigation Buttons */
        .feature-nav {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            margin: 2rem 0;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(14, 165, 233, 0.2);
            backdrop-filter: blur(10px);
        }
        
        .feature-button {
            background: linear-gradient(135deg, #0EA5E9 0%, #38BDF8 100%);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(14, 165, 233, 0.3);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            min-width: 160px;
            justify-content: center;
        }
        
        .feature-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4);
            background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 100%);
        }
        
        .feature-button.active {
            background: linear-gradient(135deg, #059669 0%, #10B981 100%);
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
        }
        
        /* Animated Backgrounds */
        @keyframes slideDown {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes slideUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        /* Section Container */
        .section-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 15px 35px rgba(14, 165, 233, 0.15);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(14, 165, 233, 0.2);
            animation: slideUp 0.6s ease-out;
        }
        
        /* Section Headers */
        .section-header {
            background: linear-gradient(135deg, #0EA5E9 0%, #38BDF8 100%);
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 15px;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 25px rgba(14, 165, 233, 0.3);
            text-align: center;
        }
        
        .section-header h2 {
            margin: 0;
            font-size: 2rem;
            font-weight: 600;
        }
        
        /* Metric Cards Enhancement */
        .metric-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem;
            box-shadow: 0 10px 30px rgba(14, 165, 233, 0.2);
            border: 2px solid rgba(14, 165, 233, 0.3);
            transition: all 0.3s ease;
            animation: slideUp 0.5s ease-out;
            backdrop-filter: blur(5px);
        }
        
        .metric-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(14, 165, 233, 0.4);
            border-color: #0EA5E9;
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #0EA5E9 0%, #38BDF8 100%);
        }
        
        .css-1d391kg .stSelectbox > label,
        .css-1d391kg .stSlider > label,
        .css-1d391kg .stCheckbox > label {
            color: white !important;
            font-weight: 500;
        }
        
        /* Alert Styling */
        .alert-container {
            background: rgba(239, 68, 68, 0.1);
            border: 2px solid #EF4444;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            animation: slideUp 0.4s ease-out;
            backdrop-filter: blur(5px);
        }
        
        .success-container {
            background: rgba(16, 185, 129, 0.1);
            border: 2px solid #10B981;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            animation: fadeIn 0.5s ease-in-out;
            backdrop-filter: blur(5px);
        }
        
        /* Chart Containers */
        .chart-container {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(14, 165, 233, 0.15);
            border: 1px solid rgba(14, 165, 233, 0.2);
            animation: fadeIn 0.6s ease-in-out;
            backdrop-filter: blur(5px);
        }
        
        /* Status Indicators */
        .status-online {
            color: #10B981;
            animation: pulse 2s infinite;
        }
        
        .status-warning {
            color: #F59E0B;
            animation: pulse 1.5s infinite;
        }
        
        .status-critical {
            color: #EF4444;
            animation: pulse 1s infinite;
        }
        
        /* Footer */
        .dashboard-footer {
            background: rgba(255, 255, 255, 0.9);
            color: #0C4A6E;
            text-align: center;
            padding: 2rem;
            border-radius: 15px;
            margin-top: 2rem;
            border-top: 3px solid #0EA5E9;
            backdrop-filter: blur(10px);
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #0EA5E9;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #0284C7;
        }
        
        /* Control Panel */
        .control-panel {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 10px 25px rgba(14, 165, 233, 0.2);
            backdrop-filter: blur(10px);
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'data_generator' not in st.session_state:
    st.session_state.data_generator = DataGenerator()
    st.session_state.alert_system = AlertSystem()
    st.session_state.metrics_history = []
    st.session_state.previous_metrics = None
    st.session_state.active_section = 'overview'

# Function to generate unique timestamp-based keys
def get_unique_key(base_name):
    return f"{base_name}_{int(time.time() * 1000000)}"

# Load custom CSS
load_custom_css()

# Enhanced Header with Logo
st.markdown("""
<div class="dashboard-header">
    <div class="logo-container">
        <div class="dashboard-logo">🌤️</div>
        <div>
            <h1 class="dashboard-title">MetricsDashboard Pro</h1>
            <p class="dashboard-subtitle">Real-Time KPI Monitoring & Analytics Platform</p>
        </div>
    </div>
    <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 1rem;">
        <span class="status-online">● LIVE</span>
        <span style="color: #F0F9FF;">|</span>
        <span style="color: #F0F9FF;">Last Updated: <span id="current-time">{}</span></span>
    </div>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

# Feature Navigation Buttons
st.markdown("""
<div class="feature-nav">
    <div style="width: 100%; text-align: center; margin-bottom: 1rem;">
        <h3 style="color: #0C4A6E; margin: 0;">Select Dashboard Features</h3>
    </div>
</div>
""", unsafe_allow_html=True)

# Create feature buttons
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📊 Overview", key="overview_btn"):
        st.session_state.active_section = 'overview'

with col2:
    if st.button("🖥️ System Metrics", key="system_btn"):
        st.session_state.active_section = 'system'

with col3:
    if st.button("💼 Business KPIs", key="business_btn"):
        st.session_state.active_section = 'business'

with col4:
    if st.button("📈 Analytics", key="analytics_btn"):
        st.session_state.active_section = 'analytics'

with col5:
    if st.button("🚨 Alerts", key="alerts_btn"):
        st.session_state.active_section = 'alerts'

# Additional feature buttons row
col6, col7, col8, col9, col10 = st.columns(5)

with col6:
    if st.button("🌐 Server Status", key="server_btn"):
        st.session_state.active_section = 'server'

with col7:
    if st.button("⚙️ Settings", key="settings_btn"):
        st.session_state.active_section = 'settings'

with col8:
    if st.button("📋 Reports", key="reports_btn"):
        st.session_state.active_section = 'reports'

with col9:
    if st.button("🔄 Real-Time", key="realtime_btn"):
        st.session_state.active_section = 'realtime'

with col10:
    if st.button("📱 Mobile View", key="mobile_btn"):
        st.session_state.active_section = 'mobile'

# Enhanced Sidebar with Controls
with st.sidebar:
    st.markdown("""
    <div class="control-panel">
        <h2 style="color: #0EA5E9; text-align: center;">⚙️ Control Panel</h2>
        <div style="height: 2px; background: linear-gradient(90deg, #0EA5E9, #38BDF8); margin: 1rem 0;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    auto_refresh = st.checkbox("🔄 Auto Refresh", value=True)
    refresh_interval = st.slider("⏱️ Refresh Interval (seconds)", 1, 10, config.REFRESH_INTERVAL)
    
    st.markdown("### 🎛️ Display Options")
    show_animations = st.checkbox("✨ Animations", value=True)
    show_tooltips = st.checkbox("💡 Tooltips", value=True)
    compact_view = st.checkbox("📱 Compact View", value=False)
    
    st.markdown("### 🎨 Theme Options")
    theme_variant = st.selectbox("Theme", ["Sky Blue", "Ocean Blue", "Light Blue"])
    
    st.markdown("""
    <div class="control-panel" style="margin-top: 2rem;">
        <h4 style="color: #0EA5E9; margin: 0;">System Status</h4>
        <p style="color: #0369A1; margin: 0.5rem 0;">🟢 All Systems Operational</p>
        <p style="color: #0369A1; margin: 0; font-size: 0.9rem;">Uptime: 99.9% | Load: 12%</p>
    </div>
    """, unsafe_allow_html=True)

# Generate current metrics for all sections
current_time = datetime.now()
system_metrics = st.session_state.data_generator.get_system_metrics()
business_metrics = st.session_state.data_generator.get_business_metrics()
server_metrics = st.session_state.data_generator.get_server_metrics()
all_metrics = {**system_metrics, **business_metrics, **server_metrics}

# Store metrics history
st.session_state.metrics_history.append(all_metrics)
if len(st.session_state.metrics_history) > config.MAX_DATA_POINTS:
    st.session_state.metrics_history = st.session_state.metrics_history[-config.MAX_DATA_POINTS:]

# Display content based on active section
if st.session_state.active_section == 'overview':
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><h2>📊 Dashboard Overview</h2></div>', unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🖥️ CPU Usage", f"{system_metrics['cpu_usage']:.1f}%")
    with col2:
        st.metric("💰 Revenue", f"${business_metrics['revenue']:,.0f}")
    with col3:
        st.metric("👥 Active Users", f"{business_metrics['active_users']:,}")
    with col4:
        st.metric("⚡ Response Time", f"{server_metrics['response_time']:.0f}ms")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_section == 'system':
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><h2>🖥️ System Performance Metrics</h2></div>', unsafe_allow_html=True)
    display_system_metrics(system_metrics)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_section == 'business':
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><h2>💼 Business KPI Dashboard</h2></div>', unsafe_allow_html=True)
    display_business_metrics(business_metrics, st.session_state.previous_metrics)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_section == 'analytics':
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><h2>📈 Real-Time Analytics</h2></div>', unsafe_allow_html=True)
    
    if len(st.session_state.metrics_history) > 1:
        df = pd.DataFrame(st.session_state.metrics_history)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            cpu_chart = create_real_time_line_chart(
                df.tail(20), 'timestamp', 'cpu_usage', 
                'CPU Usage Trend', config.COLORS['warning']
            )
            st.plotly_chart(cpu_chart, use_container_width=True, key=get_unique_key("analytics_cpu"))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            revenue_chart = create_real_time_line_chart(
                df.tail(20), 'timestamp', 'revenue',
                'Revenue Analytics', config.COLORS['success']
            )
            st.plotly_chart(revenue_chart, use_container_width=True, key=get_unique_key("analytics_revenue"))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            memory_gauge = create_gauge_chart(
                system_metrics['memory_usage'], 'Memory Usage', 100, 85
            )
            st.plotly_chart(memory_gauge, use_container_width=True, key=get_unique_key("analytics_memory"))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            users_chart = create_real_time_line_chart(
                df.tail(20), 'timestamp', 'active_users',
                'User Activity Analytics', config.COLORS['info']
            )
            st.plotly_chart(users_chart, use_container_width=True, key=get_unique_key("analytics_users"))
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_section == 'alerts':
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><h2>🚨 Alert Management Center</h2></div>', unsafe_allow_html=True)
    
    # Check for alerts
    alerts = st.session_state.alert_system.check_thresholds(all_metrics)
    for alert in alerts:
        st.session_state.alert_system.log_alert(alert)
    
    recent_alerts = st.session_state.alert_system.get_recent_alerts(10)
    
    if recent_alerts:
        for alert in reversed(recent_alerts):
            severity_color = {
                'CRITICAL': '🔴',
                'HIGH': '🟠', 
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(alert['severity'], '⚪')
            
            st.markdown(f"""
            <div class="alert-container">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{severity_color} {alert['severity']} ALERT</strong><br>
                        <span style="font-size: 1.1rem;">{alert['metric'].replace('_', ' ').title()}: <strong>{alert['value']:.2f}</strong></span><br>
                        <small>Threshold: {alert['threshold']:.2f} | Time: {alert['timestamp'].strftime('%H:%M:%S')}</small>
                    </div>
                    <div style="font-size: 2rem; opacity: 0.7;">{severity_color}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-container">
            <div style="text-align: center;">
                <h3 style="color: #10B981; margin: 0;">✅ All Systems Normal</h3>
                <p style="margin: 0.5rem 0;">No active alerts detected</p>
                <small>Last check: {}</small>
            </div>
        </div>
        """.format(current_time.strftime('%H:%M:%S')), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_section == 'server':
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><h2>🌐 Server Performance Dashboard</h2></div>', unsafe_allow_html=True)
    display_server_metrics(server_metrics)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_section == 'settings':
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><h2>⚙️ Dashboard Settings</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 Appearance")
        st.color_picker("Primary Color", "#0EA5E9")
        st.selectbox("Font Size", ["Small", "Medium", "Large"])
        st.checkbox("Dark Mode", value=False)
        
    with col2:
        st.subheader("📊 Data Settings")
        st.number_input("Refresh Rate (sec)", min_value=1, max_value=60, value=2)
        st.number_input("Data Points", min_value=10, max_value=1000, value=100)
        st.checkbox("Auto-save Data", value=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_section == 'reports':
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><h2>📋 Analytics Reports</h2></div>', unsafe_allow_html=True)
    
    st.subheader("📊 Performance Summary")
    
    if len(st.session_state.metrics_history) > 0:
        df = pd.DataFrame(st.session_state.metrics_history)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Avg CPU Usage", f"{df['cpu_usage'].mean():.1f}%")
            st.metric("Max Memory", f"{df['memory_usage'].max():.1f}%")
        
        with col2:
            st.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
            st.metric("Peak Users", f"{df['active_users'].max():,}")
        
        with col3:
            st.metric("Avg Response", f"{df['response_time'].mean():.0f}ms")
            st.metric("Total Requests", f"{df['requests_per_second'].sum():,}")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_section == 'realtime':
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><h2>🔄 Real-Time Monitor</h2></div>', unsafe_allow_html=True)
    
    # Auto-refresh real-time data
    placeholder = st.empty()
    
    if auto_refresh:
        with placeholder.container():
            st.subheader(f"🕐 Live Update: {current_time.strftime('%H:%M:%S')}")
            
            # Real-time metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                display_system_metrics(system_metrics)
            with col2:
                display_business_metrics(business_metrics, st.session_state.previous_metrics)
            with col3:
                display_server_metrics(server_metrics)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_section == 'mobile':
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><h2>📱 Mobile Dashboard View</h2></div>', unsafe_allow_html=True)
    
    # Compact mobile-friendly layout
    st.metric("System Health", "98.5%", "↗️ +0.2%")
    st.metric("Revenue Today", f"${business_metrics['revenue']:,.0f}", "↗️ +12%")
    st.metric("Active Users", f"{business_metrics['active_users']:,}", "↗️ +8%")
    
    st.progress(system_metrics['cpu_usage'] / 100)
    st.caption(f"CPU Usage: {system_metrics['cpu_usage']:.1f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Update previous metrics
st.session_state.previous_metrics = all_metrics.copy()

# Enhanced Footer
st.markdown("""
<div class="dashboard-footer">
    <div style="display: flex; justify-content: center; align-items: center; gap: 25px; flex-wrap: wrap;">
        <span>🌤️ <strong>MetricsDashboard Pro</strong></span>
        <span>|</span>
        <span>🚀 Built with Streamlit & Python</span>
        <span>|</span>
        <span>☁️ Sky Blue Theme</span>
        <span>|</span>
        <span>📊 Advanced Analytics</span>
    </div>
    <div style="margin-top: 1rem; font-size: 0.9rem;">
        © 2025 MetricsDashboard Pro - Cloud-Based Performance Monitoring
    </div>
</div>
""", unsafe_allow_html=True)
