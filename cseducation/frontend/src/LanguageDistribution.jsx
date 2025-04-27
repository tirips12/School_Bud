import React from 'react';
import { Card, ProgressBar } from 'react-bootstrap';

// Sample language data - in a real app, this would come from an API
const languageData = [
  { name: 'Python', percent: 42, color: '#3498db' },
  { name: 'JavaScript', percent: 28, color: '#2ecc71' },
  { name: 'HTML/CSS', percent: 15, color: '#e74c3c' },
  { name: 'Java', percent: 10, color: '#f39c12' },
  { name: 'C++', percent: 5, color: '#9b59b6' }
];

const LanguageDistribution = () => {
  return (
    <Card className="h-100">
      <Card.Body className="p-0">
        {languageData.map((language, index) => (
          <div key={language.name} className={`px-3 py-2 ${index !== languageData.length - 1 ? 'mb-3' : ''}`}>
            <div className="language-bar d-flex align-items-center mb-2">
              <div 
                className="language-color me-2" 
                style={{
                  width: '12px', 
                  height: '12px', 
                  borderRadius: '50%', 
                  backgroundColor: language.color
                }}
              />
              <div className="language-name flex-grow-1">{language.name}</div>
              <div className="language-percent fw-bold">{language.percent}%</div>
            </div>
            <ProgressBar 
              now={language.percent} 
              style={{ height: '8px', backgroundColor: '#f8f9fa' }}
              variant="" // Remove default styling
              className="mb-1"
            >
              <ProgressBar 
                now={language.percent} 
                style={{ backgroundColor: language.color }} 
              />
            </ProgressBar>
          </div>
        ))}
      </Card.Body>
    </Card>
  );
};

export default LanguageDistribution;
