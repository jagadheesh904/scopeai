from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
import json
import os
from datetime import datetime

from models.database import get_db, Project, User
from routers.auth import get_current_user
from services.architecture_diagram import create_advanced_architecture_diagram

router = APIRouter()

class ExportRequest(BaseModel):
    project_id: int
    format: str  # excel, pdf, json

@router.post("/pdf")
async def export_to_pdf(
    request: ExportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        project = db.query(Project).filter(
            Project.id == request.project_id, 
            Project.created_by == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch)
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.HexColor('#2c3e50')
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.HexColor('#34495e')
        )
        
        story = []
        
        # Title Page
        title = Paragraph(f"ScopeAI Project Scope: {project.name}", title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Project Overview
        overview_title = Paragraph("Project Overview", heading_style)
        story.append(overview_title)
        
        overview_data = [
            ['Field', 'Value'],
            ['Project Name', project.name],
            ['Description', project.description],
            ['Industry', project.industry],
            ['Project Type', project.project_type],
            ['Tech Stack', ', '.join(project.tech_stack)],
            ['Complexity', project.complexity],
            ['Duration', f"{project.duration_weeks} weeks"],
            ['Status', project.status],
            ['Created', project.created_at.strftime("%Y-%m-%d")],
            ['Created By', current_user.full_name or current_user.email]
        ]
        
        overview_table = Table(overview_data, colWidths=[2*inch, 4*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(overview_table)
        story.append(Spacer(1, 0.5*inch))
        
        # Architecture Diagram Section
        architecture_title = Paragraph("System Architecture", heading_style)
        story.append(architecture_title)
        
        # Add architecture description
        arch_desc = Paragraph(
            f"This diagram illustrates the high-level system architecture for the {project.name} project, "
            f"based on the selected technology stack ({', '.join(project.tech_stack[:3])}...) and project type ({project.project_type}).",
            styles['Normal']
        )
        story.append(arch_desc)
        story.append(Spacer(1, 0.2*inch))
        
        # Create and add advanced architecture diagram
        architecture_diagram = create_advanced_architecture_diagram(
            project.tech_stack, 
            project.project_type, 
            project.name
        )
        story.append(architecture_diagram)
        story.append(Spacer(1, 0.3*inch))
        
        # Tech Stack Details
        tech_title = Paragraph("Technology Stack Details", heading_style)
        story.append(tech_title)
        
        tech_categories = {
            'Frontend': [tech for tech in project.tech_stack if tech.lower() in 
                        ['react', 'angular', 'vue', 'javascript', 'typescript', 'html', 'css', 'sass', 'bootstrap']],
            'Backend': [tech for tech in project.tech_stack if tech.lower() in 
                       ['python', 'node.js', 'java', 'c#', 'go', 'ruby', 'php', 'django', 'flask', 'express', 'spring']],
            'Database': [tech for tech in project.tech_stack if tech.lower() in 
                       ['mongodb', 'postgresql', 'mysql', 'redis', 'sqlite', 'oracle', 'sql server']],
            'Infrastructure': [tech for tech in project.tech_stack if tech.lower() in 
                             ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'nginx', 'apache', 'terraform']],
            'Tools & Other': [tech for tech in project.tech_stack if tech.lower() not in 
                            ['react', 'angular', 'vue', 'javascript', 'typescript', 'html', 'css', 'sass', 'bootstrap',
                             'python', 'node.js', 'java', 'c#', 'go', 'ruby', 'php', 'django', 'flask', 'express', 'spring',
                             'mongodb', 'postgresql', 'mysql', 'redis', 'sqlite', 'oracle', 'sql server',
                             'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'nginx', 'apache', 'terraform']]
        }
        
        tech_data = [['Category', 'Technologies']]
        for category, techs in tech_categories.items():
            if techs:  # Only add categories that have technologies
                tech_data.append([category, ', '.join(techs)])
        
        if len(tech_data) > 1:  # If we have technologies beyond the header
            tech_table = Table(tech_data, colWidths=[1.5*inch, 4.5*inch])
            tech_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            story.append(tech_table)
        
        story.append(Spacer(1, 0.5*inch))
        
        # Add page break before detailed sections
        story.append(PageBreak())
        
        # Activities Section
        if project.activities:
            activities_title = Paragraph("Activity Plan", heading_style)
            story.append(activities_title)
            
            # Extract activities from the nested structure
            activities_data = project.activities
            if isinstance(activities_data, dict) and 'activities' in activities_data:
                activities_list = activities_data['activities']
            else:
                activities_list = activities_data if isinstance(activities_data, list) else []
            
            if activities_list:
                # Group activities by phase
                activities_by_phase = {}
                for activity in activities_list:
                    phase = activity.get('phase', 'Other')
                    if phase not in activities_by_phase:
                        activities_by_phase[phase] = []
                    activities_by_phase[phase].append(activity)
                
                for phase, phase_activities in activities_by_phase.items():
                    phase_title = Paragraph(phase, styles['Heading3'])
                    story.append(phase_title)
                    
                    phase_data = [['Activity', 'Description', 'Effort (Hours)', 'Roles']]
                    for activity in phase_activities:
                        phase_data.append([
                            activity.get('name', ''),
                            activity.get('description', ''),
                            str(activity.get('effort_hours', 0)),
                            ', '.join(activity.get('required_roles', []))
                        ])
                    
                    phase_table = Table(phase_data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 1.5*inch])
                    phase_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5D6D7E')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('FONTSIZE', (0, 1), (-1, -1), 9)
                    ]))
                    story.append(phase_table)
                    story.append(Spacer(1, 0.2*inch))
        
        # Cost Estimate Section
        if project.cost_estimate:
            cost_title = Paragraph("Cost Estimate", heading_style)
            story.append(cost_title)
            
            cost_data = project.cost_estimate
            breakdown = cost_data.get('breakdown', [])
            total_cost = cost_data.get('total_cost', 0)
            
            if breakdown:
                cost_table_data = [['Role', 'Hours', 'Rate ($/hr)', 'Total Cost ($)']]
                for item in breakdown:
                    cost_table_data.append([
                        item.get('role', ''),
                        str(item.get('hours', 0)),
                        str(item.get('rate', 0)),
                        f"${item.get('cost', 0):,}"
                    ])
                
                # Add total row
                cost_table_data.append(['', '', 'Total:', f"${total_cost:,}"])
                
                cost_table = Table(cost_table_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1.5*inch])
                cost_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#f8f9fa')),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#2ecc71')),
                    ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                ]))
                story.append(cost_table)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        filename = f"scopeai_{project.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")

@router.post("/excel")
async def export_to_excel(
    request: ExportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        project = db.query(Project).filter(
            Project.id == request.project_id, 
            Project.created_by == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Create Excel file in memory
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Project Overview Sheet
            overview_data = {
                'Field': ['Project Name', 'Description', 'Industry', 'Project Type', 'Tech Stack', 'Complexity', 'Duration (Weeks)', 'Status'],
                'Value': [project.name, project.description, project.industry, project.project_type, ', '.join(project.tech_stack), project.complexity, project.duration_weeks, project.status]
            }
            overview_df = pd.DataFrame(overview_data)
            overview_df.to_excel(writer, sheet_name='Project Overview', index=False)
            
            # Activities Sheet
            if project.activities:
                activities_data = []
                activities_list = project.activities.get('activities', []) if isinstance(project.activities, dict) else project.activities
                
                for activity in activities_list:
                    activities_data.append({
                        'Phase': activity.get('phase', ''),
                        'Activity': activity.get('name', ''),
                        'Description': activity.get('description', ''),
                        'Effort Hours': activity.get('effort_hours', 0),
                        'Dependencies': ', '.join(activity.get('dependencies', [])),
                        'Required Roles': ', '.join(activity.get('required_roles', []))
                    })
                activities_df = pd.DataFrame(activities_data)
                activities_df.to_excel(writer, sheet_name='Activities', index=False)
            
            # Resource Plan Sheet
            if project.resource_plan:
                resource_data = project.resource_plan.get('resources', []) if isinstance(project.resource_plan, dict) else project.resource_plan
                resource_df = pd.DataFrame(resource_data)
                resource_df.to_excel(writer, sheet_name='Resource Plan', index=False)
            
            # Cost Estimate Sheet
            if project.cost_estimate and 'breakdown' in project.cost_estimate:
                cost_df = pd.DataFrame(project.cost_estimate['breakdown'])
                cost_df.to_excel(writer, sheet_name='Cost Estimate', index=False)
        
        output.seek(0)
        
        # Return as downloadable file
        filename = f"scopeai_{project.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel export failed: {str(e)}")

@router.post("/json")
async def export_to_json(
    request: ExportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        project = db.query(Project).filter(
            Project.id == request.project_id, 
            Project.created_by == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Create comprehensive JSON export
        export_data = {
            "project": {
                "name": project.name,
                "description": project.description,
                "industry": project.industry,
                "project_type": project.project_type,
                "tech_stack": project.tech_stack,
                "complexity": project.complexity,
                "compliance_requirements": project.compliance_requirements,
                "duration_weeks": project.duration_weeks,
                "status": project.status
            },
            "scope": {
                "activities": project.activities,
                "timeline": project.timeline,
                "resource_plan": project.resource_plan,
                "cost_estimate": project.cost_estimate
            },
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "exported_by": current_user.email,
                "tool": "ScopeAI"
            }
        }
        
        json_str = json.dumps(export_data, indent=2, default=str)
        
        filename = f"scopeai_{project.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        
        return StreamingResponse(
            io.BytesIO(json_str.encode()),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSON export failed: {str(e)}")
