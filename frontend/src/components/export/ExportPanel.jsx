import React from 'react';

const ExportPanel = ({ project, onExport }) => {
  const exportOptions = [
    {
      id: 'excel',
      name: 'Excel Export',
      description: 'Export to Microsoft Excel format with multiple sheets',
      icon: '📊',
      formats: ['xlsx']
    },
    {
      id: 'pdf',
      name: 'PDF Report',
      description: 'Generate a professional PDF report',
      icon: '📄',
      formats: ['pdf']
    },
    {
      id: 'json',
      name: 'JSON Data',
      description: 'Export raw data in JSON format for integration',
      icon: '🔗',
      formats: ['json']
    },
    {
      id: 'project',
      name: 'MS Project',
      description: 'Export to Microsoft Project format',
      icon: '📅',
      formats: ['mpp', 'xml']
    },
    {
      id: 'jira',
      name: 'Jira Import',
      description: 'Export for Jira project import',
      icon: '🎯',
      formats: ['csv', 'json']
    },
    {
      id: 'devops',
      name: 'Azure DevOps',
      description: 'Export for Azure DevOps integration',
      icon: '⚡',
      formats: ['json']
    }
  ];

  const handleExport = (format) => {
    onExport(format);
  };

  return (
    <div className="export-panel">
      <div className="preview-header">
        <h2>Export Options</h2>
      </div>
      
      <p style={{ color: '#666', marginBottom: '2rem' }}>
        Export your project scope in various formats for different use cases.
      </p>

      <div className="export-options">
        {exportOptions.map(option => (
          <div
            key={option.id}
            className="export-option"
            onClick={() => handleExport(option.id)}
          >
            <div className="icon">{option.icon}</div>
            <h4>{option.name}</h4>
            <p style={{ fontSize: '0.875rem', color: '#666', margin: '0.5rem 0' }}>
              {option.description}
            </p>
            <div style={{ fontSize: '0.75rem', color: '#667eea' }}>
              Formats: {option.formats.join(', ')}
            </div>
          </div>
        ))}
      </div>

      {project && (
        <div style={{ marginTop: '2rem', padding: '1rem', background: '#f8f9fa', borderRadius: '8px' }}>
          <h4 style={{ marginBottom: '0.5rem' }}>Current Project</h4>
          <p><strong>Name:</strong> {project.name}</p>
          <p><strong>Industry:</strong> {project.industry}</p>
          <p><strong>Type:</strong> {project.project_type}</p>
          <p><strong>Status:</strong> {project.status}</p>
        </div>
      )}
    </div>
  );
};

export default ExportPanel;
