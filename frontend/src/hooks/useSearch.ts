import { useState, useCallback } from 'react';
import { searchApi } from '@/services/searchApi';
import type { SearchSession, SearchResultItem } from '@/types/search';
import type { LLMProvider } from '@/lib/apiKeys';
import { getApiKey, getModel, getBaseUrl } from '@/lib/apiKeys';

export const useSearch = () => {
  const [session, setSession] = useState<SearchSession>({
    sessionId: null,
    pendingQuestions: [],
    answeredQuestions: {},
  });
  const [showSubmitButton, setShowSubmitButton] = useState(false);

  const clearSession = useCallback(() => {
    setSession({
      sessionId: null,
      pendingQuestions: [],
      answeredQuestions: {},
    });
    setShowSubmitButton(false);
  }, []);

  const startSearch = useCallback(async (query: string, provider: LLMProvider) => {
    const apiKey = getApiKey(provider);
    const model = getModel(provider);
    const baseUrl = getBaseUrl(provider);
    
    if (!apiKey) {
      throw new Error('API_KEY_MISSING');
    }

    const payload = {
      query,
      LLM_PROVIDER: provider,
      LLM_API_KEY: apiKey,
      LLM_BASE_URL: baseUrl,
      LLM_MODEL: model,
    };

    const response = await searchApi.startSearch(payload);
    
    setSession({
      sessionId: response.session_id,
      pendingQuestions: response.clarification,
      answeredQuestions: {},
    });

    return response;
  }, []);

  const answerQuestion = useCallback((questionId: string, choice: string) => {
    setSession(prev => {
      const newAnsweredQuestions = {
        ...prev.answeredQuestions,
        [questionId]: choice,
      };
      
      const hasAnswers = Object.keys(newAnsweredQuestions).length > 0;
      setShowSubmitButton(hasAnswers);
      
      return {
        ...prev,
        answeredQuestions: newAnsweredQuestions,
      };
    });
  }, []);

  const submitAnswers = useCallback(async (originalQuery: string, searchMode: string = "quick") => {
    if (!session.sessionId) {
      throw new Error('No active session');
    }

    const answers = session.pendingQuestions.map(q => ({
      question_id: q.question_id,
      question: q.text,
      choice: session.answeredQuestions[q.question_id] || "Skip"
    }));

    const payload = {
      session_id: session.sessionId,
      search_mode: searchMode,
      query: originalQuery,
      answers,
    };

    const response = await searchApi.submitAnswers(payload);
    setShowSubmitButton(false);
    
    return response;
  }, [session]);

  const pollForResults = useCallback(async (sessionId: string): Promise<{
    status: string;
    results?: SearchResultItem[];
    resources?: SearchResultItem[];
    userDetails?: string;
    reportMarkdown?: string;
    images?: string[];
    error?: string;
  }> => {
    const response = await searchApi.getResults(sessionId);

    // Handle both string and object report types
    let reportMarkdown: string | undefined = undefined;
    if (typeof response.report === 'string') {
      reportMarkdown = response.report;
    } else if (response.report && typeof response.report === 'object') {
      reportMarkdown = `# ${response.report.title}\n\n${response.report.answer}`;
    }

    if (response.status === 'completed') {
      return {
        status: 'completed',
        results: response.resources, // Keep for backward compatibility
        resources: response.resources,
        userDetails: response.user_details,
        reportMarkdown,
        images: response.images,
      };
    } else if (response.error) {
      return {
        status: 'error',
        error: response.error,
      };
    } else {
      return {
        status: 'processing',
      };
    }
  }, []);

  return {
    session,
    showSubmitButton,
    clearSession,
    startSearch,
    answerQuestion,
    submitAnswers,
    pollForResults,
  };
};
