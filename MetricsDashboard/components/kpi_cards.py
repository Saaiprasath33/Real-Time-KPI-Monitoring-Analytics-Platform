import streamlit as st

def display_kpi_card_enhanced(title, value, delta=None, delta_color="normal", format_func=None, icon="📊"):
    """Display an enhanced KPI card with custom styling"""
    if format_func:
        formatted_value = format_func(value)
    else:
        formatted_value = f"{value:.2f}" if isinstance(value, float) else str(value)
    
    # Determine status color based on delta
    status_class = ""
    if delta is not None:
        if delta > 0:
            status_class = "status-online"
        elif delta < 0:
            status_class = "status-critical"
        else:
            status_class = "status-warning"
    
    # Create custom metric card
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <div style="color: #CBD5E1; font-size: 0.9rem; margin-bottom: 0.5rem;">
                    {icon} {title}
                </div>
                <div style="color: white; font-size: 2rem; font-weight: 600; line-height: 1;">
                    {formatted_value}
                </div>
                {f'<div class="{status_class}" style="font-size: 0.8rem; margin-top: 0.5rem;">△ {delta:.2f if isinstance(delta, float) else delta}</div>' if delta is not None else ''}
            </div>
            <div style="font-size: 2.5rem; opacity: 0.3;">
                {icon}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_system_metrics(metrics):
    """Display system performance metrics with enhanced styling"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        display_kpi_card_enhanced("CPU Usage", metrics['cpu_usage'], 
                                format_func=lambda x: f"{x:.1f}%", icon="🖥️")
    
    with col2:
        display_kpi_card_enhanced("Memory Usage", metrics['memory_usage'], 
                                format_func=lambda x: f"{x:.1f}%", icon="🧠")
    
    with col3:
        display_kpi_card_enhanced("Disk Usage", metrics['disk_usage'], 
                                format_func=lambda x: f"{x:.1f}%", icon="💾")
    
    with col4:
        display_kpi_card_enhanced("Network I/O", metrics['network_sent'] + metrics['network_recv'], 
                                format_func=lambda x: f"{x/1024/1024:.1f} MB", icon="🌐")

def display_business_metrics(metrics, previous_metrics=None):
    """Display business KPI metrics with enhanced styling"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta = None
        if previous_metrics:
            delta = metrics['revenue'] - previous_metrics.get('revenue', 0)
        display_kpi_card_enhanced("Revenue", metrics['revenue'], delta=delta, 
                                format_func=lambda x: f"${x:,.0f}", icon="💰")
    
    with col2:
        delta = None
        if previous_metrics:
            delta = metrics['active_users'] - previous_metrics.get('active_users', 0)
        display_kpi_card_enhanced("Active Users", metrics['active_users'], delta=delta,
                                format_func=lambda x: f"{x:,}", icon="👥")
    
    with col3:
        delta = None
        if previous_metrics:
            delta = metrics['conversion_rate'] - previous_metrics.get('conversion_rate', 0)
        display_kpi_card_enhanced("Conversion Rate", metrics['conversion_rate'], delta=delta,
                                format_func=lambda x: f"{x:.2f}%", icon="📈")
    
    with col4:
        delta = None
        if previous_metrics:
            delta = metrics['orders'] - previous_metrics.get('orders', 0)
        display_kpi_card_enhanced("Orders", metrics['orders'], delta=delta, icon="🛒")

def display_server_metrics(metrics):
    """Display server performance metrics with enhanced styling"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        display_kpi_card_enhanced("Response Time", metrics['response_time'],
                                format_func=lambda x: f"{x:.0f}ms", icon="⚡")
    
    with col2:
        display_kpi_card_enhanced("Requests/sec", metrics['requests_per_second'], icon="🔄")
    
    with col3:
        display_kpi_card_enhanced("Active Connections", metrics['active_connections'], icon="🔗")
    
    with col4:
        display_kpi_card_enhanced("Cache Hit Rate", metrics['cache_hit_rate'],
                                format_func=lambda x: f"{x:.1f}%", icon="⚡")
