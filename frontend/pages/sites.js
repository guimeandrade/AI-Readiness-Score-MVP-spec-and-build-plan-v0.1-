import { useState, useEffect } from 'react';

export default function SitesPage() {
  const [sites, setSites] = useState([]);
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    // Fetch list of monitored sites from backend
    const fetchSites = async () => {
      try {
        const res = await fetch(`${API_URL}/sites`);
        if (!res.ok) {
          throw new Error('Failed to fetch sites');
        }
        const data = await res.json();
        setSites(data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchSites();
  }, [API_URL]);

  const handleAddSite = async (e) => {
  e.preventDefault();
    setError('');
    if (!url) return;
    try {
      const res = await fetch(`${API_URL}/sites`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      if (res.ok) {
        const data = await res.json();
        setSites([...sites, data]);
        setUrl('');
      } else {
        const text = await res.text();
        setError('Failed to add site: ' + text);
      }
    } catch (err) {
      setError('Error: ' + err.message);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '20px auto' }}>
      <h1>Monitored Sites</h1>
      <form onSubmit={handleAddSite} style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter site URL"
          style={{ width: '70%', padding: '8px' }}
        />
        <button type="submit" style={{ padding: '8px 12px', marginLeft: '8px' }}>
          Add Site
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {sites.map((site, index) => (
          <li key={index} style={{ marginBottom: '10px' }}>
            <strong>{site.url}</strong> – Score: {site.score ?? 'N/A'}
            {site.recommendations && site.recommendations.length > 0 && (
              <ul>
                {site.recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
