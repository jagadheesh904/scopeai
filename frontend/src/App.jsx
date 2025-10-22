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
import Chatbot from './components/chatbot/Chatbot';
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
  const [showChatbot, setShowChatbot] = useState(false);

  // Check authentication on component mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      testAuthentication(token);
    }
  }, []);

  const testAuthentication = async (token) => {
    try {
      const response = await axios.get('/projects/');
      setIsAuthenticated(true);
      setProjects(response.data);
    } catch (error) {
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
    setShowChatbot(false);
  };

  const handleProjectCreate = async (projectData) => {
    setIsLoading(true);
    try {
      const response = await axios.post('/projects/', projectData);
      setCurrentProject(response.data);
      setActiveTab('scoping-workbench');
      loadProjects();
    } catch (error) {
      console.error('Error creating project:', error);
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

  const toggleChatbot = () => {
    setShowChatbot(!showChatbot);
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
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
                <h1>ScopeAI - AI Powered Project Scoping</h1>
                <button 
                  onClick={toggleChatbot}
                  style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    color: 'white',
                    border: 'none',
                    padding: '12px 20px',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '600',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)',
                    transition: 'transform 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.transform = 'translateY(-2px)';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.transform = 'translateY(0)';
                  }}
                >
                  <span style={{ fontSize: '16px' }}>💬</span>
                  AI Assistant
                </button>
              </div>
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

      {/* Chatbot */}
      {showChatbot && (
        <Chatbot 
          currentProject={currentProject}
          onClose={() => setShowChatbot(false)}
        />
      )}

      {/* Floating Chatbot Button */}
      {!showChatbot && (
        <button
          onClick={toggleChatbot}
          style={{
            position: 'fixed',
            bottom: '30px',
            right: '30px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            border: 'none',
            borderRadius: '50%',
            width: '70px',
            height: '70px',
            cursor: 'pointer',
            boxShadow: '0 6px 20px rgba(0,0,0,0.15)',
            fontSize: '28px',
            zIndex: 999,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'all 0.3s ease'
          }}
          onMouseEnter={(e) => {
            e.target.style.transform = 'scale(1.1)';
            e.target.style.boxShadow = '0 8px 25px rgba(0,0,0,0.2)';
          }}
          onMouseLeave={(e) => {
            e.target.style.transform = 'scale(1)';
            e.target.style.boxShadow = '0 6px 20px rgba(0,0,0,0.15)';
          }}
        >
          💬
        </button>
      )}
    </div>
  );
}

export default App;
