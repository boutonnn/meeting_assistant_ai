import axios from 'axios';
import { Summary } from '../types';

const API_URL = 'http://localhost:8000';

export const uploadFile = async (file: File): Promise<Summary> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post(`${API_URL}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const analyzeFile = async (id: number): Promise<Summary> => {
  const response = await axios.post(`${API_URL}/analyze`, null, {
    params: { id }
  });
  return response.data;
};

export const getResults = async (id: number): Promise<Summary> => {
  const response = await axios.get(`${API_URL}/results/${id}`);
  return response.data;
};