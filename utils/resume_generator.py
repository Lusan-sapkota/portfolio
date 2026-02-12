"""
Resume Generator Utility
Generates a professional resume from portfolio database data.
Produces both TXT and HTML formats.
"""

import re
from datetime import datetime
from models import PersonalInfo, SocialLink, Skill, Experience, Education, Project
from database import db
import os


def _fallback_summary():
    """Fallback professional summary when bio is not in the database."""
    return (
        "Full Stack Developer with 4+ years of hands-on experience building "
        "production systems across backend architecture, frontend development, "
        "and cross-platform mobile applications. Skilled in designing scalable "
        "REST APIs, database systems, and CI/CD pipelines. Co-founder of "
        "Icepeak Tech, delivering end-to-end software solutions. Experienced "
        "with AI/ML integrations and algorithmic systems."
    )


def _fallback_experiences():
    """Fallback experience data matching the frontend when DB is empty."""
    return [
        {
            'position': 'Co-founder & Lead Engineer',
            'company': 'Icepeak Tech',
            'location': '',
            'date_range': 'Dec 2025 - Present',
            'bullets': [
                'Founded a software development company delivering full-stack web apps, backend systems, and cross-platform mobile applications',
                'Architect end-to-end solutions from database design to deployment pipelines',
                'Handle client requirements, technical scoping, and project delivery',
                'Build and maintain production infrastructure on VPS with CI/CD automation',
            ],
            'technologies': 'System Design, Full Stack, DevOps, Client Delivery',
        },
        {
            'position': 'Development Team Lead',
            'company': 'AiGeeks',
            'location': 'Remote',
            'date_range': 'Jan 2026 - Present',
            'bullets': [
                'Lead a distributed team of developers across multiple client projects',
                'Own backend architecture decisions and enforce code quality through PR reviews',
                'Coordinate deployments and maintain staging/production environments',
            ],
            'technologies': 'TypeScript, React, Node.js, PostgreSQL',
        },
        {
            'position': 'Full Stack Developer',
            'company': 'AiGeeks',
            'location': 'Remote',
            'date_range': 'Oct 2025 - Dec 2025',
            'bullets': [
                'Built and shipped features across React frontends and Node.js backends',
                'Designed database schemas and wrote optimized PostgreSQL queries',
                'Integrated third-party APIs and handled authentication flows',
            ],
            'technologies': 'TypeScript, React, Node.js, PostgreSQL',
        },
        {
            'position': 'Software Engineer',
            'company': 'Covosys',
            'location': 'Kathmandu, Nepal',
            'date_range': 'Apr 2023 - Sep 2025',
            'bullets': [
                'Developed and maintained backend services using Django and Flask',
                'Built REST APIs serving production traffic with focus on reliability',
                'Worked with PostgreSQL for data modeling and query optimization',
                'Collaborated with senior engineers on system design and code reviews',
                'Grew from junior responsibilities to owning full feature implementations',
            ],
            'technologies': 'Python, Django, Flask, REST APIs, PostgreSQL',
        },
    ]


def _fallback_education():
    """Fallback education data matching the frontend when DB is empty."""
    return [
        {
            'degree': "Bachelor's in Information Technology",
            'institution': 'Texas International College',
            'location': 'Sifal, Kathmandu',
            'date_range': '2023 - 2027',
            'grade': '',
        },
        {
            'degree': 'Higher Secondary (+2) in Physical Science',
            'institution': 'Mansalu World College',
            'location': 'Chuchepati, Kathmandu',
            'date_range': '2021 - 2023',
            'grade': '3.48',
        },
        {
            'degree': 'Secondary Education (SEE)',
            'institution': 'Chandikaswori Secondary Boarding School',
            'location': 'Gokarneshowr-2, Kathmandu',
            'date_range': '2019 - 2021',
            'grade': '3.6',
        },
    ]


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

    sorted_grouped = {}
    for cat in category_order:
        if cat in grouped:
            sorted_grouped[cat] = grouped[cat]

    for cat in grouped:
        if cat not in sorted_grouped:
            sorted_grouped[cat] = grouped[cat]

    return sorted_grouped


def get_category_display_name(category):
    """Get display name for skill category."""
    names = {
        'programming': 'Languages',
        'frontend': 'Frontend',
        'backend': 'Backend',
        'database': 'Databases',
        'devops': 'DevOps & Cloud',
        'tools': 'Tools',
        'other': 'Other'
    }
    return names.get(category, category.title())


def extract_short_description(description):
    """Extract a clean, concise one-liner from a project description.

    Strips emojis, feature lists, and returns the first meaningful sentence
    that describes what the project is.
    """
    if not description:
        return ""

    # Remove emojis and special unicode characters
    text = re.sub(
        r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF'
        r'\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251'
        r'\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF'
        r'\U00002600-\U000026FF\U00002700-\U000027BF]+',
        '', description
    )

    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Take text up to the first "Features" / "Key Features" / "Core Features" marker
    for marker in ['Features', 'Key Features', 'Core Features', 'Core Philosophy',
                    'Tech Stack', 'Future', 'Roadmap', 'Built with']:
        idx = text.find(marker)
        if idx > 30:
            text = text[:idx].strip()
            break

    # Split into sentences and take first 1-2 that make sense
    sentences = re.split(r'(?<=[.!?])\s+', text)
    short = ""
    for s in sentences:
        s = s.strip().rstrip('.')
        if not s:
            continue
        candidate = (short + ". " + s) if short else s
        if len(candidate) > 180:
            break
        short = candidate

    if not short and text:
        short = text[:180].rsplit(' ', 1)[0]

    # Clean trailing punctuation artifacts
    short = short.strip().rstrip(',;:').strip()
    if short and not short.endswith('.'):
        short += '.'

    return short


def word_wrap(text, width=76, indent=""):
    """Wrap text to specified width with optional indent."""
    words = text.split()
    lines = []
    current = indent
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current += (" " if current.strip() else "") + word
        else:
            if current.strip():
                lines.append(current)
            current = indent + word
    if current.strip():
        lines.append(current)
    return lines


def generate_txt_resume(data):
    """Generate a professional TXT resume."""
    personal = data['personal']
    lines = []
    w = 78

    # Header
    lines.append("=" * w)
    name = personal.name.upper() if personal else "LUSAN SAPKOTA"
    title = personal.title if personal else "Full Stack Developer"
    lines.append(f"{name:^{w}}")
    lines.append(f"{title:^{w}}")

    # Contact line centered
    contact_parts = []
    if personal:
        if personal.email:
            contact_parts.append(personal.email)
        contact_parts.append("lusansapkota.com.np")
        if personal.location:
            contact_parts.append(personal.location)
        if personal.phone:
            contact_parts.append(personal.phone)
    contact_line = "  |  ".join(contact_parts)
    lines.append(f"{contact_line:^{w}}")
    lines.append("=" * w)
    lines.append("")

    # Key social links (GitHub and LinkedIn only for resume)
    github_url = ""
    linkedin_url = ""
    for link in data.get('social_links', []):
        if link.platform.lower() == 'github':
            github_url = link.url
        elif link.platform.lower() == 'linkedin':
            linkedin_url = link.url
    if github_url or linkedin_url:
        social_parts = []
        if github_url:
            social_parts.append(f"GitHub: {github_url}")
        if linkedin_url:
            social_parts.append(f"LinkedIn: {linkedin_url}")
        lines.append("  |  ".join(social_parts))
        lines.append("")

    # Professional Summary
    lines.append("PROFESSIONAL SUMMARY")
    lines.append("-" * w)
    if personal and personal.bio:
        bio = personal.bio.replace('\n', ' ').replace('\r', '').strip()
        if len(bio) > 300:
            bio = bio[:300].rsplit(' ', 1)[0].rstrip('.,;:') + '.'
        for line in word_wrap(bio, w):
            lines.append(line)
    else:
        for line in word_wrap(_fallback_summary(), w):
            lines.append(line)
    lines.append("")

    # Professional Experience
    db_experiences = data['experiences']
    if db_experiences:
        lines.append("PROFESSIONAL EXPERIENCE")
        lines.append("-" * w)
        for exp in db_experiences:
            date_range = format_date_range(exp.start_date, exp.end_date, exp.is_current)
            lines.append(f"{exp.position}")
            company_line = exp.company
            if exp.location:
                company_line += f", {exp.location}"
            if date_range:
                company_line += f"  |  {date_range}"
            lines.append(company_line)

            if exp.description:
                for desc_line in exp.description.split('\n'):
                    cleaned = desc_line.strip().lstrip('-*').strip()
                    if cleaned:
                        lines.append(f"  - {cleaned}")

            if exp.achievements:
                for ach_line in exp.achievements.split('\n'):
                    cleaned = ach_line.strip().lstrip('-*').strip()
                    if cleaned:
                        lines.append(f"  - {cleaned}")

            if exp.technologies:
                lines.append(f"  Technologies: {exp.technologies}")
            lines.append("")
    else:
        lines.append("PROFESSIONAL EXPERIENCE")
        lines.append("-" * w)
        for exp in _fallback_experiences():
            lines.append(exp['position'])
            company_line = exp['company']
            if exp['location']:
                company_line += f", {exp['location']}"
            company_line += f"  |  {exp['date_range']}"
            lines.append(company_line)
            for bullet in exp['bullets']:
                lines.append(f"  - {bullet}")
            if exp['technologies']:
                lines.append(f"  Technologies: {exp['technologies']}")
            lines.append("")

    # Education
    db_education = data['education']
    if db_education:
        lines.append("EDUCATION")
        lines.append("-" * w)
        for edu in db_education:
            degree_line = edu.degree
            if edu.field_of_study:
                degree_line += f" in {edu.field_of_study}"
            lines.append(degree_line)

            inst_line = edu.institution
            if edu.location:
                inst_line += f", {edu.location}"
            date_range = format_date_range(edu.start_date, edu.end_date, edu.is_current)
            if date_range:
                inst_line += f"  |  {date_range}"
            lines.append(inst_line)

            if edu.grade:
                lines.append(f"  GPA/Grade: {edu.grade}")
            lines.append("")
    else:
        lines.append("EDUCATION")
        lines.append("-" * w)
        for edu in _fallback_education():
            lines.append(edu['degree'])
            inst_line = f"{edu['institution']}, {edu['location']}  |  {edu['date_range']}"
            lines.append(inst_line)
            if edu['grade']:
                lines.append(f"  GPA: {edu['grade']}")
            lines.append("")

    # Technical Skills (compact format)
    if data['skills']:
        lines.append("TECHNICAL SKILLS")
        lines.append("-" * w)
        grouped = group_skills_by_category(data['skills'])
        for category, skills in grouped.items():
            skill_names = [s.name for s in skills]
            label = get_category_display_name(category)
            skill_line = f"{label}: {', '.join(skill_names)}"
            for wrapped in word_wrap(skill_line, w):
                lines.append(wrapped)
        lines.append("")

    # Key Projects (short descriptions only)
    if data['featured_projects']:
        lines.append("KEY PROJECTS")
        lines.append("-" * w)
        for project in data['featured_projects'][:8]:
            short_desc = extract_short_description(project.description)

            header = project.title
            if project.technologies:
                header += f"  [{project.technologies}]"
            lines.append(header)

            if short_desc:
                for wrapped in word_wrap(short_desc, w, "  "):
                    lines.append(wrapped)

            link_parts = []
            if project.github_url:
                link_parts.append(project.github_url)
            if project.live_url:
                link_parts.append(project.live_url)
            if link_parts:
                lines.append(f"  {' | '.join(link_parts)}")
            lines.append("")

    # Languages
    lines.append("LANGUAGES")
    lines.append("-" * w)
    lines.append("English (Fluent)  |  Nepali (Native)  |  Hindi (Conversational)")
    lines.append("")

    # Footer
    lines.append("=" * w)
    lines.append(f"Portfolio: https://www.lusansapkota.com.np  |  Last Updated: {datetime.now().strftime('%B %Y')}")
    lines.append("=" * w)

    return "\n".join(lines)


def generate_html_resume(data):
    """Generate a professional HTML resume for printing/PDF conversion."""
    personal = data['personal']

    # Extract key social links
    github_url = ""
    linkedin_url = ""
    for link in data.get('social_links', []):
        if link.platform.lower() == 'github':
            github_url = link.url
        elif link.platform.lower() == 'linkedin':
            linkedin_url = link.url

    name = personal.name if personal else 'Lusan Sapkota'
    title = personal.title if personal else 'Full Stack Developer'
    email = personal.email if personal and personal.email else 'sapkotalusan@gmail.com'
    location = personal.location if personal and personal.location else 'Kathmandu, Nepal'
    phone = personal.phone if personal and personal.phone else ''

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Resume</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.5;
            color: #222;
            max-width: 800px;
            margin: 0 auto;
            padding: 30px 40px;
            background: #fff;
            font-size: 10.5pt;
        }}

        @media print {{
            body {{
                padding: 15px 20px;
                font-size: 10pt;
            }}
            .section {{
                page-break-inside: avoid;
            }}
        }}

        .header {{
            text-align: center;
            padding-bottom: 12px;
            margin-bottom: 16px;
            border-bottom: 2px solid #333;
        }}

        .header h1 {{
            font-size: 22pt;
            color: #111;
            margin-bottom: 2px;
            letter-spacing: 3px;
            font-weight: 700;
        }}

        .header .title {{
            font-size: 11pt;
            color: #555;
            font-weight: 400;
            font-style: italic;
            margin-bottom: 8px;
        }}

        .contact-bar {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 6px 18px;
            font-size: 9pt;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}

        .contact-bar a {{
            color: #1a5276;
            text-decoration: none;
        }}

        .contact-bar span {{
            color: #444;
        }}

        .contact-bar .sep {{
            color: #aaa;
        }}

        .section {{
            margin-bottom: 16px;
        }}

        .section-title {{
            font-size: 11pt;
            color: #111;
            border-bottom: 1px solid #999;
            padding-bottom: 3px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
        }}

        .summary {{
            color: #333;
            font-size: 10pt;
            text-align: justify;
        }}

        .experience-item, .education-item {{
            margin-bottom: 14px;
        }}

        .experience-header, .education-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 2px;
        }}

        .position, .degree {{
            font-weight: 700;
            color: #111;
            font-size: 10.5pt;
        }}

        .date {{
            color: #555;
            font-size: 9.5pt;
            font-style: italic;
        }}

        .company, .institution {{
            color: #333;
            font-size: 10pt;
            font-style: italic;
            margin-bottom: 4px;
        }}

        .description {{
            color: #333;
            font-size: 9.5pt;
        }}

        .description ul {{
            margin-left: 18px;
            margin-top: 3px;
        }}

        .description li {{
            margin-bottom: 2px;
        }}

        .technologies {{
            margin-top: 4px;
            font-size: 9pt;
            color: #555;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}

        .skills-table {{
            width: 100%;
            font-size: 9.5pt;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}

        .skills-table td {{
            padding: 3px 0;
            vertical-align: top;
        }}

        .skills-table .skill-label {{
            font-weight: 700;
            color: #111;
            width: 130px;
            white-space: nowrap;
            padding-right: 10px;
        }}

        .skills-table .skill-list {{
            color: #333;
        }}

        .projects-list {{
            font-size: 9.5pt;
        }}

        .project-entry {{
            margin-bottom: 10px;
        }}

        .project-entry .project-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }}

        .project-entry h4 {{
            color: #111;
            font-size: 10pt;
            font-weight: 700;
            margin-bottom: 1px;
        }}

        .project-entry .project-tech {{
            font-size: 8.5pt;
            color: #666;
            font-style: italic;
        }}

        .project-entry p {{
            font-size: 9.5pt;
            color: #333;
            margin-bottom: 2px;
        }}

        .project-entry .project-links {{
            font-size: 8.5pt;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}

        .project-entry .project-links a {{
            color: #1a5276;
            text-decoration: none;
            margin-right: 12px;
        }}

        .languages {{
            font-size: 10pt;
            color: #333;
        }}

        .footer {{
            margin-top: 20px;
            padding-top: 8px;
            border-top: 1px solid #ccc;
            text-align: center;
            font-size: 8pt;
            color: #999;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}

        @media (max-width: 600px) {{
            .experience-header, .education-header, .project-entry .project-header {{
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
        <h1>{name.upper()}</h1>
        <div class="title">{title}</div>
        <div class="contact-bar">
            <span>{email}</span>
            <span class="sep">|</span>
            <span><a href="https://www.lusansapkota.com.np">lusansapkota.com.np</a></span>
            <span class="sep">|</span>
            <span>{location}</span>"""

    if phone:
        html += f"""
            <span class="sep">|</span>
            <span>{phone}</span>"""

    if github_url or linkedin_url:
        if github_url:
            html += f"""
            <span class="sep">|</span>
            <span><a href="{github_url}">GitHub</a></span>"""
        if linkedin_url:
            html += f"""
            <span class="sep">|</span>
            <span><a href="{linkedin_url}">LinkedIn</a></span>"""

    html += """
        </div>
    </header>
"""

    # Professional Summary
    bio = ''
    if personal and personal.bio:
        bio = personal.bio.replace('\n', ' ').replace('\r', '').strip()
        if len(bio) > 400:
            bio = bio[:400].rsplit(' ', 1)[0].rstrip('.,;:') + '.'
    else:
        bio = _fallback_summary()

    html += f"""
    <section class="section">
        <h2 class="section-title">Professional Summary</h2>
        <p class="summary">{bio}</p>
    </section>
"""

    # Professional Experience
    db_experiences = data['experiences']
    html += """
    <section class="section">
        <h2 class="section-title">Professional Experience</h2>
"""
    if db_experiences:
        for exp in db_experiences:
            date_range = format_date_range(exp.start_date, exp.end_date, exp.is_current)
            html += f"""
        <div class="experience-item">
            <div class="experience-header">
                <span class="position">{exp.position}</span>
                <span class="date">{date_range}</span>
            </div>
            <div class="company">{exp.company}{', ' + exp.location if exp.location else ''}</div>
            <div class="description">
"""
            if exp.description:
                html += "                <ul>\n"
                for line in exp.description.split('\n'):
                    cleaned = line.strip().lstrip('-*').strip()
                    if cleaned:
                        html += f"                    <li>{cleaned}</li>\n"
                html += "                </ul>\n"

            if exp.achievements:
                html += "                <ul>\n"
                for line in exp.achievements.split('\n'):
                    cleaned = line.strip().lstrip('-*').strip()
                    if cleaned:
                        html += f"                    <li>{cleaned}</li>\n"
                html += "                </ul>\n"

            if exp.technologies:
                html += f'                <div class="technologies"><strong>Technologies:</strong> {exp.technologies}</div>\n'

            html += """            </div>
        </div>
"""
    else:
        for exp in _fallback_experiences():
            html += f"""
        <div class="experience-item">
            <div class="experience-header">
                <span class="position">{exp['position']}</span>
                <span class="date">{exp['date_range']}</span>
            </div>
            <div class="company">{exp['company']}{', ' + exp['location'] if exp['location'] else ''}</div>
            <div class="description">
                <ul>
"""
            for bullet in exp['bullets']:
                html += f"                    <li>{bullet}</li>\n"
            html += "                </ul>\n"
            if exp['technologies']:
                html += f'                <div class="technologies"><strong>Technologies:</strong> {exp["technologies"]}</div>\n'
            html += """            </div>
        </div>
"""
    html += "    </section>\n"

    # Education
    db_education = data['education']
    html += """
    <section class="section">
        <h2 class="section-title">Education</h2>
"""
    if db_education:
        for edu in db_education:
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
            <div class="institution">{edu.institution}{', ' + edu.location if edu.location else ''}</div>
"""
            if edu.grade:
                html += f'            <div class="description">GPA: {edu.grade}</div>\n'
            html += "        </div>\n"
    else:
        for edu in _fallback_education():
            html += f"""
        <div class="education-item">
            <div class="education-header">
                <span class="degree">{edu['degree']}</span>
                <span class="date">{edu['date_range']}</span>
            </div>
            <div class="institution">{edu['institution']}, {edu['location']}</div>
"""
            if edu['grade']:
                html += f'            <div class="description">GPA: {edu["grade"]}</div>\n'
            html += "        </div>\n"
    html += "    </section>\n"

    # Technical Skills (compact table format)
    if data['skills']:
        html += """
    <section class="section">
        <h2 class="section-title">Technical Skills</h2>
        <table class="skills-table">
"""
        grouped = group_skills_by_category(data['skills'])
        for category, skills in grouped.items():
            skill_names = ', '.join(s.name for s in skills)
            html += f"""            <tr>
                <td class="skill-label">{get_category_display_name(category)}</td>
                <td class="skill-list">{skill_names}</td>
            </tr>
"""
        html += """        </table>
    </section>
"""

    # Key Projects (short descriptions)
    if data['featured_projects']:
        html += """
    <section class="section">
        <h2 class="section-title">Key Projects</h2>
        <div class="projects-list">
"""
        for project in data['featured_projects'][:8]:
            short_desc = extract_short_description(project.description)

            html += f"""
            <div class="project-entry">
                <div class="project-header">
                    <h4>{project.title}</h4>
                    <span class="project-tech">{project.technologies or ''}</span>
                </div>
"""
            if short_desc:
                html += f"                <p>{short_desc}</p>\n"

            links = []
            if project.github_url:
                links.append(f'<a href="{project.github_url}">GitHub</a>')
            if project.live_url:
                links.append(f'<a href="{project.live_url}">Live</a>')
            if links:
                html += f'                <div class="project-links">{"  |  ".join(links)}</div>\n'

            html += "            </div>\n"
        html += """
        </div>
    </section>
"""

    # Languages
    html += """
    <section class="section">
        <h2 class="section-title">Languages</h2>
        <p class="languages">English (Fluent)  |  Nepali (Native)  |  Hindi (Conversational)</p>
    </section>
"""

    # Footer
    html += f"""
    <footer class="footer">
        <p>Portfolio: <a href="https://www.lusansapkota.com.np">lusansapkota.com.np</a>  |  Last Updated: {datetime.now().strftime('%B %Y')}</p>
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
        txt_content = generate_txt_resume(data)
        txt_path = os.path.join(base_path, 'Lusan_Sapkota_Resume.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        results['txt'] = txt_path
    except Exception as e:
        results['errors'].append(f"TXT generation error: {str(e)}")

    try:
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
