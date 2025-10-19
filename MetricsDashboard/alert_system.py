import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config

class AlertSystem:
    def __init__(self):
        self.alert_history = []
        self.last_alert_time = {}
        self.cooldown_period = 300  # 5 minutes in seconds
        
    def check_thresholds(self, metrics):
        """Check if any metrics exceed defined thresholds"""
        alerts = []
        current_time = datetime.now()
        
        # Check each metric against thresholds
        for metric, threshold in config.ALERT_THRESHOLDS.items():
            if metric in metrics:
                value = metrics[metric]
                
                # Check if threshold is exceeded
                if self._is_threshold_exceeded(metric, value, threshold):
                    # Check cooldown period
                    if self._can_send_alert(metric, current_time):
                        alert = {
                            'metric': metric,
                            'value': value,
                            'threshold': threshold,
                            'timestamp': current_time,
                            'severity': self._get_severity(metric, value, threshold)
                        }
                        alerts.append(alert)
                        self.last_alert_time[metric] = current_time
                        
        return alerts
    
    def _is_threshold_exceeded(self, metric, value, threshold):
        """Check if a specific metric exceeds its threshold"""
        if metric in ['cpu_usage', 'memory_usage', 'error_rate', 'response_time']:
            return value > threshold
        elif metric == 'revenue':
            return value < threshold  # Alert if revenue drops below threshold
        return False
    
    def _can_send_alert(self, metric, current_time):
        """Check if we can send an alert (respecting cooldown period)"""
        if metric not in self.last_alert_time:
            return True
        
        time_diff = (current_time - self.last_alert_time[metric]).total_seconds()
        return time_diff >= self.cooldown_period
    
    def _get_severity(self, metric, value, threshold):
        """Determine alert severity"""
        if metric in ['cpu_usage', 'memory_usage']:
            if value > threshold * 1.2:
                return 'CRITICAL'
            elif value > threshold * 1.1:
                return 'HIGH'
            else:
                return 'MEDIUM'
        elif metric == 'error_rate':
            if value > threshold * 2:
                return 'CRITICAL'
            else:
                return 'HIGH'
        else:
            return 'MEDIUM'
    
    def send_email_alert(self, alert):
        """Send email notification for alerts"""
        try:
            msg = MIMEMultipart()
            msg['From'] = config.EMAIL_CONFIG['sender_email']
            msg['To'] = config.EMAIL_CONFIG['recipient_email']
            msg['Subject'] = f"🚨 KPI Alert: {alert['metric'].upper()} - {alert['severity']}"
            
            body = f"""
            Alert Details:
            
            Metric: {alert['metric'].replace('_', ' ').title()}
            Current Value: {alert['value']:.2f}
            Threshold: {alert['threshold']:.2f}
            Severity: {alert['severity']}
            Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
            
            Please investigate immediately.
            
            MetricsDashboard Alert System
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(config.EMAIL_CONFIG['smtp_server'], config.EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(config.EMAIL_CONFIG['sender_email'], config.EMAIL_CONFIG['sender_password'])
            text = msg.as_string()
            server.sendmail(config.EMAIL_CONFIG['sender_email'], config.EMAIL_CONFIG['recipient_email'], text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Failed to send email alert: {str(e)}")
            return False
    
    def log_alert(self, alert):
        """Log alert to history"""
        self.alert_history.append(alert)
        
        # Keep only last 100 alerts
        if len(self.alert_history) > 100:
            self.alert_history = self.alert_history[-100:]
    
    def get_recent_alerts(self, limit=10):
        """Get recent alerts"""
        return self.alert_history[-limit:] if self.alert_history else []
