# Configuration settings for MetricsDashboard
import os

# Dashboard Configuration
DASHBOARD_TITLE = "MetricsDashboard Pro"
REFRESH_INTERVAL = 2  # seconds
MAX_DATA_POINTS = 100

# Alert Configuration
ALERT_THRESHOLDS = {
    'cpu_usage': 80.0,
    'memory_usage': 85.0,
    'revenue': 10000.0,
    'response_time': 2000.0,  # milliseconds
    'error_rate': 5.0  # percentage
}

# Email Configuration (Optional)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'sender_password': 'your_app_password',
    'recipient_email': 'recipient@gmail.com'
}

# Sky Blue Theme Colors
COLORS = {
    'primary': '#0EA5E9',           # Sky Blue
    'secondary': '#38BDF8',         # Light Sky Blue
    'accent': '#7DD3FC',            # Very Light Sky Blue
    'success': '#10B981',           # Green
    'warning': '#F59E0B',           # Amber
    'danger': '#EF4444',            # Red
    'info': '#06B6D4',              # Cyan
    'light': '#F0F9FF',             # Very Light Blue
    'dark': '#0C4A6E',              # Dark Sky Blue
    'background': '#E0F2FE',        # Sky Blue Background
    'surface': '#F0F9FF',           # Card Background
    'text_primary': '#0C4A6E',      # Dark Text
    'text_secondary': '#0369A1'     # Secondary Text
}

# Gradient Colors
GRADIENTS = {
    'primary': 'linear-gradient(135deg, #0EA5E9 0%, #38BDF8 100%)',
    'secondary': 'linear-gradient(135deg, #38BDF8 0%, #7DD3FC 100%)',
    'success': 'linear-gradient(135deg, #059669 0%, #10B981 100%)',
    'warning': 'linear-gradient(135deg, #D97706 0%, #F59E0B 100%)',
    'danger': 'linear-gradient(135deg, #DC2626 0%, #EF4444 100%)',
    'background': 'linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 50%, #7DD3FC 100%)'
}

# Animation Settings
ANIMATIONS = {
    'fade_in': 'fadeIn 0.5s ease-in-out',
    'slide_up': 'slideUp 0.3s ease-out',
    'pulse': 'pulse 2s infinite',
    'bounce': 'bounce 1s ease-in-out'
}
