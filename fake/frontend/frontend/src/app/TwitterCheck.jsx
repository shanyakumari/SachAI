"use client";
import React, { useState, useEffect } from 'react';
import {
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Tooltip,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend
} from 'recharts';
import { motion } from "framer-motion";

export default function TwitterCheck() {
  const [username, setUsername] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [assistantReply, setAssistantReply] = useState('');
  const [model, setModel] = useState('random_forest'); // Default model

  useEffect(() => {
    const stored = localStorage.getItem('recent_checks');
    if (stored) setHistory(JSON.parse(stored));
  }, []);

  const saveToHistory = (username) => {
    const updated = [username, ...history.filter((u) => u !== username)].slice(0, 5);
    setHistory(updated);
    localStorage.setItem('recent_checks', JSON.stringify(updated));
  };

  const handleCheck = async (name = username, selectedModel = model) => {
    setLoading(true);
    setResult(null);
    setAssistantReply('');
    try {
      const response = await fetch('http://localhost:5000/predict-twitter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: name, model: selectedModel }),
      });
      const data = await response.json();
      setResult(data);
      saveToHistory(name);
      generateAssistantResponse(data);

      const newEntry = {
        username: name,
        is_fake: data.is_fake,
        confidence: data.confidence,
        checked_at: new Date().toLocaleString(),
      };
      const past = JSON.parse(localStorage.getItem("detailed_history") || "[]");
      localStorage.setItem("detailed_history", JSON.stringify([newEntry, ...past.slice(0, 19)]));
    } catch (err) {
      setResult({ error: 'Something went wrong. Try again.' });
    }
    setLoading(false);
  };

  const generateAssistantResponse = (data) => {
    if (!data || data.error) return;

    const messages = [];
    const suspicious = [];

    if (data.followers < 10) suspicious.push('very few followers');
    if (data.following > 1000) suspicious.push('high following count');
    if (data.tweets < 5) suspicious.push('very few tweets');
    if (!data.profile_image_url) suspicious.push('no profile picture');
    if (!data.bio || data.bio.length < 10) suspicious.push('short or missing bio');
    if (data.username?.match(/\d{3,}/)) suspicious.push('username contains suspicious numbers');
    if (data.follower_following_ratio < 0.1) suspicious.push('low follower-to-following ratio');

    if (suspicious.length === 0) {
      messages.push('✅ This account appears genuine based on the visible metrics.');
    } else {
      messages.push('⚠️ This account shows the following red flags:');
      messages.push(...suspicious.map((s) => `• ${s}`));
      messages.push("🧠 The model considered these to likely mark it as suspicious.");
    }

    setAssistantReply(messages.join('\n'));
  };

  const getChartData = () => {
    if (!result) return [];
    return [
      { feature: 'Followers', value: Math.min(result.followers, 1000000) },
      { feature: 'Following', value: Math.min(result.following, 10000) },
      { feature: 'Tweets', value: Math.min(result.tweets, 100000) },
      { feature: 'Listed', value: result.listed || 0 },
      { feature: 'Bio Length', value: result.bio?.length || 0 },
      { feature: 'Profile Pic', value: result.profile_image_url ? 1 : 0 },
      { feature: 'Account Age', value: result.account_age_days },
      { feature: 'Ratio', value: Math.round((result.followers / result.following) * 10) / 10 },
    ];
  };

  const getBarData = () => {
    if (!result) return [];
    return [
      { name: 'Followers', Current: Math.min(result.followers, 100000), Average: 5000 },
      { name: 'Tweets', Current: Math.min(result.tweets, 100000), Average: 1500 },
      { name: 'Following', Current: Math.min(result.following, 10000), Average: 500 },
      { name: 'Bio Length', Current: result.bio?.length || 0, Average: 80 },
    ];
  };

  const exportCSV = () => {
    const csv = `Field,Value\nUsername,${result.username}\nName,${result.name}\nFollowers,${result.followers}\nFollowing,${result.following}\nTweets,${result.tweets}\nBio Length,${result.bio?.length || 0}\nConfidence,${result.confidence}%\nFake,${result.is_fake}`;
    const blob = new Blob([csv], { type: 'text/csv' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${result.username}_report.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-blue-800 to-purple-900 text-white flex">
      <div className="flex-1 p-4 flex flex-col items-center justify-center">
        <div className="bg-[#1f1f2e] p-8 rounded-2xl shadow-lg max-w-xl w-full" id="result-box">
          <h1 className="text-3xl font-bold text-center mb-6">🔍 Fake Account Detector</h1>

          <div className="text-3xl md:text-4xl font-extrabold text-center mb-6 flex justify-center gap-1">
            {"SachAI".split("").map((char, index) => (
              <motion.span
                key={index}
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1, type: "spring", stiffness: 300 }}
                className="text-blue-400"
              >
                {char}
              </motion.span>
            ))}
          </div>

          <input
            type="text"
            placeholder="Enter Twitter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-3 rounded bg-gray-800 text-white border border-blue-400 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <div className="flex justify-between mt-4">
            <button
              onClick={() => setModel('random_forest')}
              className={`py-2 px-4 rounded ${model === 'random_forest' ? 'bg-blue-600' : 'bg-blue-400'}`}
            >
              Random Forest
            </button>
            <button
              onClick={() => setModel('knn')}
              className={`py-2 px-4 rounded ${model === 'knn' ? 'bg-blue-600' : 'bg-blue-400'}`}
            >
              KNN
            </button>
            <button
              onClick={() => setModel('linear_svc')}
              className={`py-2 px-4 rounded ${model === 'linear_svc' ? 'bg-blue-600' : 'bg-blue-400'}`}
            >
              Linear SVC
            </button>
          </div>
          <button
            onClick={() => handleCheck()}
            className="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded shadow"
            disabled={loading}
          >
            {loading ? 'Checking...' : 'Check'}
          </button>

          {result && (
            <div className="mt-6 space-y-4 text-center">
              {result.error ? (
                <p className="text-red-400">{result.error}</p>
              ) : (
                <>
                  <img src={result.profile_image_url} alt="Profile" className="w-24 h-24 rounded-full mx-auto border-4 border-blue-400 shadow" />
                  <h2 className="text-xl font-semibold">{result.name} (@{result.username})</h2>
                  <p className="text-gray-300 italic">📝 {result.bio || 'No bio available'}</p>
                  <div className="grid grid-cols-2 gap-4 text-sm text-gray-300 mt-4">
                    <p><strong>Followers:</strong><br />{result.followers}</p>
                    <p><strong>Following:</strong><br />{result.following}</p>
                    <p><strong>Tweets:</strong><br />{result.tweets}</p>
                    <p><strong>Account Age:</strong><br />{result.account_age_days} days</p>
                    <p><strong>Joined:</strong><br />{result.created_at}</p>
                  </div>
                  <div className="text-lg font-bold mt-4">
                    {result.is_fake
                      ? <span className="text-red-400">⚠️ Fake Account Detected</span>
                      : <span className="text-green-400">✅ Real Account</span>}
                  </div>
                  <h3 className="text-lg font-semibold mt-6 mb-2">📊 Feature Radar</h3>
                  <div className="w-full h-80">
                    <ResponsiveContainer>
                      <RadarChart cx="50%" cy="50%" outerRadius="80%" data={getChartData()}>
                        <PolarGrid stroke="#ccc" />
                        <PolarAngleAxis dataKey="feature" stroke="#ddd" tick={{ fontSize: 12 }} />
                        <PolarRadiusAxis stroke="#555" angle={30} domain={[0, 100000]} tickFormatter={(val) => val > 1000 ? `${val / 1000}k` : val} />
                        <Radar name="Features" dataKey="value" stroke="#38bdf8" fill="#38bdf8" fillOpacity={0.6} />
                        <Tooltip formatter={(value) => value.toLocaleString()} />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                  <h3 className="text-lg font-semibold mt-8 mb-2">📈 Comparison with Average</h3>
                  <div className="w-full h-72">
                    <ResponsiveContainer>
                      <BarChart data={getBarData()} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#555" />
                        <XAxis dataKey="name" stroke="#ccc" tick={{ fontSize: 12 }} />
                        <YAxis stroke="#ccc" tick={{ fontSize: 12 }} />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="Current" fill="#38bdf8" />
                        <Bar dataKey="Average" fill="#9333ea" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="w-80 bg-[#161625] border-l border-gray-700 p-4 text-sm space-y-4">
        <h2 className="text-lg font-semibold mb-2">🗂 Recent History</h2>
        <ul className="space-y-2">
          {history.map((user, idx) => (
            <li key={idx} className="flex justify-between items-center bg-gray-800 px-3 py-2 rounded">
              <span className="truncate">@{user}</span>
              <button
                onClick={() => handleCheck(user)}
                className="text-blue-400 hover:text-blue-600 text-xs"
              >Recheck</button>
            </li>
          ))}
        </ul>

        {result && (
          <div className="pt-4 border-t border-gray-700">
            <h2 className="text-lg font-semibold mb-2">📤 Export</h2>
            <button
              onClick={exportCSV}
              className="block w-full bg-purple-600 hover:bg-purple-700 text-white py-2 px-4 rounded"
            >Export CSV</button>
          </div>
        )}

        <div className="pt-4 border-t border-gray-700">
          <h2 className="text-lg font-semibold mb-2">🤖 AI Assistant</h2>
          <p className="text-gray-400 whitespace-pre-wrap">{assistantReply || 'Ask a question to learn why the model made this decision.'}</p>
        </div>
      </div>
    </div>
  );
}
