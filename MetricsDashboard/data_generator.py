import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import psutil
import time

class DataGenerator:
    def __init__(self):
        self.base_revenue = 50000
        self.base_users = 1000
        
    def get_system_metrics(self):
        """Get real-time system performance metrics"""
        return {
            'timestamp': datetime.now(),
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_sent': psutil.net_io_counters().bytes_sent,
            'network_recv': psutil.net_io_counters().bytes_recv
        }
    
    def get_business_metrics(self):
        """Generate realistic business KPI data"""
        current_hour = datetime.now().hour
        
        # Simulate daily patterns
        if 9 <= current_hour <= 17:  # Business hours
            traffic_multiplier = random.uniform(1.2, 2.0)
        else:  # Off hours
            traffic_multiplier = random.uniform(0.3, 0.8)
            
        return {
            'timestamp': datetime.now(),
            'revenue': self.base_revenue * traffic_multiplier * random.uniform(0.8, 1.3),
            'active_users': int(self.base_users * traffic_multiplier * random.uniform(0.7, 1.4)),
            'conversion_rate': random.uniform(2.1, 4.8),
            'bounce_rate': random.uniform(35, 65),
            'avg_session_duration': random.uniform(180, 420),  # seconds
            'page_load_time': random.uniform(800, 2500),  # milliseconds
            'error_rate': random.uniform(0.1, 8.0),  # percentage
            'orders': random.randint(50, 200),
            'cart_abandonment': random.uniform(60, 80)
        }
    
    def get_server_metrics(self):
        """Generate server performance metrics"""
        return {
            'timestamp': datetime.now(),
            'response_time': random.uniform(200, 3000),  # milliseconds
            'requests_per_second': random.randint(100, 1000),
            'active_connections': random.randint(50, 500),
            'database_connections': random.randint(10, 100),
            'cache_hit_rate': random.uniform(70, 95),
            'uptime': random.uniform(99.0, 99.99)
        }
    
    def generate_historical_data(self, days=30):
        """Generate historical data for trends"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        dates = pd.date_range(start=start_date, end=end_date, freq='H')
        data = []
        
        for date in dates:
            hour = date.hour
            # Simulate realistic patterns
            if 9 <= hour <= 17:
                base_multiplier = random.uniform(1.2, 1.8)
            else:
                base_multiplier = random.uniform(0.4, 0.9)
                
            data.append({
                'timestamp': date,
                'revenue': self.base_revenue * base_multiplier * random.uniform(0.8, 1.2),
                'users': int(self.base_users * base_multiplier * random.uniform(0.7, 1.3)),
                'conversion_rate': random.uniform(2.5, 4.2),
                'response_time': random.uniform(300, 2000)
            })
        
        return pd.DataFrame(data)
