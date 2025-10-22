import React, { useState } from 'react';

const ScopingWorkbench = ({ project, onGenerateScope, isLoading }) => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      // In a real application, you would upload the file to the backend
      console.log('File selected:', file.name);
    }
  };

  const handleGenerateScope = () => {
    onGenerateScope(project.id, {
      project_description: project.description,
      industry: project.industry,
      project_type: project.project_type,
      tech_stack: project.tech_stack,
      complexity: project.complexity,
      compliance_requirements: project.compliance_requirements
    });
  };

  const phases = [
    {
      name: 'Discover & Design',
      activities: [
        { name: 'Discovery', description: 'Initial project discovery and requirements gathering' },
        { name: 'Technical Design', description: 'System architecture and technical design' },
        { name: 'UI/UX Design', description: 'User interface and experience design' },
        { name: 'Planning', description: 'Project planning and resource allocation' }
      ]
    },
    {
      name: 'Development Spirits',
      activities: [
        { name: 'Frontend Development', description: 'Client-side application development' },
        { name: 'Backend Development', description: 'Server-side application development' },
        { name: 'API Development', description: 'RESTful API development and documentation' },
        { name: 'Database Design', description: 'Database schema design and implementation' }
      ]
    },
    {
      name: 'Testing & QA',
      activities: [
        { name: 'Unit Testing', description: 'Component-level testing' },
        { name: 'Integration Testing', description: 'System integration testing' },
        { name: 'User Acceptance Testing', description: 'End-user validation testing' },
        { name: 'Performance Testing', description: 'System performance and load testing' }
      ]
    },
    {
      name: 'Deployment',
      activities: [
        { name: 'Environment Setup', description: 'Production environment configuration' },
        { name: 'Deployment', description: 'Application deployment to production' },
        { name: 'Post-Launch Support', description: 'Initial production support' }
      ]
    },
    {
      name: 'Post-Launch Support',
      activities: [
        { name: 'Monitoring', description: 'System monitoring and maintenance' },
        { name: 'Bug Fixing', description: 'Issue resolution and bug fixes' },
        { name: 'Enhancements', description: 'Feature enhancements and improvements' }
      ]
    }
  ];

  return (
    <div className="scoping-workbench">
      <div className="workbench-header">
        <h2>PROJECT SCOPING WORKBENCH</h2>
        <button 
          onClick={handleGenerateScope}
          className="generate-btn"
          disabled={isLoading}
          style={{ width: 'auto', padding: '0.75rem 1.5rem', fontSize: '1rem' }}
        >
          {isLoading ? (
            <>
              <div className="spinner" style={{ 
                display: 'inline-block', 
                width: '16px', 
                height: '16px', 
                marginRight: '0.5rem',
                borderWidth: '2px'
              }}></div>
              Generating...
            </>
          ) : (
            'Generate Scope'
          )}
        </button>
      </div>

      <div className="form-group">
        <label>Optional Uploads</label>
        <div style={{ 
          border: '2px dashed #ddd', 
          padding: '2rem', 
          textAlign: 'center', 
          borderRadius: '8px',
          backgroundColor: '#fafafa',
          cursor: 'pointer'
        }}>
          <input
            type="file"
            onChange={handleFileUpload}
            style={{ display: 'none' }}
            id="file-upload"
            multiple
          />
          <label htmlFor="file-upload" style={{ cursor: 'pointer', display: 'block' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📎</div>
            {selectedFile ? (
              <div>
                <strong>Selected: {selectedFile.name}</strong>
                <div style={{ fontSize: '0.875rem', color: '#666', marginTop: '0.5rem' }}>
                  Click to change file
                </div>
              </div>
            ) : (
              <div>
                <strong>Click to upload RFP, SOW, or requirement documents</strong>
                <div style={{ fontSize: '0.875rem', color: '#666', marginTop: '0.5rem' }}>
                  Supports PDF, Word, Excel files
                </div>
              </div>
            )}
          </label>
        </div>
      </div>

      <div className="activity-plan" style={{ marginTop: '2rem' }}>
        <h3 style={{ 
          marginBottom: '1.5rem', 
          color: '#2c3e50',
          paddingBottom: '0.5rem',
          borderBottom: '2px solid #e1e5e9'
        }}>
          Activity Plan Template
        </h3>
        
        {phases.map((phase, phaseIndex) => (
          <div key={phaseIndex} className="phase-section">
            <h4 className="phase-title">{phase.name}</h4>
            <ul className="activity-list">
              {phase.activities.map((activity, activityIndex) => (
                <li key={activityIndex} className="activity-item">
                  <input type="checkbox" />
                  <div className="activity-details">
                    <div className="activity-name">{activity.name}</div>
                    <div className="activity-description">{activity.description}</div>
                  </div>
                  <div className="activity-effort">40h</div>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div style={{ 
        marginTop: '2rem', 
        padding: '1rem', 
        backgroundColor: '#e7f3ff', 
        borderRadius: '8px',
        border: '1px solid #b3d9ff'
      }}>
        <h4 style={{ color: '#0066cc', marginBottom: '0.5rem' }}>💡 Pro Tip</h4>
        <p style={{ fontSize: '0.875rem', color: '#0066cc', margin: 0 }}>
          Click "Generate Scope" to automatically create a customized activity plan based on your project requirements.
          The AI will analyze your project details and generate a tailored scope with accurate effort estimates.
        </p>
      </div>
    </div>
  );
};

export default ScopingWorkbench;
