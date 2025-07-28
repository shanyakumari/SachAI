import { useState } from 'react';

export default function Home() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    bio: '',
    followers: '',
    following: '',
    tweets: ''
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const res = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      const data = await res.json();
      setResult(data.result);
    } catch (err) {
      console.error(err);
      setResult('Error contacting backend');
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gray-100">
      <h1 className="text-3xl font-bold mb-4">Fake Account Detection</h1>
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md space-y-4 w-full max-w-md">
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label className="block text-sm font-medium text-gray-700 capitalize">{key}</label>
            <input
              type="text"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              required
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
            />
          </div>
        ))}
        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700">
          Detect
        </button>
      </form>
      {result && (
        <div className="mt-6 text-xl font-semibold">
          Prediction: <span className={result === 'Fake' ? 'text-red-500' : 'text-green-500'}>{result}</span>
        </div>
      )}
    </div>
  );
}
