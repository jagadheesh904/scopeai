import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './components/layout/Header';
import Sidebar from './components/layout/Sidebar';
import ProjectInputForm from './components/forms/ProjectInputForm';
import ScopingWorkbench from './components/scoping/ScopingWorkbench';
import ScopePreview from './components/scoping/ScopePreview';
import CostEstimate from './components/scoping/CostEstimate';
import ExportPanel from './components/export/ExportPanel';
import LoginForm from './components/forms/LoginForm';
import './App.css';

// Configure axios base URL - use 127.0.0.1 instead of localhost
axios.defaults.baseURL = 'http://127.0.0.1:8000/api';

// Add request interceptor to include auth token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle auth errors
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

function App() {
  const [currentProject, setCurrentProject] = useState(null);
  const [projects, setProjects] = useState([]);
  const [activeTab, setActiveTab] = useState('scope-library');
  const [generatedScope, setGeneratedScope] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  // Check authentication on component mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Verify token is valid by making a test request
      testAuthentication(token);
    }
  }, []);

  const testAuthentication = async (token) => {
    try {
      // Try to get projects to verify token is valid
      const response = await axios.get('/projects/');
      setIsAuthenticated(true);
      setProjects(response.data);
    } catch (error) {
      // Token is invalid, clear it
      localStorage.removeItem('token');
      setIsAuthenticated(false);
    }
  };

  const loadProjects = async () => {
    try {
      const response = await axios.get('/projects/');
      setProjects(response.data);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  const handleLogin = (token, userData) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
    setUser(userData);
    loadProjects();
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUser(null);
    setProjects([]);
    setCurrentProject(null);
  };

  const handleProjectCreate = async (projectData) => {
    setIsLoading(true);
    try {
      console.log('Creating project with data:', projectData);
      
      const response = await axios.post('/projects/', projectData);
      console.log('Project created:', response.data);
      
      setCurrentProject(response.data);
      setActiveTab('scoping-workbench');
      loadProjects();
    } catch (error) {
      console.error('Error creating project:', error);
      console.error('Error response:', error.response);
      
      let errorMessage = 'Unknown error occurred';
      if (error.response) {
        errorMessage = error.response.data?.detail || `Server error: ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'No response from server. Please check if backend is running.';
      } else {
        errorMessage = error.message;
      }
      
      alert(`Error creating project: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateScope = async (projectId, scopeData) => {
    setIsLoading(true);
    try {
      const response = await axios.post('/scoping/generate-draft', {
        project_id: projectId,
        ...scopeData
      });
      
      setGeneratedScope(response.data.scope);
      
      // Update current project with generated scope
      const updatedProject = await axios.get(`/projects/${projectId}`);
      setCurrentProject(updatedProject.data);
      
    } catch (error) {
      console.error('Error generating scope:', error);
      alert('Error generating scope: ' + (error.response?.data?.detail || 'Unknown error'));
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = async (format) => {
    if (!currentProject) return;
    
    try {
      const response = await axios.post(`/exports/${format}`, {
        project_id: currentProject.id,
        format: format
      }, {
        responseType: 'blob'
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `scopeai_${currentProject.name}_${new Date().toISOString().split('T')[0]}.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting:', error);
      alert('Error exporting project: ' + (error.response?.data?.detail || 'Unknown error'));
    }
  };

  if (!isAuthenticated) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <Header user={user} onLogout={handleLogout} />
      <div className="app-body">
        <Sidebar 
          activeTab={activeTab} 
          setActiveTab={setActiveTab}
          projects={projects}
          currentProject={currentProject}
          setCurrentProject={setCurrentProject}
        />
        
        <main className="main-content">
          {activeTab === 'scope-library' && (
            <div className="scope-library">
              <h1>ScopeAI - AI Powered Project Scoping</h1>
              <ProjectInputForm 
                onSubmit={handleProjectCreate}
                isLoading={isLoading}
              />
            </div>
          )}

          {activeTab === 'scoping-workbench' && currentProject && (
            <div className="scoping-workbench-container">
              <ScopingWorkbench 
                project={currentProject}
                onGenerateScope={handleGenerateScope}
                isLoading={isLoading}
              />
              
              <div className="preview-section">
                <ScopePreview scope={generatedScope || currentProject} />
                <CostEstimate costData={generatedScope?.cost_estimate || currentProject?.cost_estimate} />
              </div>
            </div>
          )}

          {activeTab === 'exports' && currentProject && (
            <ExportPanel 
              project={currentProject}
              onExport={handleExport}
            />
          )}

          {activeTab === 'scoping-workbench' && !currentProject && (
            <div className="empty-state">
              <h2>No Project Selected</h2>
              <p>Please select a project from the sidebar or create a new one from the Scope Library.</p>
            </div>
          )}

          {activeTab === 'activity-files' && (
            <div className="empty-state">
              <h2>Activity Files</h2>
              <p>This feature is coming soon. You'll be able to manage activity templates and historical data here.</p>
            </div>
          )}

          {activeTab === 'integrations' && (
            <div className="empty-state">
              <h2>Integrations</h2>
              <p>This feature is coming soon. Integrate with Jira, Azure DevOps, and other project management tools.</p>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="empty-state">
              <h2>Settings</h2>
              <p>This feature is coming soon. Configure billing rates, user preferences, and system settings.</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
