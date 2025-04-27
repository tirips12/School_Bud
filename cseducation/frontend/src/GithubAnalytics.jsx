import React, { useEffect, useState } from 'react';
import { Card, Table, Tabs, Tab, Badge, Spinner } from 'react-bootstrap';

export default function GithubAnalytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState('top_voted');

  useEffect(() => {
    fetch('/api/github-analytics/')
      .then(res => res.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center my-4"><Spinner animation="border" /> Loading GitHub analytics...</div>;
  if (!data) return <div className="alert alert-danger">Failed to load GitHub analytics.</div>;

  return (
    <Card className="mb-4">
      <Card.Header>
        <h4 className="mb-0">GitHub Integration Analytics</h4>
      </Card.Header>
      <Card.Body>
        <Tabs activeKey={tab} onSelect={setTab} className="mb-3">
          <Tab eventKey="top_voted" title="Top Voted Repos">
            <Table striped bordered hover responsive>
              <thead>
                <tr>
                  <th>Repo</th>
                  <th>Owner</th>
                  <th>Votes</th>
                  <th>Stars</th>
                  <th>Language</th>
                  <th>Last Updated</th>
                </tr>
              </thead>
              <tbody>
                {data.top_voted.map(repo => (
                  <tr key={repo.id}>
                    <td><a href={repo.url} target="_blank" rel="noopener noreferrer">{repo.name}</a></td>
                    <td><img src={repo.owner_avatar_url} alt={repo.owner} width={24} height={24} className="rounded me-2" />{repo.owner}</td>
                    <td><Badge bg="primary">{repo.votes}</Badge></td>
                    <td><Badge bg="warning" text="dark">{repo.stargazers_count}</Badge></td>
                    <td>{repo.language}</td>
                    <td>{new Date(repo.updated_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Tab>
          <Tab eventKey="top_commented" title="Most Commented Repos">
            <Table striped bordered hover responsive>
              <thead>
                <tr>
                  <th>Repo</th>
                  <th>Owner</th>
                  <th>Comments</th>
                  <th>Votes</th>
                  <th>Stars</th>
                  <th>Language</th>
                </tr>
              </thead>
              <tbody>
                {data.top_commented.map(repo => (
                  <tr key={repo.id}>
                    <td><a href={repo.url} target="_blank" rel="noopener noreferrer">{repo.name}</a></td>
                    <td><img src={repo.owner_avatar_url} alt={repo.owner} width={24} height={24} className="rounded me-2" />{repo.owner}</td>
                    <td>{repo.metadata && repo.metadata.num_comments ? repo.metadata.num_comments : '-'}</td>
                    <td><Badge bg="primary">{repo.votes}</Badge></td>
                    <td><Badge bg="warning" text="dark">{repo.stargazers_count}</Badge></td>
                    <td>{repo.language}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Tab>
          <Tab eventKey="recent_comments" title="Recent Comments">
            <Table striped bordered hover responsive>
              <thead>
                <tr>
                  <th>Repo</th>
                  <th>Comment</th>
                  <th>Author</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {data.recent_comments.map(comment => (
                  <tr key={comment.id}>
                    <td>{comment.repo}</td>
                    <td>{comment.content}</td>
                    <td>{comment.author_username}</td>
                    <td>{new Date(comment.created_at).toLocaleString()}</td>
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
