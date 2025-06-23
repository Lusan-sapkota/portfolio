import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import current_app, render_template_string
from typing import List, Optional, Dict
from datetime import datetime
import logging
import requests
import socket

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ip_info(ip_address: str) -> Dict[str, str]:
    """
    Get geolocation information for an IP address
    """
    try:
        # Handle localhost/private IPs
        if ip_address in ['127.0.0.1', '::1', 'localhost'] or ip_address.startswith('192.168.') or ip_address.startswith('10.') or ip_address.startswith('172.'):
            return {
                'ip': ip_address,
                'city': 'Local/Private Network',
                'region': 'Local',
                'country': 'Local',
                'timezone': 'Local Timezone',
                'isp': 'Local Network',
                'org': 'Private Network'
            }
        
        # Use ip-api.com for geolocation (free service)
        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    'ip': ip_address,
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('regionName', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'timezone': data.get('timezone', 'Unknown'),
                    'isp': data.get('isp', 'Unknown'),
                    'org': data.get('org', 'Unknown'),
                    'lat': data.get('lat', 'Unknown'),
                    'lon': data.get('lon', 'Unknown')
                }
    except Exception as e:
        logger.warning(f"Failed to get IP info for {ip_address}: {e}")
    
    # Fallback info
    return {
        'ip': ip_address,
        'city': 'Unknown',
        'region': 'Unknown',
        'country': 'Unknown',
        'timezone': 'Unknown',
        'isp': 'Unknown',
        'org': 'Unknown'
    }

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('MAIL_PORT', 587))
        self.email_user = os.getenv('MAIL_USERNAME')
        self.email_password = os.getenv('MAIL_PASSWORD')
        self.from_name = os.getenv('FROM_NAME', "Lusan's Portfolio")
        
    def send_email(self, to_emails: List[str], subject: str, body: str, 
                   html_body: Optional[str] = None, attachments: Optional[List[str]] = None) -> bool:
        """
        Send email to one or more recipients
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <contact@lusansapkota.com.np>"
            msg.add_header('Reply-To', 'contact@lusansapkota.com.np')
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject
            
            # Add text content
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML content if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    if os.path.isfile(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_user, to_emails, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_emails}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_donation_confirmation(self, donor_email: str, donor_name: str, 
                                 project_title: str, amount: float) -> bool:
        """
        Send donation confirmation email
        """
        subject = f"Thank you for supporting {project_title}!"
        
        text_body = f"""
        Dear {donor_name},

        Thank you for your generous donation of ${amount:.2f} to support "{project_title}".

        Your contribution helps me continue developing and maintaining this project. 
        I truly appreciate your support!

        Best regards,
        The Development Team
        """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Thank you for your donation!</h2>
                
                <p>Dear <strong>{donor_name}</strong>,</p>
                
                <p>Thank you for your generous donation of <strong>${amount:.2f}</strong> to support 
                "<strong>{project_title}</strong>".</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0;">
                    <p><strong>Donation Details:</strong></p>
                    <ul>
                        <li>Project: {project_title}</li>
                        <li>Amount: ${amount:.2f}</li>
                        <li>Date: {datetime.now().strftime('%B %d, %Y')}</li>
                    </ul>
                </div>
                
                <p>Your contribution helps me continue developing and maintaining this project. 
                I truly appreciate your support!</p>
                
                <p>Best regards,<br>
                <strong>The Development Team</strong></p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email([donor_email], subject, text_body, html_body)
    
    def send_newsletter(self, subscribers: List[str], subject: str, content: str) -> bool:
        """
        Send newsletter to subscribers with proper unsubscribe links
        """
        success_count = 0
        
        for email in subscribers:
            try:
                # Generate unsubscribe token
                import base64
                unsubscribe_token = base64.b64encode(email.encode()).decode()
                unsubscribe_url = f"https://lusansapkota.com.np/newsletter/unsubscribe/{unsubscribe_token}"
                
                html_template = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Newsletter</title>
                </head>
                <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;">
                    <div style="padding: 40px 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 16px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15); overflow: hidden;">
                        
                        <!-- Header -->
                        <header style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); padding: 40px 30px; text-align: center; position: relative;">
                        <div style="position: relative; z-index: 1;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            📧 Lusan's Portfolio Newsletter
                            </h1>
                            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px; font-weight: 300;">
                            Latest updates from the world of development
                            </p>
                        </div>
                        </header>
                        
                        <!-- Content -->
                        <div style="padding: 40px 30px;">
                        <div style="background: #f8f9fa; border-left: 4px solid #f39c12; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                            <h2 style="color: #2c3e50; margin: 0 0 15px 0; font-size: 18px; font-weight: 600;">
                            🎯 What's New This Week
                            </h2>
                            <div style="color: #555; line-height: 1.7; font-size: 15px;">
                            {content}
                            </div>
                        </div>
                        
                        <!-- Call to Action -->
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="https://lusansapkota.com.np" style="display: inline-block; background: linear-gradient(135deg, #f39c12, #e67e22); color: #ffffff; text-decoration: none; padding: 15px 30px; border-radius: 50px; font-weight: 600; font-size: 16px; box-shadow: 0 8px 20px rgba(243, 156, 18, 0.3); transition: all 0.3s ease; border: none;">
                            🌐 Visit My Portfolio
                            </a>
                        </div>
                        
                        <!-- Social Links -->
                        <div style="text-align: center; margin: 30px 0; padding: 20px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 12px;">
                            <p style="color: #666; margin: 0 0 15px 0; font-size: 14px; font-weight: 500;">Connect with me:</p>
                            <div style="text-align: center;">
                            <a href="https://linkedin.com/in/lusansapkota" style="display: inline-block; margin: 0 10px; padding: 8px 16px; background: #0077b5; color: white; text-decoration: none; border-radius: 25px; font-size: 14px; font-weight: 500;">📊 LinkedIn</a>
                            <a href="https://github.com/lusansapkota" style="display: inline-block; margin: 0 10px; padding: 8px 16px; background: #333; color: white; text-decoration: none; border-radius: 25px; font-size: 14px; font-weight: 500;">💻 GitHub</a>
                            <a href="mailto:contact@lusansapkota.com.np" style="display: inline-block; margin: 0 10px; padding: 8px 16px; background: #e74c3c; color: white; text-decoration: none; border-radius: 25px; font-size: 14px; font-weight: 500;">📧 Email</a>
                            </div>
                        </div>
                        </div>
                        
                        <!-- Footer -->
                        <footer style="background: #2c3e50; padding: 30px; text-align: center;">
                        <div style="margin-bottom: 20px;">
                            <h3 style="color: #ffffff; margin: 0 0 10px 0; font-size: 20px; font-weight: 600;">Lusan Sapkota</h3>
                            <p style="color: #bdc3c7; margin: 0; font-size: 14px;">Full Stack Developer & Tech Enthusiast</p>
                        </div>
                        
                        <div style="border-top: 1px solid #34495e; padding-top: 20px; color: #95a5a6; font-size: 13px; line-height: 1.6;">
                            <p style="margin: 0 0 10px 0;">📧 You're receiving this because you subscribed to my newsletter</p>
                            <p style="margin: 0;">
                            <a href="{unsubscribe_url}" style="color: #e74c3c; text-decoration: none; font-weight: 500;">Unsubscribe from this newsletter</a>
                            </p>
                            <p style="margin: 15px 0 0 0; font-size: 12px; opacity: 0.8; color: #f1c40f; font-weight: 600;">
                            📍 Kathmandu, Nepal | 🌐 <span>lusansapkota.com.np</span>
                            </p>
                        </div>
                        </footer>
                    </div>
                    
                    <!-- Bottom spacing -->
                    <div style="height: 40px;"></div>
                    </div>
                </body>
                </html>
                """
                
                # Create plain text version
                text_content = f"""
                LUSAN'S PORTFOLIO NEWSLETTER
                ============================
                
                What's New This Week:
                {content}
                
                Visit my portfolio: https://lusansapkota.com.np
                
                ---
                You're receiving this email because you subscribed to my newsletter.
                To unsubscribe, visit: {unsubscribe_url}
                
                Lusan Sapkota - Full Stack Developer
                Kathmandu, Nepal
                """
                
                if self.send_email([email], subject, text_content, html_template):
                    success_count += 1
                    
            except Exception as e:
                logger.error(f"Failed to send newsletter to {email}: {e}")
                continue
                
        logger.info(f"Newsletter sent to {success_count}/{len(subscribers)} subscribers")
        return success_count > 0
    
    def send_contact_notification(self, name: str, email: str, subject: str, message: str) -> bool:
        """
        Send contact form notification to admin
        """
        admin_email = "contact@lusansapkota.com.np"
        notification_subject = f"New Contact Form Submission - {subject or 'No Subject'}"
        
        text_body = f"""
        New contact form submission received:

        Name: {name}
        Email: {email}
        Subject: {subject or 'No Subject'}
        
        Message:
        {message}
        
        ---
        Sent from Portfolio Contact Form
        """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50; border-bottom: 2px solid #f39c12; padding-bottom: 10px;">
                    New Contact Form Submission
                </h2>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                    <p><strong>Subject:</strong> {subject or 'No Subject'}</p>
                </div>
                
                <div style="margin: 20px 0;">
                    <h3 style="color: #2c3e50;">Message:</h3>
                    <div style="background: #fff; padding: 15px; border-left: 4px solid #f39c12; white-space: pre-wrap;">
{message}
                    </div>
                </div>
                
                <footer style="border-top: 1px solid #eee; padding-top: 20px; text-align: center; color: #666; font-size: 0.9em;">
                    <p>Sent from Portfolio Contact Form</p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        return self.send_email([admin_email], notification_subject, text_body, html_body)
    
    def send_contact_auto_reply(self, name: str, email: str, subject: str) -> bool:
        """
        Send auto-reply to contact form submitter
        """
        reply_subject = f"Thank you for contacting me - {subject or 'Your Message'}"
        
        text_body = f"""
        Hi {name},

        Thank you for reaching out to me through my portfolio website. I have received your message and will get back to you as soon as possible, usually within 24-48 hours.

        If your inquiry is urgent, please feel free to reach out to me directly at sapkotalusan@gmail.com.

        I appreciate your interest and look forward to connecting with you!

        Best regards,
        Lusan Sapkota
        Full Stack Developer
        https://lusansapkota.com.np
        """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <header style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2c3e50; margin-bottom: 10px;">Thank you for contacting me!</h1>
                    <div style="height: 3px; background: linear-gradient(135deg, #f39c12, #e67e22); border-radius: 2px;"></div>
                </header>
                
                <div style="margin-bottom: 30px;">
                    <p>Hi <strong>{name}</strong>,</p>
                    
                    <p>Thank you for reaching out to me through my portfolio website. I have received your message and will get back to you as soon as possible, usually within <strong>24-48 hours</strong>.</p>
                    
                    <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0; color: #856404;">
                            <strong>📧 Urgent inquiries:</strong> Feel free to reach out directly at 
                            <a href="mailto:contact@lusansapkota.com.np" style="color: #f39c12;">contact@lusansapkota.com.np</a>
                        </p>
                    </div>
                    
                    <p>I appreciate your interest and look forward to connecting with you!</p>
                </div>
                
                <footer style="border-top: 1px solid #eee; padding-top: 20px; text-align: center;">
                    <div style="margin-bottom: 15px;">
                        <h3 style="color: #2c3e50; margin-bottom: 5px;">Lusan Sapkota</h3>
                        <p style="color: #f39c12; margin: 0; font-weight: 500;">Full Stack Developer</p>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <a href="https://lusansapkota.com.np" style="color: #f39c12; text-decoration: none; font-weight: 500;">
                            🌐 lusansapkota.com.np
                        </a>
                    </div>
                    
                    <div style="color: #666; font-size: 0.9em;">
                        <p style="margin: 0;">This is an automated response. You can reply if it's urgent otherwise i will do it.</p>
                    </div>
                </footer>
            </div>
        </body>
        </html>
        """
        
        return self.send_email([email], reply_subject, text_body, html_body)
    
    def send_donation_thank_you(self, email: str, name: str, amount: float, project_title: str, currency: str = 'USD') -> bool:
        """
        Send a thank you email for donation
        """
        # Format currency symbol and amount
        if currency.upper() == 'NPR':
            currency_symbol = '₨'
            formatted_amount = f"₨{amount:,.2f}"
            currency_name = 'Nepalese Rupees'
        elif currency.upper() == 'USD':
            currency_symbol = '$'
            formatted_amount = f"${amount:,.2f}"
            currency_name = 'US Dollars'
        else:
            currency_symbol = currency
            formatted_amount = f"{currency} {amount:,.2f}"
            currency_name = currency
        
        subject = f"Thank you for your generous donation to {project_title}!"
        
        text_body = f"""
        Dear {name},

        Thank you so much for your generous donation of {formatted_amount} to {project_title}!

        Your support means the world to me and helps me continue building amazing projects that benefit the entire developer community. Every contribution, no matter the size, makes a real difference in advancing technology and creating valuable resources.

        What happens next:
        ✅ Your donation is being processed
        ✅ You'll receive an update when the processing is complete
        ✅ You can track the project's progress on my donation page

        I'm truly grateful for supporters like you who believe in open source innovation and community-driven development.

        If you have any questions or would like to connect, feel free to reach out anytime.

        With sincere appreciation,
        Lusan Sapkota
        Full Stack Developer

        🌐 https://lusansapkota.com.np
        💙 https://donate.lusansapkota.com.np
        """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <header style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2c3e50; margin-bottom: 10px;">Thank you for your donation! 💙</h1>
                    <div style="height: 3px; background: linear-gradient(135deg, #f39c12, #e67e22); border-radius: 2px;"></div>
                </header>
                
                <div style="margin-bottom: 30px;">
                    <p>Dear <strong>{name}</strong>,</p>
                    
                    <p>Thank you so much for your generous donation of <strong>{formatted_amount}</strong> to <strong>{project_title}</strong>!</p>
                    
                    <div style="background: #d4edda; border: 1px solid #c3e6cb; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                        <h3 style="color: #155724; margin: 0 0 10px 0;">Donation Amount</h3>
                        <div style="font-size: 2em; color: #28a745; font-weight: bold; margin: 10px 0;">{formatted_amount}</div>
                        <p style="margin: 5px 0; color: #155724;">for {project_title}</p>
                        <small style="color: #6c757d;">({currency_name})</small>
                    </div>
                    
                    <p>Your support means the world to me and helps me continue building amazing projects that benefit the entire developer community. Every contribution, no matter the size, makes a real difference in advancing technology and creating valuable resources.</p>
                    
                    <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <h4 style="color: #856404; margin: 0 0 10px 0;">What happens next:</h4>
                        <ul style="color: #856404; margin: 0; padding-left: 20px;">
                            <li>✅ Your donation is being processed</li>
                            <li>✅ You'll receive an update when the processing is complete</li>
                            <li>✅ You can track the project's progress on my donation page</li>
                        </ul>
                    </div>
                    
                    {f'''
                    <div style="background: #e7f3ff; border: 1px solid #b8daff; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <h4 style="color: #0c5460; margin: 0 0 10px 0;">💡 Payment Note:</h4>
                        <p style="color: #0c5460; margin: 0;">
                            {f"You selected to pay in {currency_name}. Please complete your payment using the instructions provided. The exact amount I receive may differ slightly due to transaction fees or exchange rates, and I'll record the actual amount received." if currency == 'NPR' else "You selected to pay in US Dollars. International payment processing may take 1-3 business days depending on your payment method."}
                        </p>
                    </div>
                    ''' if currency else ''}
                    
                    <p>I'm truly grateful for supporters like you who believe in open source innovation and community-driven development.</p>
                    
                    <p>If you have any questions or would like to connect, feel free to reach out anytime.</p>
                </div>
                
                <footer style="border-top: 1px solid #eee; padding-top: 20px; text-align: center;">
                    <div style="margin-bottom: 15px;">
                        <h3 style="color: #2c3e50; margin-bottom: 5px;">With sincere appreciation,</h3>
                        <h3 style="color: #2c3e50; margin-bottom: 5px;">Lusan Sapkota</h3>
                        <p style="color: #f39c12; margin: 0; font-weight: 500;">Full Stack Developer</p>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <a href="https://lusansapkota.com.np" style="color: #f39c12; text-decoration: none; font-weight: 500; margin-right: 20px;">
                            🌐 Portfolio
                        </a>
                        <a href="https://donate.lusansapkota.com.np" style="color: #f39c12; text-decoration: none; font-weight: 500;">
                            💙 Donations
                        </a>
                    </div>
                    
                    <div style="color: #666; font-size: 0.9em;">
                        <p style="margin: 0;">Thank you for supporting open source innovation!</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.8em;">
                            💸 Donation in {currency_name} • Sent on {datetime.now().strftime('%B %d, %Y')}
                        </p>
                    </div>
                </footer>
            </div>
        </body>
        </html>
        """
        
        return self.send_email([email], subject, text_body, html_body)

    def send_admin_notification(self, username: str, ip_address: str, timestamp: datetime) -> bool:
        """
        Send admin login notification email with IP geolocation
        """
        try:
            # Get IP geolocation info
            ip_info = get_ip_info(ip_address)
            
            # Format timestamp
            formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
            
            # Prepare email content
            subject = f"🚨 Admin Login Alert - {username}"
            
            # Text body
            text_body = f"""
ADMIN LOGIN ALERT
=================

An admin login has been detected for your portfolio website.

Login Details:
- Username: {username}
- Date & Time: {formatted_time}
- IP Address: {ip_info['ip']}
- Location: {ip_info['city']}, {ip_info['region']}, {ip_info['country']}
- ISP: {ip_info['isp']}
- Organization: {ip_info['org']}
- Timezone: {ip_info['timezone']}

If this was not you, please secure your admin account immediately!

Admin Panel: https://lusansapkota.com.np/admin
            """
            
            # HTML body
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Admin Login Alert</title>
            </head>
            <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f8f9fa;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    
                    <!-- Header -->
                    <header style="background: linear-gradient(135deg, #dc3545, #c82333); padding: 30px; text-align: center; color: white;">
                        <h1 style="margin: 0; font-size: 24px;">
                            🚨 Admin Login Alert
                        </h1>
                        <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 16px;">
                            Security Notification
                        </p>
                    </header>
                    
                    <!-- Content -->
                    <div style="padding: 30px;">
                        <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 20px; margin-bottom: 25px;">
                            <h3 style="color: #856404; margin: 0 0 10px 0; font-size: 18px;">
                                ⚠️ Admin Access Detected
                            </h3>
                            <p style="color: #856404; margin: 0; font-size: 14px;">
                                An administrator has successfully logged into your portfolio website.
                            </p>
                        </div>
                        
                        <div style="background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 25px;">
                            <h3 style="color: #343a40; margin: 0 0 15px 0; font-size: 18px;">
                                📊 Login Details
                            </h3>
                            
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px 0; font-weight: 600; color: #555;">👤 Username:</td>
                                    <td style="padding: 8px 0; color: #343a40; font-weight: 600;">{username}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: 600; color: #555;">🕐 Date & Time:</td>
                                    <td style="padding: 8px 0; color: #343a40; font-weight: 600;">{formatted_time}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: 600; color: #555;">🌐 IP Address:</td>
                                    <td style="padding: 8px 0; color: #343a40; font-weight: 600;">{ip_info['ip']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: 600; color: #555;">📍 Location:</td>
                                    <td style="padding: 8px 0; color: #343a40; font-weight: 600;">{ip_info['city']}, {ip_info['region']}, {ip_info['country']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: 600; color: #555;">🏢 ISP:</td>
                                    <td style="padding: 8px 0; color: #343a40; font-weight: 600;">{ip_info['isp']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: 600; color: #555;">🏢 Organization:</td>
                                    <td style="padding: 8px 0; color: #343a40; font-weight: 600;">{ip_info['org']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: 600; color: #555;">🕐 Timezone:</td>
                                    <td style="padding: 8px 0; color: #343a40; font-weight: 600;">{ip_info['timezone']}</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div style="background-color: #d1ecf1; border: 1px solid #bee5eb; padding: 20px; border-radius: 8px; margin-bottom: 25px;">
                            <h3 style="color: #0c5460; margin: 0 0 10px 0; font-size: 16px;">
                                🔒 Security Notice
                            </h3>
                            <p style="color: #0c5460; margin: 0; font-size: 14px; line-height: 1.5;">
                                If this login was not authorized by you, please:
                            </p>
                            <ul style="color: #0c5460; font-size: 14px; margin: 10px 0 0 20px; padding: 0;">
                                <li>Change your admin password immediately</li>
                                <li>Check for any unauthorized changes</li>
                                <li>Review admin activity logs</li>
                                <li>Consider enabling additional security measures</li>
                            </ul>
                        </div>
                        
                        <div style="text-align: center; margin: 25px 0;">
                            <a href="https://lusansapkota.com.np/admin" 
                               style="background: linear-gradient(135deg, #007bff, #0056b3); 
                                      color: white; 
                                      text-decoration: none; 
                                      padding: 12px 30px; 
                                      border-radius: 25px; 
                                      font-weight: 500; 
                                      display: inline-block;">
                                🔐 Access Admin Panel
                            </a>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <footer style="border-top: 1px solid #eee; padding: 20px; text-align: center; background-color: #f8f9fa; border-radius: 0 0 10px 10px;">
                        <p style="color: #6c757d; margin: 0; font-size: 14px;">
                            This is an automated security notification from your portfolio website.
                        </p>
                        <p style="color: #6c757d; margin: 5px 0 0 0; font-size: 12px;">
                            © 2025 Lusan's Portfolio. All rights reserved.
                        </p>
                    </footer>
                </div>
            </body>
            </html>
            """
            
            # Send to admin email
            admin_email = self.email_user  # Send to the configured email
            
            return self.send_email([admin_email], subject, text_body, html_body)
            
        except Exception as e:
            logger.error(f"Failed to send admin login notification: {e}")
            return False

    def send_password_change_notification(self, username: str, ip_address: str, timestamp: datetime) -> bool:
        """
        Send password change notification email
        """
        try:
            # Get IP geolocation info
            ip_info = get_ip_info(ip_address)
            
            # Format timestamp
            formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
            
            # Prepare email content
            subject = f"🔐 Password Changed - {username}"
            
            # Text body
            text_body = f"""
PASSWORD CHANGE NOTIFICATION
============================

Your admin password has been successfully changed.

Change Details:
- Username: {username}
- Date & Time: {formatted_time}
- IP Address: {ip_info['ip']}
- Location: {ip_info['city']}, {ip_info['region']}, {ip_info['country']}
- ISP: {ip_info['isp']}

If you did not make this change, please contact support immediately!

Admin Panel: https://lusansapkota.com.np/admin
            """
            
            # HTML body
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Password Change Notification</title>
            </head>
            <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f8f9fa;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    
                    <!-- Header -->
                    <header style="background: linear-gradient(135deg, #28a745, #20c997); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                        <h1 style="color: white; margin: 0; font-size: 24px;">
                            🔐 Password Changed Successfully
                        </h1>
                        <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 16px;">
                            Admin Security Notification
                        </p>
                    </header>
                    
                    <!-- Content -->
                    <div style="padding: 30px;">
                        <div style="background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; padding: 20px; margin-bottom: 25px;">
                            <h3 style="color: #155724; margin: 0 0 10px 0; font-size: 18px;">
                                ✅ Password Updated
                            </h3>
                            <p style="color: #155724; margin: 0; font-size: 14px;">
                                Your admin password has been successfully changed. You will need to use your new password for future logins.
                            </p>
                        </div>
                        
                        <div style="background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 25px;">
                            <h3 style="color: #343a40; margin: 0 0 15px 0; font-size: 18px;">
                                📋 Change Details
                            </h3>
                            
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px 0; font-weight: 600; color: #555;">Admin User:</td>
                                    <td style="padding: 8px 0; color: #343a40; font-weight: 600;">{username}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: 600; color: #555;">🌐 IP Address:</td>
                                    <td style="padding: 8px 0; color: #343a40; font-weight: 600;">{ip_info['ip']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: 600; color: #555;">📍 Location:</td>
                                    <td style="padding: 8px 0; color: #343a40; font-weight: 600;">{ip_info['city']}, {ip_info['region']}, {ip_info['country']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: 600; color: #555;">🏢 ISP:</td>
                                    <td style="padding: 8px 0; color: #343a40; font-weight: 600;">{ip_info['isp']}</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 20px; margin-bottom: 25px;">
                            <h3 style="color: #856404; margin: 0 0 10px 0; font-size: 16px;">
                                🛡️ Security Notice
                            </h3>
                            <p style="color: #856404; margin: 0; font-size: 14px; line-height: 1.5;">
                                If you did not make this password change, please contact support immediately and:
                            </p>
                            <ul style="color: #856404; font-size: 14px; margin: 10px 0 0 20px; padding: 0;">
                                <li>Secure your account immediately</li>
                                <li>Check for any unauthorized changes</li>
                                <li>Review admin activity logs</li>
                                <li>Contact support if you suspect unauthorized access</li>
                            </ul>
                        </div>
                        
                        <div style="background-color: #e2e3e5; border-radius: 8px; padding: 20px; margin-bottom: 25px;">
                            <h3 style="color: #383d41; margin: 0 0 10px 0; font-size: 16px;">
                                💡 Security Best Practices
                            </h3>
                            <ul style="color: #383d41; font-size: 14px; margin: 10px 0 0 20px; padding: 0; line-height: 1.6;">
                                <li>Use a unique password not used elsewhere</li>
                                <li>Consider using a password manager</li>
                                <li>Enable two-factor authentication if available</li>
                                <li>Log out from shared or public computers</li>
                                <li>Regularly review admin activity logs</li>
                            </ul>
                        </div>
                        
                        <div style="text-align: center; margin: 25px 0;">
                            <a href="https://lusansapkota.com.np/admin" 
                               style="background: linear-gradient(135deg, #007bff, #0056b3); 
                                      color: white; 
                                      text-decoration: none; 
                                      padding: 12px 30px; 
                                      border-radius: 25px; 
                                      font-weight: 500; 
                                      display: inline-block;">
                                🔐 Access Admin Panel
                            </a>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <footer style="border-top: 1px solid #eee; padding: 20px; text-align: center; background-color: #f8f9fa; border-radius: 0 0 10px 10px;">
                        <p style="color: #6c757d; margin: 0; font-size: 14px;">
                            This is an automated security notification from your portfolio website.
                        </p>
                        <p style="color: #6c757d; margin: 5px 0 0 0; font-size: 12px;">
                            © 2025 Lusan's Portfolio. All rights reserved.
                        </p>
                    </footer>
                </div>
            </body>
            </html>
            """
            
            # Send to admin email
            admin_email = self.email_user  # Send to the configured email
            
            return self.send_email([admin_email], subject, text_body, html_body)
            
        except Exception as e:
            logger.error(f"Failed to send password change notification: {e}")
            return False
    
    def send_admin_donation_notification(self, donation, project_title: str) -> bool:
        """
        Send notification to admin when a new donation is made
        """
        try:
            # Format amount based on currency
            if donation.currency == 'NPR':
                amount_display = f"Rs. {donation.amount:.2f}"
            else:
                amount_display = f"${donation.amount:.2f}"
            
            subject = f"New Donation Alert: {amount_display} for {project_title}"
            
            text_body = f"""
New Donation Received!

A new donation has been submitted and requires your attention.

Donation Details:
- Project: {project_title}
- Amount: {amount_display}
- Donor: {'Anonymous' if donation.is_anonymous else donation.donor_name}
- Email: {donation.donor_email if not donation.is_anonymous else 'Hidden (Anonymous)'}
- Phone: {donation.donor_phone or 'Not provided'}
- Payment Method: {donation.payment_method or 'Not specified'}
- Status: {donation.status}
- Date: {donation.created_at.strftime('%B %d, %Y at %I:%M %p') if donation.created_at else 'N/A'}

{f'Message from donor: "{donation.message}"' if donation.message else ''}

Please log in to the admin panel to verify this donation and update its status.

Admin Panel: https://lusansapkota.com.np/admin/donations

Best regards,
Portfolio Donation System
"""
            
            html_body = f"""
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Donation Alert</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8f9fa;">
    <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 10px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); overflow: hidden;">
        
        <!-- Header -->
        <header style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 30px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">
                🔔 New Donation Alert
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">
                A new donation requires your attention
            </p>
        </header>
        
        <!-- Content -->
        <div style="padding: 30px;">
            <div style="background: #e8f5e8; border-left: 4px solid #28a745; padding: 20px; margin-bottom: 20px; border-radius: 5px;">
                <h2 style="color: #155724; margin: 0 0 10px 0; font-size: 20px;">
                    Donation Amount: {amount_display}
                </h2>
                <p style="color: #155724; margin: 0; font-size: 16px;">
                    Project: <strong>{project_title}</strong>
                </p>
            </div>
            
            <h3 style="color: #333; margin-bottom: 15px;">Donation Details:</h3>
            <p>Donor: {'Anonymous' if donation.is_anonymous else donation.donor_name}</p>
            <p>Email: {donation.donor_email if not donation.is_anonymous else 'Hidden (Anonymous)'}</p>
            <p>Phone: {donation.donor_phone or 'Not provided'}</p>
            <p>Payment Method: {donation.payment_method or 'Not specified'}</p>
            <p>Status: {donation.status}</p>
            <p>Date: {donation.created_at.strftime('%B %d, %Y at %I:%M %p') if donation.created_at else 'N/A'}</p>
            
            {f'<div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 15px; margin-bottom: 20px;"><h4 style="color: #856404; margin: 0 0 10px 0;">Message from donor:</h4><p style="color: #856404; margin: 0; font-style: italic;">"{donation.message}"</p></div>' if donation.message else ''}
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="https://lusansapkota.com.np/admin/donations" 
                   style="background: #007bff; 
                          color: white; 
                          text-decoration: none; 
                          padding: 12px 24px; 
                          border-radius: 6px; 
                          font-weight: 500; 
                          display: inline-block;">
                    🔐 Verify in Admin Panel
                </a>
            </div>
            
            <p style="color: #6c757d; text-align: center; margin-top: 20px; font-size: 14px;">
                Please confirm the payment status and update the donation accordingly.
            </p>
        </div>
        
        <!-- Footer -->
        <footer style="border-top: 1px solid #eee; padding: 20px; text-align: center; background-color: #f8f9fa;">
            <p style="color: #6c757d; margin: 0; font-size: 14px;">
                This is an automated notification from your portfolio donation system.
            </p>
        </footer>
    </div>
</body>
</html>
"""
            
            # Send to admin email (sapkotalusan@gmail.com)
            admin_email = "sapkotalusan@gmail.com"
            
            return self.send_email([admin_email], subject, text_body, html_body)
            
        except Exception as e:
            logger.error(f"Failed to send admin donation notification: {e}")
            return False

    def send_donation_confirmation(self, donation, project_title: str, confirmation_amount: float = None) -> bool:
        """
        Send confirmation email to donor when donation is marked as complete
        """
        try:
            # Use provided amount or fall back to verified/original amount
            display_amount = confirmation_amount or donation.verified_amount or donation.amount
            
            # Format amount based on currency
            if donation.currency == 'NPR':
                amount_display = f"Rs. {display_amount:.2f}"
            else:
                amount_display = f"${display_amount:.2f}"
            
            subject = f"Donation Confirmed: Thank you for supporting {project_title}!"
            
            text_body = f"""
Dear {donation.donor_name if not donation.is_anonymous else 'Valued Supporter'},

I are delighted to confirm that your donation has been successfully processed!

Donation Confirmation Details:
- Project: {project_title}
- Confirmed Amount: {amount_display}
- Date Processed: {datetime.now().strftime('%B %d, %Y')}
- Status: CONFIRMED

Your generous contribution will help advance this project and make a meaningful impact. 
{'Your donation has been made anonymously as requested.' if donation.is_anonymous else 'Your name will be added to my supporters list to recognize your contribution.'}

{f'Your message: "{donation.message}"' if donation.message else ''}

Thank you once again for your support and trust in my work.

View all supporters: https://lusansapkota.com.np/donation/thanksgiving

With gratitude,
Lusan Sapkota
"""
            
            html_body = f"""
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Donation Confirmed</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8f9fa;">
    <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 10px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); overflow: hidden;">
        
        <!-- Header -->
        <header style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 30px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">
                ✅ Donation Confirmed!
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">
                Thank you for your generous support
            </p>
        </header>
        
        <!-- Content -->
        <div style="padding: 30px;">
            <p style="font-size: 18px; color: #333; margin-bottom: 20px;">
                Dear {donation.donor_name if not donation.is_anonymous else 'Valued Supporter'},
            </p>
            
            <p style="color: #333; line-height: 1.6; margin-bottom: 20px;">
                I are delighted to confirm that your donation has been successfully processed! 
                Your support means the world to me.
            </p>
            
            <div style="background: #e8f5e8; border: 1px solid #d4edda; border-radius: 8px; padding: 20px; margin: 20px 0;">
                <h3 style="color: #155724; margin: 0 0 10px 0; font-size: 18px;">
                    ✅ Donation Confirmed
                </h3>
                <p>Project: {project_title}</p>
                <p style="font-size: 18px; color: #28a745; font-weight: bold;">Confirmed Amount: {amount_display}</p>
                <p>Date Processed: {datetime.now().strftime('%B %d, %Y')}</p>
                <p><span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">CONFIRMED</span></p>
            </div>
            
            <p style="color: #333; line-height: 1.6; margin-bottom: 20px;">
                Your generous contribution will help advance this project and make a meaningful impact.
                {'Your donation has been made anonymously as requested.' if donation.is_anonymous else 'Your name will be added to my supporters list to recognize your contribution.'}
            </p>
            
            {f'<div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 15px; margin-bottom: 20px;"><h4 style="color: #856404; margin: 0 0 10px 0;">Your message:</h4><p style="color: #856404; margin: 0; font-style: italic;">"{donation.message}"</p></div>' if donation.message else ''}
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://lusansapkota.com.np/donation/thanksgiving" 
                   style="background: #007bff; 
                          color: white; 
                          text-decoration: none; 
                          padding: 12px 24px; 
                          border-radius: 6px; 
                          font-weight: 500; 
                          display: inline-block;">
                    ❤️ View All Supporters
                </a>
            </div>
            
            <p style="color: #333; line-height: 1.6; margin-top: 30px;">
                Thank you once again for your support and trust in my work.
            </p>
            
            <p style="color: #333; font-weight: bold;">
                With gratitude,<br>
                Lusan Sapkota
            </p>
        </div>
        
        <!-- Footer -->
        <footer style="border-top: 1px solid #eee; padding: 20px; text-align: center; background-color: #f8f9fa;">
            <p style="color: #6c757d; margin: 0; font-size: 14px;">
                Thank you for supporting open source development and innovation.
            </p>
        </footer>
    </div>
</body>
</html>
"""
            
            return self.send_email([donation.donor_email], subject, text_body, html_body)
            
        except Exception as e:
            logger.error(f"Failed to send donation confirmation email: {e}")
            return False

# Initialize email service
email_service = EmailService()
