import React from 'react';

const ScopePreview = ({ scope }) => {
  if (!scope) {
    return (
      <div className="scope-preview">
        <div className="preview-header">
          <h3>GENERATED SCOPE PREVIEW</h3>
        </div>
        <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
          Generate a scope to see the preview here
        </div>
      </div>
    );
  }

  // Handle both old and new data structures
  const activitiesData = scope.activities || {};
  const activities = activitiesData.activities || activitiesData || [];
  const timeline = scope.timeline || {};
  const resourcePlanData = scope.resource_plan || {};
  const resourcePlan = resourcePlanData.resources || resourcePlanData || [];

  // Group activities by phase
  const activitiesByPhase = Array.isArray(activities) ? activities.reduce((acc, activity) => {
    const phase = activity.phase || 'Other';
    if (!acc[phase]) {
      acc[phase] = [];
    }
    acc[phase].push(activity);
    return acc;
  }, {}) : {};

  return (
    <div className="scope-preview">
      <div className="preview-header">
        <h3>GENERATED SCOPE PREVIEW</h3>
      </div>

      <div className="preview-content">
        <div className="summary-view" style={{ marginBottom: '1.5rem' }}>
          <h4 style={{ marginBottom: '0.5rem', color: '#2c3e50' }}>Summary View</h4>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div style={{ background: '#f8f9fa', padding: '0.75rem', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.875rem', color: '#666' }}>Total Activities</div>
              <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>{Array.isArray(activities) ? activities.length : 0}</div>
            </div>
            <div style={{ background: '#f8f9fa', padding: '0.75rem', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.875rem', color: '#666' }}>Timeline</div>
              <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>{timeline.total_weeks || 'N/A'} weeks</div>
            </div>
          </div>
        </div>

        <div className="activity-plan-preview">
          <h4 style={{ marginBottom: '0.5rem', color: '#2c3e50' }}>Activity Plan</h4>
          <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
            {Object.entries(activitiesByPhase).map(([phase, phaseActivities]) => (
              <div key={phase} style={{ marginBottom: '1rem' }}>
                <div style={{ fontWeight: '600', color: '#667eea', marginBottom: '0.5rem' }}>
                  {phase}
                </div>
                {phaseActivities.map((activity, index) => (
                  <div key={index} style={{ 
                    padding: '0.5rem', 
                    background: '#f8f9fa', 
                    marginBottom: '0.25rem',
                    borderRadius: '4px',
                    fontSize: '0.875rem'
                  }}>
                    <div style={{ fontWeight: '500' }}>{activity.name}</div>
                    <div style={{ color: '#666', fontSize: '0.75rem' }}>
                      {activity.effort_hours}h • {activity.required_roles?.join(', ')}
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>

        <div className="resource-allocation" style={{ marginTop: '1rem' }}>
          <h4 style={{ marginBottom: '0.5rem', color: '#2c3e50' }}>Resource Allocation</h4>
          <div style={{ maxHeight: '150px', overflowY: 'auto' }}>
            {Array.isArray(resourcePlan) && resourcePlan.map((resource, index) => (
              <div key={index} style={{
                display: 'flex',
                justifyContent: 'space-between',
                padding: '0.5rem',
                background: '#f8f9fa',
                marginBottom: '0.25rem',
                borderRadius: '4px',
                fontSize: '0.875rem'
              }}>
                <span>{resource.role}</span>
                <span style={{ fontWeight: '500' }}>{resource.total_hours}h</span>
              </div>
            ))}
          </div>
        </div>

        {timeline.milestones && (
          <div className="timeline-preview" style={{ marginTop: '1rem' }}>
            <h4 style={{ marginBottom: '0.5rem', color: '#2c3e50' }}>Key Milestones</h4>
            <div style={{ maxHeight: '150px', overflowY: 'auto' }}>
              {timeline.milestones.map((milestone, index) => (
                <div key={index} style={{
                  padding: '0.5rem',
                  background: '#f8f9fa',
                  marginBottom: '0.25rem',
                  borderRadius: '4px',
                  fontSize: '0.875rem'
                }}>
                  <div style={{ fontWeight: '500' }}>{milestone.name}</div>
                  <div style={{ color: '#666', fontSize: '0.75rem' }}>
                    Week {milestone.week}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ScopePreview;
