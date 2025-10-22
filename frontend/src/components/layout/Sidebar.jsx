import React from 'react';

const Sidebar = ({ activeTab, setActiveTab, projects, currentProject, setCurrentProject }) => {
  const menuItems = [
    { id: 'scope-library', label: 'Scope Library', icon: '📚' },
    { id: 'activity-files', label: 'Activity Files', icon: '📁' },
    { id: 'integrations', label: 'Integrations', icon: '🔗' },
    { id: 'scoping-workbench', label: 'Project Scoping Workbench', icon: '⚙️' },
    { id: 'exports', label: 'Exports', icon: '📤' },
    { id: 'settings', label: 'Settings', icon: '⚙️' }
  ];

  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        {menuItems.map(item => (
          <li
            key={item.id}
            className={`sidebar-item ${activeTab === item.id ? 'active' : ''}`}
            onClick={() => setActiveTab(item.id)}
          >
            <span className="icon">{item.icon}</span>
            {item.label}
          </li>
        ))}
      </nav>

      {projects.length > 0 && (
        <div className="projects-list" style={{ marginTop: '2rem', padding: '0 1.5rem' }}>
          <h4 style={{ marginBottom: '1rem', color: '#666' }}>Recent Projects</h4>
          {projects.slice(0, 5).map(project => (
            <div
              key={project.id}
              className={`sidebar-item ${currentProject?.id === project.id ? 'active' : ''}`}
              onClick={() => {
                setCurrentProject(project);
                setActiveTab('scoping-workbench');
              }}
              style={{ fontSize: '0.9rem' }}
            >
              {project.name}
            </div>
          ))}
        </div>
      )}
    </aside>
  );
};

export default Sidebar;
