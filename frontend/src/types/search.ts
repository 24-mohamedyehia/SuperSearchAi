export interface ClarificationQuestion {
  question_id: string;
  text: string;
  choices: string[];
}

export interface SearchResultItem {
  title: string;
  url: string;
  content: string;
  score?: number;
  image?: string;
  search_query?: string;
}

export interface SearchSession {
  sessionId: string | null;
  pendingQuestions: ClarificationQuestion[];
  answeredQuestions: Record<string, string>;
}

export interface SearchPayload {
  query: string;
  LLM_PROVIDER: string;
  LLM_API_KEY: string;
  LLM_BASE_URL: string;
  LLM_MODEL: string;
}

export interface AnswersPayload {
  session_id: string;
  search_mode: string;
  query: string;
  answers: Array<{
    question_id: string;
    question: string;
    choice: string;
  }>;
}

export interface SearchResponse {
  session_id: string;
  clarification: ClarificationQuestion[];
}

export interface SubmitResponse {
  session_id: string;
  status: string;
  error?: string;
}

export interface ResultsResponse {
  session_id: string;
  status: string;
  search_mode?: string;
  query?: string;
  user_details?: string;
  report?: {
    title: string;
    answer: string;
  };
  images?: string[];
  resources?: SearchResultItem[];
  created_at?: string;
  completed_at?: string;
  error?: string;
}
