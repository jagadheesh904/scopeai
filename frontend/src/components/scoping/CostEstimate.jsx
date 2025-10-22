import React from 'react';

const CostEstimate = ({ costData }) => {
  if (!costData) {
    return (
      <div className="cost-estimate">
        <div className="preview-header">
          <h3>Cost Estimate</h3>
        </div>
        <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
          Generate a scope to see cost estimates
        </div>
      </div>
    );
  }

  // Handle both direct breakdown and nested structure
  const breakdown = costData.breakdown || [];
  const totalCost = costData.total_cost || 0;

  // If breakdown is empty but we have total cost, show at least the total
  const hasBreakdown = breakdown && breakdown.length > 0;

  return (
    <div className="cost-estimate">
      <div className="preview-header">
        <h3>Cost Estimate</h3>
      </div>

      {hasBreakdown ? (
        <table className="cost-table">
          <thead>
            <tr>
              <th>Role</th>
              <th>Effort</th>
              <th>Hours</th>
              <th>Rate</th>
              <th>Total Cost ($)</th>
            </tr>
          </thead>
          <tbody>
            {breakdown.map((item, index) => (
              <tr key={index}>
                <td>{item.role}</td>
                <td>{(item.hours / 40).toFixed(1)} weeks</td>
                <td>{item.hours}</td>
                <td>${item.rate}/hr</td>
                <td>${item.cost ? item.cost.toLocaleString() : '0'}</td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr className="total-cost">
              <td colSpan="4" style={{ textAlign: 'right', fontWeight: '600' }}>
                Cost of Transformation:
              </td>
              <td style={{ fontWeight: '600' }}>
                ${totalCost.toLocaleString()}
              </td>
            </tr>
            <tr className="total-cost">
              <td colSpan="4" style={{ textAlign: 'right', fontWeight: '600' }}>
                GRAND TOTAL PROJECT COST:
              </td>
              <td style={{ fontWeight: '600', fontSize: '1.1rem', color: '#667eea' }}>
                ${totalCost.toLocaleString()}
              </td>
            </tr>
          </tfoot>
        </table>
      ) : (
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#667eea', marginBottom: '1rem' }}>
            ${totalCost.toLocaleString()}
          </div>
          <div style={{ color: '#666' }}>
            Total Project Cost
          </div>
          <div style={{ fontSize: '0.875rem', color: '#999', marginTop: '0.5rem' }}>
            Detailed breakdown will be available after scope generation
          </div>
        </div>
      )}

      <div style={{ marginTop: '1.5rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button style={{
          padding: '0.5rem 1rem',
          background: '#667eea',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontSize: '0.875rem'
        }}>
          SAVE DRAFT
        </button>
        <button style={{
          padding: '0.5rem 1rem',
          background: '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontSize: '0.875rem'
        }}>
          SHARE FOR REVIEW
        </button>
        <button style={{
          padding: '0.5rem 1rem',
          background: '#6c757d',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontSize: '0.875rem'
        }}>
          EXPORT FINALIZED SCOPE
        </button>
      </div>
    </div>
  );
};

export default CostEstimate;
