import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class AlertManager:
    def __init__(self, email_config=None):
        self.email_config = email_config or {}
        self.alert_thresholds = {
            'temperature': {'min': 18, 'max': 30},
            'humidity': {'min': 30, 'max': 70},
            'gas': {'min': 5000, 'max': 50000}
        }
        self.alert_history = []
    
    def check_alerts(self, readings):
        """Check if any readings trigger alerts"""
        alerts = []
        
        # Check temperature
        if not self.alert_thresholds['temperature']['min'] <= \
           readings['temperature'] <= \
           self.alert_thresholds['temperature']['max']:
            alerts.append({
                'type': 'temperature',
                'value': readings['temperature'],
                'threshold': self.alert_thresholds['temperature']
            })
        
        # Check humidity
        if not self.alert_thresholds['humidity']['min'] <= \
           readings['humidity'] <= \
           self.alert_thresholds['humidity']['max']:
            alerts.append({
                'type': 'humidity',
                'value': readings['humidity'],
                'threshold': self.alert_thresholds['humidity']
            })
        
        # Check gas levels
        if not self.alert_thresholds['gas']['min'] <= \
           readings['gas'] <= \
           self.alert_thresholds['gas']['max']:
            alerts.append({
                'type': 'gas',
                'value': readings['gas'],
                'threshold': self.alert_thresholds['gas']
            })
        
        if alerts:
            self._handle_alerts(alerts)
        
        return alerts
    
    def _handle_alerts(self, alerts):
        """Handle triggered alerts"""
        # Store in history
        self.alert_history.extend([
            {
                **alert,
                'timestamp': datetime.now()
            }
            for alert in alerts
        ])
        
        # Send notifications
        if self.email_config:
            self._send_alert_email(alerts)
    
    def _send_alert_email(self, alerts):
        """Send email notification for alerts"""
        if not self.email_config:
            return
        
        msg = MIMEMultipart()
        msg['From'] = self.email_config['from']
        msg['To'] = self.email_config['to']
        msg['Subject'] = 'Environmental Alert'
        
        body = 'The following alerts have been triggered:\n\n'
        for alert in alerts:
            body += f"- {alert['type'].title()}: {alert['value']} "
            body += f"(Threshold: {alert['threshold']})\n"
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(self.email_config['smtp_server'])
            server.starttls()
            server.login(
                self.email_config['username'],
                self.email_config['password']
            )
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f'Failed to send alert email: {e}')
    
    def get_alert_summary(self, hours=24):
        """Get summary of alerts in the past hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_alerts = [
            alert for alert in self.alert_history
            if alert['timestamp'] > cutoff
        ]
        
        return {
            'total': len(recent_alerts),
            'by_type': {
                alert_type: len([
                    a for a in recent_alerts
                    if a['type'] == alert_type
                ])
                for alert_type in ['temperature', 'humidity', 'gas']
            }
        }
