import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import current_app, render_template_string
from typing import List, Optional
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.from_name = os.getenv('FROM_NAME', 'Lusan Portfolio')
        
    def send_email(self, to_emails: List[str], subject: str, body: str, 
                   html_body: Optional[str] = None, attachments: Optional[List[str]] = None) -> bool:
        """
        Send email to one or more recipients
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.email_user}>"
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

        Your contribution helps us continue developing and maintaining this project. 
        We truly appreciate your support!

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
                
                <p>Your contribution helps us continue developing and maintaining this project. 
                We truly appreciate your support!</p>
                
                <p>Best regards,<br>
                <strong>The Development Team</strong></p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email([donor_email], subject, text_body, html_body)
    
    def send_newsletter(self, subscribers: List[str], subject: str, content: str) -> bool:
        """
        Send newsletter to subscribers
        """
        html_template = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <header style="text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 20px; margin-bottom: 30px;">
                    <h1 style="color: #2c3e50;">Lusan's Portfolio Newsletter</h1>
                </header>
                
                <div style="margin-bottom: 30px;">
                    {content}
                </div>
                
                <footer style="border-top: 1px solid #eee; padding-top: 20px; text-align: center; color: #666;">
                    <p>You're receiving this email because you subscribed to our newsletter.</p>
                    <p><a href="#" style="color: #3498db;">Unsubscribe</a></p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(subscribers, subject, content, html_template)

# Initialize email service
email_service = EmailService()
