import axios from 'axios';
import type { SearchPayload, AnswersPayload, SearchResponse, SubmitResponse, ResultsResponse } from '../types/search';

class SearchApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  }

  async startSearch(payload: SearchPayload): Promise<SearchResponse> {
    const response = await axios.post(`${this.baseUrl}/start/`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  }

  async submitAnswers(payload: AnswersPayload): Promise<SubmitResponse> {
    const response = await axios.post(`${this.baseUrl}/search/`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  }

  async getResults(sessionId: string): Promise<ResultsResponse> {
    const response = await axios.get(`${this.baseUrl}/results/?session_id=${sessionId}`);
    return response.data;
  }
}

export const searchApi = new SearchApiService();
