import { useState, useEffect } from 'react';

const SitesPage = () => {
  const [sites, setSites] = useState([]);
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');

  const API_URL = process.env.NEXT_PUBLIC_API_URL || '';

  const fetchSites = async () => {
    try {
      const res = await fetch(`${API_URL}/sites`);
      if (!res.ok) throw new Error('Failed to fetch sites');
      const data = await res.json();
      setSites(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchSites();
  }, []);

  const handleAddSite = async (e) => {
    e.preventDefault();
    if (!url.trim()) {
      setError('Please enter a URL.');
      return;
    }
    try {
      const res = await fetch(`${API_URL}/sites`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      if (!res.ok) {
        throw new Error('Failed to add site');
      }
      const data = await res.json();
      setSites([...sites, data]);
      setUrl('');
      setError('');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: '1rem' }}>
      <h1>Monitored Sites</h1>
      <form onSubmit={handleAddSite} style={{ marginBottom: '1rem' }}>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter website URL"
          style={{ width: '300px', marginRight: '0.5rem' }}
        />
        <button type="submit">Add Site</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {sites.map((site) => (
          <li key={site.url} style={{ marginBottom: '1rem' }}>
            <strong>{site.url}</strong>
            <div>Score: {site.score}</div>
            {site.details && (
              <div>
                <em>Category Breakdown:</em>
                <ul>
                  {Object.entries(site.details).map(([category, value]) => (
                    <li key={category}>
                      {category}: {value.toFixed(1)}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {site.recommendations && site.recommendations.length > 0 && (
              <div>
                <em>Recommendations:</em>
                <ul>
                  {site.recommendations.map((rec, idx) => (
                    <li key={idx}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SitesPage;
