import React, { useEffect, useState } from 'react';
import GithubAnalytics from './GithubAnalytics';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Form, Table, Badge, Spinner, Tabs, Tab, Card } from 'react-bootstrap';

// Mount Per-Course Activity as a card with tabs (for consistency)
export function PerCourseActivity({ stats }) {
  const [tab, setTab] = useState('per-course');
  return (
    <Card className="mb-4 shadow-sm">
      <Card.Header className="bg-white border-bottom-0 pb-0">
        <h4 className="mb-0">Per-Course Activity</h4>
      </Card.Header>
      <Card.Body>
        <Tabs activeKey={tab} onSelect={setTab} className="mb-3">
          <Tab eventKey="per-course" title="Overview">
            <Table striped bordered hover responsive className="align-middle">
              <thead className="table-light">
                <tr>
                  <th>Course</th>
                  <th>Questions</th>
                  <th>Answers</th>
                  <th>Project Discussions</th>
                  <th>Enrolled Students</th>
                </tr>
              </thead>
              <tbody>
                {stats.map(stat => (
                  <tr key={stat.course.id}>
                    <td>
                      <a href={`/courses/${stat.course.id}/`} className="d-flex align-items-center text-decoration-none">
                        <Badge bg="secondary" className="me-2">{stat.course.code}</Badge>
                        <span className="fw-bold">{stat.course.name}</span>
                      </a>
                    </td>
                    <td><Badge bg="primary">{stat.questions}</Badge></td>
                    <td><Badge bg="info" text="dark">{stat.answers}</Badge></td>
                    <td><Badge bg="success">{stat.discussions}</Badge></td>
                    <td><Badge bg="dark">{stat.students}</Badge></td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Tab>
        </Tabs>
      </Card.Body>
    </Card>
  );
}

// These mounting functions are no longer needed since we're using createRoot in analytics-dashboard-mount.js
// Keeping them for backward compatibility but they're not used
export function mountGithubAnalytics() {
  console.warn('mountGithubAnalytics is deprecated - use createRoot instead');
  return null;
}

export function mountPerCourseActivity(stats) {
  console.warn('mountPerCourseActivity is deprecated - use createRoot instead');
  return null;
}

// Mount Activity Log into its own div
import { Pagination, OverlayTrigger, Tooltip } from 'react-bootstrap';

export function ActivityLog() {
  const [allLogs, setAllLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [activeCategory, setActiveCategory] = useState('all');
  const [page, setPage] = useState(1);
  const pageSize = 10; // Number of items per page

  // Fetch all logs at once instead of paginated
  const fetchAllLogs = () => {
    setLoading(true);
    // Use limit=1000 to get a large number of logs (adjust as needed)
    fetch(`/api/eventlogs/?limit=1000`)
      .then((res) => res.json())
      .then((data) => {
        setAllLogs(data.results);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching logs:', error);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchAllLogs();
  }, []);

  // Reset to first page when filters change
  useEffect(() => {
    setPage(1);
  }, [filter, activeCategory]);

  const handlePageChange = (newPage) => {
    setPage(newPage);
  };

  // Define event categories
  const categories = {
    all: { label: 'All Activities', filter: () => true },
    questions: { 
      label: 'Questions', 
      filter: (log) => log.event_type.includes('question') 
    },
    answers: { 
      label: 'Answers', 
      filter: (log) => log.event_type.includes('answer') 
    },
    github: { 
      label: 'GitHub', 
      filter: (log) => log.event_type.startsWith('github_') 
    },
    votes: { 
      label: 'Votes', 
      filter: (log) => log.event_type.includes('vote') 
    }
  };
  
  // Apply both category and text filters to all logs
  const filteredLogs = allLogs.filter(log => {
    // First apply category filter
    const passesCategoryFilter = categories[activeCategory].filter(log);
    if (!passesCategoryFilter) return false;
    
    // If no text filter, return all logs that pass category filter
    if (!filter.trim()) return true;
    
    // Apply text filter
    const searchTerm = filter.toLowerCase();
    return log.event_type.toLowerCase().includes(searchTerm) ||
      (log.description && log.description.toLowerCase().includes(searchTerm)) ||
      (log.user && log.user.username && log.user.username.toLowerCase().includes(searchTerm));
  });
  
  // Calculate total pages based on filtered logs
  const totalPages = Math.ceil(filteredLogs.length / pageSize);
  
  // Get current page of filtered logs
  const currentPageLogs = filteredLogs.slice((page - 1) * pageSize, page * pageSize);

  // Helper for event type styling
  const getRowClass = (eventType) => {
    if (eventType.startsWith('github_')) return 'table-info';
    if (eventType === 'question_created_module') return 'table-success'; // module-specific
    if (['question_created', 'answer_created', 'vote'].includes(eventType)) return 'table-light'; // default
    return '';
  };
  const getBadge = (eventType) => {
    if (eventType.startsWith('github_')) return <Badge bg="danger">GitHub</Badge>;
    if (eventType === 'question_created_module') return <Badge bg="success">Module Q</Badge>;
    if (eventType === 'question_created') return <Badge bg="primary">Q</Badge>;
    if (eventType === 'answer_created') return <Badge bg="info">A</Badge>;
    if (eventType === 'vote') return <Badge bg="secondary">Vote</Badge>;
    return <Badge bg="dark">{eventType}</Badge>;
  };

  // Reusable React Pagination component
  function ReactPagination({ current, total, onPageChange }) {
    if (total <= 1) return null;
    const items = [];
    const maxButtons = 7;
    let start = Math.max(1, current - Math.floor(maxButtons / 2));
    let end = Math.min(total, start + maxButtons - 1);
    if (end - start < maxButtons - 1) {
      start = Math.max(1, end - maxButtons + 1);
    }
    // Always show First and Prev
    items.push(
      <Pagination.First key="first" onClick={() => onPageChange(1)} disabled={current === 1} />
    );
    items.push(
      <Pagination.Prev key="prev" onClick={() => onPageChange(current - 1)} disabled={current === 1} />
    );
    // Page numbers
    for (let i = start; i <= end; i++) {
      items.push(
        <Pagination.Item key={i} active={i === current} onClick={() => onPageChange(i)}>
          {i}
        </Pagination.Item>
      );
    }
    // Always show Next and Last
    items.push(
      <Pagination.Next key="next" onClick={() => onPageChange(current + 1)} disabled={current === total} />
    );
    items.push(
      <Pagination.Last key="last" onClick={() => onPageChange(total)} disabled={current === total} />
    );
    return <Pagination>{items}</Pagination>;
  }

  // Handle clearing the search filter
  const handleClearFilter = () => {
    setFilter('');
  };

  return (
    <Card className="mb-4">
      <Card.Header>
        <div className="d-flex align-items-center justify-content-between mb-3">
          <h4 className="mb-0">Recent Activity Log</h4>
          <div className="d-flex align-items-center">
            <div className="position-relative" style={{ maxWidth: 320 }}>
              <Form.Control
                type="text"
                placeholder="Filter by user, event, description..."
                value={filter}
                onChange={e => setFilter(e.target.value)}
                className="pe-4"
              />
              {filter && (
                <button 
                  className="btn btn-sm position-absolute" 
                  style={{ right: '4px', top: '50%', transform: 'translateY(-50%)', border: 'none' }}
                  onClick={handleClearFilter}
                >
                  <i className="fas fa-times text-muted"></i>
                </button>
              )}
            </div>
          </div>
        </div>
        
        {/* Category filter buttons */}
        <div className="d-flex flex-wrap gap-2">
          {Object.entries(categories).map(([key, category]) => (
            <button
              key={key}
              className={`btn btn-sm ${activeCategory === key ? 'btn-primary' : 'btn-outline-secondary'}`}
              onClick={() => setActiveCategory(key)}
            >
              {category.label}
            </button>
          ))}
        </div>
      </Card.Header>
      <Card.Body className="p-0">
        {loading ? (
          <div className="text-center my-4"><Spinner animation="border" /> Loading...</div>
        ) : (
          <>
            <Table striped hover responsive className="mb-0">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>User</th>
                  <th>Event</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {filteredLogs.length > 0 ? (
                  currentPageLogs.map(log => (
                    <tr key={log.id} className={getRowClass(log.event_type)}>
                      <td>{new Date(log.timestamp).toLocaleString()}</td>
                      <td>{log.user ? log.user.username : 'Anonymous'}</td>
                      <td>
                        <OverlayTrigger
                          placement="top"
                          overlay={<Tooltip>{log.event_type}</Tooltip>}
                        >
                          <span>{getBadge(log.event_type)}</span>
                        </OverlayTrigger>
                      </td>
                      <td>{log.description}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="text-center py-4">
                      <div className="d-flex flex-column align-items-center">
                        <i className="fas fa-search fa-2x text-muted mb-3"></i>
                        <h5 className="text-muted">No results found</h5>
                        <p className="text-muted mb-0">
                          {filter ? `No activities matching '${filter}'` : `No ${activeCategory !== 'all' ? categories[activeCategory].label.toLowerCase() : 'activities'} found`}
                        </p>
                        {(filter || activeCategory !== 'all') && (
                          <button 
                            className="btn btn-outline-primary btn-sm mt-3"
                            onClick={() => {
                              setFilter('');
                              setActiveCategory('all');
                            }}
                          >
                            <i className="fas fa-times me-1"></i> Clear filters
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                )}
              </tbody>
            </Table>
            <div className="d-flex justify-content-center py-3">
              <ReactPagination current={page} total={totalPages} onPageChange={handlePageChange} />
            </div>
          </>
        )}
      </Card.Body>
    </Card>
  );
}


// This mounting function is no longer needed since we're using createRoot in analytics-dashboard-mount.js
// Keeping it for backward compatibility but it's not used
export function mountActivityLog() {
  console.warn('mountActivityLog is deprecated - use createRoot instead');
  return null;
}
