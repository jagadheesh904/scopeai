from reportlab.graphics.shapes import Drawing, Rect, Line, String
from reportlab.graphics import renderPDF
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Flowable
from typing import List

class AdvancedArchitectureDiagram(Flowable):
    def __init__(self, width, height, tech_stack: List[str], project_type: str, project_name: str):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.tech_stack = [tech.lower() for tech in tech_stack]
        self.project_type = project_type
        self.project_name = project_name

    def categorize_technologies(self):
        """Categorize technologies into architecture components"""
        categories = {
            'frontend': [],
            'backend': [],
            'database': [],
            'infrastructure': [],
            'tools': []
        }
        
        # Define technology mappings
        frontend_techs = ['react', 'angular', 'vue', 'javascript', 'typescript', 'html', 'css', 'sass', 'bootstrap', 'tailwind']
        backend_techs = ['python', 'node.js', 'java', 'c#', 'go', 'ruby', 'php', 'django', 'flask', 'express', 'spring', 'fastapi']
        database_techs = ['mongodb', 'postgresql', 'mysql', 'redis', 'sqlite', 'oracle', 'sql server', 'dynamodb']
        infrastructure_techs = ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'nginx', 'apache', 'terraform', 'jenkins']
        
        for tech in self.tech_stack:
            tech_lower = tech.lower()
            if any(ft in tech_lower for ft in frontend_techs):
                categories['frontend'].append(tech)
            elif any(bt in tech_lower for bt in backend_techs):
                categories['backend'].append(tech)
            elif any(dt in tech_lower for dt in database_techs):
                categories['database'].append(tech)
            elif any(it in tech_lower for it in infrastructure_techs):
                categories['infrastructure'].append(tech)
            else:
                categories['tools'].append(tech)
        
        # Set defaults if no technologies found
        if not categories['frontend']:
            categories['frontend'] = ['React'] if 'web' in self.project_type.lower() else ['Mobile UI']
        if not categories['backend']:
            categories['backend'] = ['Node.js']
        if not categories['database']:
            categories['database'] = ['MongoDB']
        if not categories['infrastructure']:
            categories['infrastructure'] = ['AWS']
            
        return categories

    def draw(self):
        d = Drawing(self.width, self.height)
        
        # Color scheme
        colors_scheme = {
            'frontend': colors.HexColor('#4CAF50'),      # Green
            'backend': colors.HexColor('#2196F3'),       # Blue
            'database': colors.HexColor('#FF9800'),      # Orange
            'infrastructure': colors.HexColor('#607D8B'), # Blue Grey
            'external': colors.HexColor('#9C27B0'),      # Purple
            'user': colors.HexColor('#795548')           # Brown
        }
        
        categories = self.categorize_technologies()
        
        # Title
        d.add(String(self.width/2, self.height-0.3*inch, 
                    f"Architecture Diagram - {self.project_name}", 
                    fontSize=12, fillColor=colors.black, textAnchor='middle'))
        
        # Draw components with better layout
        components = [
            # (x, y, width, height, type, label, technologies)
            (1*inch, 4.5*inch, 1.2*inch, 0.8*inch, 'user', 'User/Browser', ['Client']),
            (3*inch, 4.5*inch, 1.5*inch, 0.8*inch, 'frontend', 'Frontend', categories['frontend'][:2]),
            (5*inch, 4.5*inch, 1.5*inch, 0.8*inch, 'backend', 'Backend API', categories['backend'][:2]),
            (3*inch, 2.5*inch, 1.5*inch, 0.8*inch, 'infrastructure', 'Infrastructure', categories['infrastructure'][:2]),
            (5*inch, 2.5*inch, 1.5*inch, 0.8*inch, 'database', 'Database', categories['database'][:2]),
            (7*inch, 3.5*inch, 1.5*inch, 0.8*inch, 'external', 'External APIs', ['Third Party'])
        ]
        
        # Draw components
        for x, y, w, h, comp_type, label, techs in components:
            # Main box
            d.add(Rect(x, y, w, h, 
                      fillColor=colors_scheme[comp_type], 
                      strokeColor=colors.black,
                      strokeWidth=1))
            
            # Label
            d.add(String(x + w/2, y + h - 0.2*inch, label, 
                       fontSize=9, fillColor=colors.white, textAnchor='middle'))
            
            # Technologies (truncate if too many)
            tech_text = '\n'.join(techs)
            d.add(String(x + w/2, y + h/2 - 0.1*inch, tech_text,
                       fontSize=8, fillColor=colors.white, textAnchor='middle'))
        
        # Draw connections
        connections = [
            # (start_x, start_y, end_x, end_y)
            (2.2*inch, 4.9*inch, 3*inch, 4.9*inch),  # User -> Frontend
            (4.5*inch, 4.9*inch, 5*inch, 4.9*inch),  # Frontend -> Backend
            (5.75*inch, 4.5*inch, 5.75*inch, 3.3*inch),  # Backend -> Database (vertical)
            (5*inch, 4.1*inch, 4.5*inch, 4.1*inch),  # Backend -> Infrastructure (horizontal part 1)
            (4.5*inch, 4.1*inch, 4.5*inch, 3.3*inch),  # Backend -> Infrastructure (vertical part 2)
            (6.5*inch, 4.9*inch, 7*inch, 4.9*inch),  # Backend -> External APIs
        ]
        
        for start_x, start_y, end_x, end_y in connections:
            d.add(Line(start_x, start_y, end_x, end_y, 
                      strokeColor=colors.black,
                      strokeWidth=1.5))
            
            # Add arrowhead for direction
            if end_x > start_x:  # Horizontal right
                d.add(Line(end_x-0.1*inch, end_y-0.05*inch, end_x, end_y, strokeColor=colors.black, strokeWidth=1.5))
                d.add(Line(end_x-0.1*inch, end_y+0.05*inch, end_x, end_y, strokeColor=colors.black, strokeWidth=1.5))
            elif end_x < start_x:  # Horizontal left
                d.add(Line(end_x+0.1*inch, end_y-0.05*inch, end_x, end_y, strokeColor=colors.black, strokeWidth=1.5))
                d.add(Line(end_x+0.1*inch, end_y+0.05*inch, end_x, end_y, strokeColor=colors.black, strokeWidth=1.5))
            elif end_y < start_y:  # Vertical down
                d.add(Line(end_x-0.05*inch, end_y+0.1*inch, end_x, end_y, strokeColor=colors.black, strokeWidth=1.5))
                d.add(Line(end_x+0.05*inch, end_y+0.1*inch, end_x, end_y, strokeColor=colors.black, strokeWidth=1.5))
        
        # Legend
        legend_y = 1.2*inch
        legend_x = 1*inch
        for i, (comp_type, color) in enumerate(colors_scheme.items()):
            d.add(Rect(legend_x + (i % 3) * 2.5*inch, 
                      legend_y - (i // 3) * 0.3*inch, 
                      0.2*inch, 0.15*inch, 
                      fillColor=color, strokeColor=colors.black))
            d.add(String(legend_x + (i % 3) * 2.5*inch + 0.25*inch, 
                        legend_y - (i // 3) * 0.3*inch + 0.05*inch, 
                        comp_type.title(), 
                        fontSize=7, fillColor=colors.black))
        
        renderPDF.draw(d, self.canv, 0, 0)

def create_advanced_architecture_diagram(tech_stack, project_type, project_name):
    """Create an advanced architecture diagram"""
    return AdvancedArchitectureDiagram(8*inch, 6*inch, tech_stack, project_type, project_name)
