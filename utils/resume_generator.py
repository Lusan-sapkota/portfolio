"""
Resume Generator Utility
Generates a professional resume from portfolio database data.
Produces both TXT and HTML formats.
"""

from datetime import datetime
from models import PersonalInfo, SocialLink, Skill, Experience, Education, Project
from database import db
import os


def get_portfolio_data():
    """Fetch all required data from database for resume generation."""
    data = {
        'personal': PersonalInfo.query.first(),
        'social_links': SocialLink.query.filter_by(is_active=True).order_by(SocialLink.sort_order).all(),
        'skills': Skill.query.order_by(Skill.category, Skill.sort_order).all(),
        'experiences': Experience.query.order_by(Experience.is_current.desc(), Experience.start_date.desc()).all(),
        'education': Education.query.order_by(Education.is_current.desc(), Education.start_date.desc()).all(),
        'featured_projects': Project.query.filter_by(is_featured=True).order_by(Project.created_at.desc()).all(),
    }
    return data


def format_date_range(start_date, end_date, is_current=False):
    """Format date range for display."""
    if not start_date:
        return ""

    start_str = start_date.strftime('%b %Y')

    if is_current or not end_date:
        return f"{start_str} - Present"

    end_str = end_date.strftime('%b %Y')
    return f"{start_str} - {end_str}"


def group_skills_by_category(skills):
    """Group skills by their category."""
    grouped = {}
    category_order = ['programming', 'frontend', 'backend', 'database', 'devops', 'tools', 'other']

    for skill in skills:
        cat = skill.category or 'other'
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(skill)

    # Sort by predefined order
    sorted_grouped = {}
    for cat in category_order:
        if cat in grouped:
            sorted_grouped[cat] = grouped[cat]

    # Add any remaining categories
    for cat in grouped:
        if cat not in sorted_grouped:
            sorted_grouped[cat] = grouped[cat]

    return sorted_grouped


def get_category_display_name(category):
    """Get display name for skill category."""
    names = {
        'programming': 'Programming Languages',
        'frontend': 'Frontend Development',
        'backend': 'Backend Development',
        'database': 'Database & DevOps',
        'devops': 'DevOps & Cloud',
        'tools': 'Tools & Technologies',
        'other': 'Other Skills'
    }
    return names.get(category, category.title())


def generate_txt_resume(data):
    """Generate a professional TXT resume."""
    personal = data['personal']
    lines = []

    # Header
    lines.append("=" * 78)
    name = personal.name if personal else "LUSAN SAPKOTA"
    title = personal.title if personal else "Full Stack Developer"
    lines.append(f"{name.upper():^78}")
    lines.append(f"{title:^78}")
    lines.append("=" * 78)
    lines.append("")

    # Contact Information
    lines.append("CONTACT INFORMATION")
    lines.append("-" * 20)
    if personal:
        if personal.phone:
            lines.append(f"Phone: {personal.phone}")
        else:
            lines.append("Phone: Available upon request")
        if personal.email:
            lines.append(f"Email: {personal.email}")
        lines.append("Website: https://www.lusansapkota.com.np")
        if personal.location:
            lines.append(f"Location: {personal.location}")
    lines.append("")

    # Social Profiles
    if data['social_links']:
        lines.append("SOCIAL PROFILES")
        lines.append("-" * 15)
        platform_names = {
            'github': 'GitHub',
            'linkedin': 'LinkedIn',
            'twitter': 'X (Twitter)',
            'youtube': 'YouTube',
            'instagram': 'Instagram',
            'discord': 'Discord',
            'leetcode': 'LeetCode',
            'hackerrank': 'HackerRank',
            'facebook': 'Facebook'
        }
        for link in data['social_links']:
            platform_display = platform_names.get(link.platform.lower(), link.platform.title())
            lines.append(f"• {platform_display}: {link.url}")
        lines.append("")

    # Professional Summary
    lines.append("PROFESSIONAL SUMMARY")
    lines.append("-" * 20)
    if personal and personal.bio:
        # Word wrap the bio
        bio = personal.bio.replace('\n', ' ').replace('\r', '')
        words = bio.split()
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= 76:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
    else:
        lines.append("Passionate Full Stack Developer with expertise in modern web technologies,")
        lines.append("AI/ML, and building scalable applications.")
    lines.append("")

    # Education
    if data['education']:
        lines.append("EDUCATION")
        lines.append("-" * 9)
        for edu in data['education']:
            degree_line = f"{edu.degree}"
            if edu.field_of_study:
                degree_line += f" in {edu.field_of_study}"
            date_range = format_date_range(edu.start_date, edu.end_date, edu.is_current)
            if date_range:
                degree_line += f" ({date_range})"
            lines.append(degree_line)
            lines.append(edu.institution)
            if edu.location:
                lines.append(edu.location)
            if edu.grade:
                lines.append(f"• GPA/Grade: {edu.grade}")
            if edu.description:
                for desc_line in edu.description.split('\n'):
                    if desc_line.strip():
                        lines.append(f"• {desc_line.strip()}")
            lines.append("")

    # Technical Skills
    if data['skills']:
        lines.append("TECHNICAL SKILLS")
        lines.append("-" * 16)
        lines.append("")

        grouped = group_skills_by_category(data['skills'])
        for category, skills in grouped.items():
            lines.append(f"{get_category_display_name(category)}:")
            skill_items = []
            for skill in skills:
                proficiency = f" ({skill.proficiency}%)" if skill.proficiency else ""
                skill_items.append(f"• {skill.name}{proficiency}")

            for item in skill_items:
                lines.append(item)
            lines.append("")

    # Professional Experience
    if data['experiences']:
        lines.append("PROFESSIONAL EXPERIENCE")
        lines.append("-" * 23)
        lines.append("")

        for exp in data['experiences']:
            # Position and date
            date_range = format_date_range(exp.start_date, exp.end_date, exp.is_current)
            lines.append(f"{exp.position} ({date_range})")

            # Company
            company_line = exp.company
            if exp.location:
                company_line += f" · {exp.location}"
            lines.append(company_line)

            # Description/Achievements
            if exp.description:
                for desc_line in exp.description.split('\n'):
                    if desc_line.strip():
                        if desc_line.strip().startswith('•') or desc_line.strip().startswith('-'):
                            lines.append(desc_line.strip())
                        else:
                            lines.append(f"• {desc_line.strip()}")

            if exp.achievements:
                for ach_line in exp.achievements.split('\n'):
                    if ach_line.strip():
                        if ach_line.strip().startswith('•') or ach_line.strip().startswith('-'):
                            lines.append(ach_line.strip())
                        else:
                            lines.append(f"• {ach_line.strip()}")

            # Technologies
            if exp.technologies:
                lines.append(f"• Technologies: {exp.technologies}")

            lines.append("")

    # Featured Projects
    if data['featured_projects']:
        lines.append("KEY PROJECTS")
        lines.append("-" * 12)
        lines.append("")

        for i, project in enumerate(data['featured_projects'], 1):
            lines.append(f"{i}. {project.title}")
            if project.description:
                # Word wrap description
                desc = project.description.replace('\n', ' ').replace('\r', '')
                wrapped = []
                words = desc.split()
                current_line = "   • "
                for word in words:
                    if len(current_line) + len(word) + 1 <= 76:
                        current_line += (" " if len(current_line) > 5 else "") + word
                    else:
                        wrapped.append(current_line)
                        current_line = "     " + word
                if current_line.strip():
                    wrapped.append(current_line)
                for line in wrapped:
                    lines.append(line)

            if project.technologies:
                lines.append(f"   • Technologies: {project.technologies}")
            if project.github_url:
                lines.append(f"   • GitHub: {project.github_url}")
            if project.live_url:
                lines.append(f"   • Live: {project.live_url}")
            lines.append("")

    # Languages
    lines.append("LANGUAGES")
    lines.append("-" * 9)
    lines.append("• English (Fluent)")
    lines.append("• Nepali (Native)")
    lines.append("• Hindi (Conversational)")
    lines.append("")

    # Availability
    lines.append("AVAILABILITY")
    lines.append("-" * 12)
    lines.append("Available for freelance projects and remote work opportunities.")
    lines.append("")

    # References
    lines.append("REFERENCES")
    lines.append("-" * 10)
    lines.append("Available upon request.")
    lines.append("")

    # Footer
    lines.append("=" * 78)
    lines.append(f"Last Updated: {datetime.now().strftime('%B %d, %Y')}")
    lines.append("Resume created from portfolio data at: https://www.lusansapkota.com.np")
    lines.append("This resume is auto-generated from my live portfolio.")
    lines.append("Kindly contact me for my concise resume.")
    lines.append("=" * 78)

    return "\n".join(lines)


def generate_html_resume(data):
    """Generate a professional HTML resume for printing/PDF conversion."""
    personal = data['personal']

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{personal.name if personal else 'Resume'} - Resume</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 850px;
            margin: 0 auto;
            padding: 40px;
            background: #fff;
        }}

        @media print {{
            body {{
                padding: 20px;
            }}
        }}

        .header {{
            text-align: center;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}

        .header h1 {{
            font-size: 2.5rem;
            color: #2c3e50;
            margin-bottom: 5px;
            letter-spacing: 2px;
        }}

        .header .title {{
            font-size: 1.2rem;
            color: #7f8c8d;
            font-weight: 400;
        }}

        .contact-bar {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 15px;
            font-size: 0.9rem;
        }}

        .contact-bar a {{
            color: #3498db;
            text-decoration: none;
        }}

        .contact-bar span {{
            color: #666;
        }}

        .section {{
            margin-bottom: 25px;
        }}

        .section-title {{
            font-size: 1.1rem;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .summary {{
            text-align: justify;
            color: #555;
        }}

        .experience-item, .education-item {{
            margin-bottom: 20px;
        }}

        .experience-header, .education-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 5px;
        }}

        .position, .degree {{
            font-weight: 600;
            color: #2c3e50;
            font-size: 1.05rem;
        }}

        .date {{
            color: #7f8c8d;
            font-size: 0.9rem;
        }}

        .company, .institution {{
            color: #3498db;
            font-size: 0.95rem;
            margin-bottom: 8px;
        }}

        .description {{
            color: #555;
            font-size: 0.9rem;
        }}

        .description ul {{
            margin-left: 20px;
        }}

        .description li {{
            margin-bottom: 3px;
        }}

        .technologies {{
            margin-top: 8px;
            font-size: 0.85rem;
            color: #666;
        }}

        .technologies strong {{
            color: #555;
        }}

        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }}

        .skill-category {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 5px;
            border-left: 3px solid #3498db;
        }}

        .skill-category h4 {{
            color: #2c3e50;
            font-size: 0.9rem;
            margin-bottom: 8px;
        }}

        .skill-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .skill-tag {{
            background: #e8f4fd;
            color: #2980b9;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
        }}

        .projects-grid {{
            display: grid;
            gap: 15px;
        }}

        .project-item {{
            padding: 12px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 3px solid #27ae60;
        }}

        .project-item h4 {{
            color: #2c3e50;
            margin-bottom: 5px;
        }}

        .project-item p {{
            font-size: 0.9rem;
            color: #555;
            margin-bottom: 8px;
        }}

        .project-links {{
            font-size: 0.85rem;
        }}

        .project-links a {{
            color: #3498db;
            text-decoration: none;
            margin-right: 15px;
        }}

        .social-links {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .social-links a {{
            color: #3498db;
            text-decoration: none;
            padding: 5px 12px;
            background: #e8f4fd;
            border-radius: 15px;
            font-size: 0.85rem;
        }}

        .footer {{
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            text-align: center;
            font-size: 0.8rem;
            color: #999;
        }}

        @media (max-width: 600px) {{
            .skills-grid {{
                grid-template-columns: 1fr;
            }}

            .experience-header, .education-header {{
                flex-direction: column;
            }}

            .contact-bar {{
                flex-direction: column;
                align-items: center;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>{personal.name.upper() if personal else 'LUSAN SAPKOTA'}</h1>
        <div class="title">{personal.title if personal else 'Full Stack Developer'}</div>
        <div class="contact-bar">
            <span>📧 {personal.email if personal and personal.email else 'sapkotalusan@gmail.com'}</span>
            <span>🌐 <a href="https://www.lusansapkota.com.np">lusansapkota.com.np</a></span>
            <span>📍 {personal.location if personal and personal.location else 'Kathmandu, Nepal'}</span>
        </div>
    </header>
"""

    # Professional Summary
    if personal and personal.bio:
        html += f"""
    <section class="section">
        <h2 class="section-title">Professional Summary</h2>
        <p class="summary">{personal.bio}</p>
    </section>
"""

    # Experience
    if data['experiences']:
        html += """
    <section class="section">
        <h2 class="section-title">Professional Experience</h2>
"""
        for exp in data['experiences']:
            date_range = format_date_range(exp.start_date, exp.end_date, exp.is_current)
            html += f"""
        <div class="experience-item">
            <div class="experience-header">
                <span class="position">{exp.position}</span>
                <span class="date">{date_range}</span>
            </div>
            <div class="company">{exp.company}{' · ' + exp.location if exp.location else ''}</div>
            <div class="description">
"""
            if exp.description:
                html += "<ul>"
                for line in exp.description.split('\n'):
                    if line.strip():
                        clean_line = line.strip().lstrip('•-').strip()
                        html += f"<li>{clean_line}</li>"
                html += "</ul>"

            if exp.technologies:
                html += f'<div class="technologies"><strong>Technologies:</strong> {exp.technologies}</div>'

            html += """
            </div>
        </div>
"""
        html += "    </section>\n"

    # Education
    if data['education']:
        html += """
    <section class="section">
        <h2 class="section-title">Education</h2>
"""
        for edu in data['education']:
            date_range = format_date_range(edu.start_date, edu.end_date, edu.is_current)
            degree_text = edu.degree
            if edu.field_of_study:
                degree_text += f" in {edu.field_of_study}"

            html += f"""
        <div class="education-item">
            <div class="education-header">
                <span class="degree">{degree_text}</span>
                <span class="date">{date_range}</span>
            </div>
            <div class="institution">{edu.institution}{' · ' + edu.location if edu.location else ''}</div>
"""
            if edu.grade:
                html += f'<div class="description">GPA: {edu.grade}</div>'
            html += """
        </div>
"""
        html += "    </section>\n"

    # Skills
    if data['skills']:
        html += """
    <section class="section">
        <h2 class="section-title">Technical Skills</h2>
        <div class="skills-grid">
"""
        grouped = group_skills_by_category(data['skills'])
        for category, skills in grouped.items():
            html += f"""
            <div class="skill-category">
                <h4>{get_category_display_name(category)}</h4>
                <div class="skill-tags">
"""
            for skill in skills:
                html += f'                    <span class="skill-tag">{skill.name}</span>\n'
            html += """
                </div>
            </div>
"""
        html += """
        </div>
    </section>
"""

    # Featured Projects
    if data['featured_projects']:
        html += """
    <section class="section">
        <h2 class="section-title">Key Projects</h2>
        <div class="projects-grid">
"""
        for project in data['featured_projects'][:6]:  # Limit to 6 projects
            html += f"""
            <div class="project-item">
                <h4>{project.title}</h4>
                <p>{project.description[:200] + '...' if project.description and len(project.description) > 200 else project.description or ''}</p>
                <div class="project-links">
"""
            if project.technologies:
                html += f'<strong>Tech:</strong> {project.technologies}<br>'
            if project.github_url:
                html += f'<a href="{project.github_url}">GitHub</a>'
            if project.live_url:
                html += f'<a href="{project.live_url}">Live Demo</a>'
            html += """
                </div>
            </div>
"""
        html += """
        </div>
    </section>
"""

    # Social Links
    if data['social_links']:
        html += """
    <section class="section">
        <h2 class="section-title">Connect</h2>
        <div class="social-links">
"""
        for link in data['social_links']:
            html += f'            <a href="{link.url}">{link.platform.title()}</a>\n'
        html += """
        </div>
    </section>
"""

    # Footer
    html += f"""
    <footer class="footer">
        <p>Last Updated: {datetime.now().strftime('%B %d, %Y')} | Auto-generated from <a href="https://www.lusansapkota.com.np">lusansapkota.com.np</a></p>
    </footer>
</body>
</html>
"""

    return html


def save_resume_files(base_path):
    """Generate and save resume files to the specified path."""
    data = get_portfolio_data()

    results = {
        'txt': None,
        'html': None,
        'errors': []
    }

    try:
        # Generate TXT resume
        txt_content = generate_txt_resume(data)
        txt_path = os.path.join(base_path, 'Lusan_Sapkota_Resume.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        results['txt'] = txt_path
    except Exception as e:
        results['errors'].append(f"TXT generation error: {str(e)}")

    try:
        # Generate HTML resume
        html_content = generate_html_resume(data)
        html_path = os.path.join(base_path, 'Lusan_Sapkota_Resume.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        results['html'] = html_path
    except Exception as e:
        results['errors'].append(f"HTML generation error: {str(e)}")

    return results


def get_resume_preview(format='txt'):
    """Generate resume content for preview without saving."""
    data = get_portfolio_data()

    if format == 'html':
        return generate_html_resume(data)
    else:
        return generate_txt_resume(data)
