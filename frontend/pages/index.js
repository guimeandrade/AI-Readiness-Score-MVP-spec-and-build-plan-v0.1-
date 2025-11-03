import { useState } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      if (response.ok) {
        const data = await response.json();
        setResult(data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>AI Readiness Score</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter website URL"
          style={{ width: '300px', marginRight: '0.5rem' }}
        />
        <button type="submit">Scan</button>
      </form>
      {result && (
        <div style={{ marginTop: '1rem' }}>
          <h2>Results for {result.url}</h2>
          <p>Score: {result.score}</p>
          {result.details && (
            <>
              <h3>Category Breakdown</h3>
              <ul>
                {Object.entries(result.details).map(([category, value]) => (
                  <li key={category}>
                    {category}: {value.toFixed(1)}
                  </li>
                ))}
              </ul>
            </>
          )}
          {result.recommendations && result.recommendations.length > 0 && (
            <>
              <h3>Recommendations</h3>
              <ul>
                {result.recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}
