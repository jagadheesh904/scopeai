import React, { useState } from 'react';

const ProjectInputForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    industry: '',
    project_type: '',
    tech_stack: [],
    complexity: 'medium',
    compliance_requirements: [],
    duration_weeks: 12
  });

  const [currentTech, setCurrentTech] = useState('');
  const [currentCompliance, setCurrentCompliance] = useState('');

  const industries = [
    'Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing',
    'Education', 'Energy', 'Telecommunications', 'Transportation', 'Media'
  ];

  const projectTypes = [
    'Web Application', 'Mobile Application', 'Data Analytics', 'Machine Learning',
    'Platform Migration', 'System Integration', 'Cloud Transformation', 'Digital Transformation'
  ];

  const complexityLevels = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' }
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const addTechStack = () => {
    if (currentTech.trim() && !formData.tech_stack.includes(currentTech.trim())) {
      setFormData(prev => ({
        ...prev,
        tech_stack: [...prev.tech_stack, currentTech.trim()]
      }));
      setCurrentTech('');
    }
  };

  const removeTechStack = (tech) => {
    setFormData(prev => ({
      ...prev,
      tech_stack: prev.tech_stack.filter(t => t !== tech)
    }));
  };

  const addCompliance = () => {
    if (currentCompliance.trim() && !formData.compliance_requirements.includes(currentCompliance.trim())) {
      setFormData(prev => ({
        ...prev,
        compliance_requirements: [...prev.compliance_requirements, currentCompliance.trim()]
      }));
      setCurrentCompliance('');
    }
  };

  const removeCompliance = (req) => {
    setFormData(prev => ({
      ...prev,
      compliance_requirements: prev.compliance_requirements.filter(r => r !== req)
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleKeyPress = (e, callback) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      callback();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="project-form">
      <div className="form-group">
        <label>Client/Project Name</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => handleInputChange('name', e.target.value)}
          placeholder="Enter project name"
          required
        />
      </div>

      <div className="form-group">
        <label>Industry</label>
        <select
          value={formData.industry}
          onChange={(e) => handleInputChange('industry', e.target.value)}
          required
        >
          <option value="">Select Industry</option>
          {industries.map(industry => (
            <option key={industry} value={industry}>{industry}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Project Type</label>
        <select
          value={formData.project_type}
          onChange={(e) => handleInputChange('project_type', e.target.value)}
          required
        >
          <option value="">Select Project Type</option>
          {projectTypes.map(type => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Tech Stack</label>
        <div className="tech-stack-input">
          <input
            type="text"
            value={currentTech}
            onChange={(e) => setCurrentTech(e.target.value)}
            onKeyPress={(e) => handleKeyPress(e, addTechStack)}
            placeholder="Add technology (e.g., React, Python, AWS)"
          />
          <button type="button" onClick={addTechStack}>Add</button>
        </div>
        <div className="tech-tags">
          {formData.tech_stack.map(tech => (
            <span key={tech} className="tech-tag">
              {tech}
              <button type="button" onClick={() => removeTechStack(tech)}>×</button>
            </span>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label>Project Description</label>
        <textarea
          value={formData.description}
          onChange={(e) => handleInputChange('description', e.target.value)}
          placeholder="Describe the project requirements, goals, and scope..."
          required
        />
        <small style={{ color: '#666', fontSize: '0.875rem' }}>
          Leverages GenAI for intelligent scoping
        </small>
      </div>

      <div className="form-group">
        <label>Complexity Level</label>
        <div style={{ display: 'flex', gap: '1rem' }}>
          {complexityLevels.map(level => (
            <label key={level.value} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <input
                type="radio"
                value={level.value}
                checked={formData.complexity === level.value}
                onChange={(e) => handleInputChange('complexity', e.target.value)}
              />
              {level.label}
            </label>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label>Compliance Requirements</label>
        <div className="tech-stack-input">
          <input
            type="text"
            value={currentCompliance}
            onChange={(e) => setCurrentCompliance(e.target.value)}
            onKeyPress={(e) => handleKeyPress(e, addCompliance)}
            placeholder="Add compliance requirement (e.g., GDPR, HIPAA, SOC2)"
          />
          <button type="button" onClick={addCompliance}>Add</button>
        </div>
        <div className="tech-tags">
          {formData.compliance_requirements.map(req => (
            <span key={req} className="tech-tag">
              {req}
              <button type="button" onClick={() => removeCompliance(req)}>×</button>
            </span>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label>Estimated Duration (Weeks)</label>
        <input
          type="number"
          value={formData.duration_weeks}
          onChange={(e) => handleInputChange('duration_weeks', parseInt(e.target.value))}
          min="1"
          max="104"
        />
      </div>

      <button type="submit" className="generate-btn" disabled={isLoading}>
        {isLoading ? 'Generating Scope...' : 'GENERATE DRAFT SCOPE'}
      </button>
    </form>
  );
};

export default ProjectInputForm;
