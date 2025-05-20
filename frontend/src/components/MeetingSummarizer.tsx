import React, { useState } from 'react';
import { uploadFile, analyzeFile, getResults } from '../lib/api';
import { Summary } from '../types';

const MeetingSummarizer: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisId, setAnalysisId] = useState<number | null>(null);
  const [resultId, setResultId] = useState<string>(''); // New state for input

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await uploadFile(file);
      setAnalysisId(response.id);
      setSummary(response);
      console.log('Uploaded, analysisId:', response.id); // Debug
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error uploading file');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!analysisId) {
      setError('No file uploaded yet');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await analyzeFile(analysisId);
      setSummary(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error analyzing file');
    } finally {
      setLoading(false);
    }
  };

  const handleGetResults = async () => {
    const id = parseInt(resultId) || analysisId;
    if (!id) {
      setError('Please enter a valid ID or upload a file');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await getResults(id);
      setSummary(response);
      console.log('Get Results response:', response); // Debug
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error retrieving results');
      console.error('Get Results error:', err); // Debug
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Meeting Summarizer</h1>
      
      <div className="mb-4">
        <input
          type="file"
          accept=".txt,.mp3,.wav"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-blue-50 file:text-blue-700
            hover:file:bg-blue-100"
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">
          Enter ID to Get Results (optional)
        </label>
        <input
          type="number"
          value={resultId}
          onChange={(e) => setResultId(e.target.value)}
          placeholder={analysisId ? `Using ID: ${analysisId}` : 'Enter ID'}
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
        />
      </div>

      <div className="mb-4 space-x-2">
        <button
          onClick={handleUpload}
          disabled={loading || !file}
          className="bg-blue-500 text-white py-2 px-4 rounded disabled:bg-gray-400"
        >
          {loading ? 'Uploading...' : 'Upload File'}
        </button>
        <button
          onClick={handleAnalyze}
          disabled={loading || !analysisId}
          className="bg-green-500 text-white py-2 px-4 rounded disabled:bg-gray-400"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
        <button
          onClick={handleGetResults}
          disabled={loading}
          className="bg-purple-500 text-white py-2 px-4 rounded disabled:bg-gray-400"
        >
          {loading ? 'Fetching...' : 'Get Results'}
        </button>
      </div>

      {error && (
        <div className="text-red-500 mb-4">{error}</div>
      )}

      {summary && (
        <div className="bg-gray-100 p-4 rounded">
          <h2 className="text-xl font-semibold">Summary</h2>
          <p><strong>ID:</strong> {summary.id}</p>
          <p><strong>Filename:</strong> {summary.filename}</p>
          <p><strong>Status:</strong> {summary.status}</p>
          {summary.summary && (
            <div>
              <h3 className="text-lg font-medium">Summary Content:</h3>
              <p>{summary.summary}</p>
            </div>
          )}
          <p><strong>Created At:</strong> {new Date(summary.created_at).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
};

export default MeetingSummarizer;