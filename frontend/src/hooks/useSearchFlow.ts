import { useState, useCallback } from 'react';
import { useSearch } from './useSearch';
import { useMessages } from './useMessages';
import { handleSearchError, handleSubmitError } from '../lib/errorHandling';
import type { LLMProvider } from '../lib/apiKeys';
import type { SearchMode } from '../components/SearchInput';
import type { Step } from '../components/ProgressSteps';
import type { SearchResultItem } from '../types/search';

export const useSearchFlow = () => {
  const [currentStep, setCurrentStep] = useState<Step>("query");
  const [isLoading, setIsLoading] = useState(false);
  const [searchMode, setSearchMode] = useState<SearchMode>("quick");
  
  const search = useSearch();
  const messagesHandler = useMessages();

  const pollForResults = useCallback(async (sessionId: string, loadingMessageId?: string) => {
    try {
      const result = await search.pollForResults(sessionId);
      
      if (result.status === 'completed' && (result.results || result.resources)) {
        setCurrentStep("results");
        setIsLoading(false);
        
        // Remove loading message if provided
        if (loadingMessageId) {
          messagesHandler.removeMessage(loadingMessageId);
        }
        
        // Add comprehensive result message with all data
        if (result.reportMarkdown) {
          messagesHandler.addMessage({
            type: "result",
            content: result.reportMarkdown, // Pass markdown string as content
            data: {
              reportMarkdown: result.reportMarkdown,
              images: result.images || [],
              resources: result.resources || [],
              userDetails: result.userDetails,
            },
          });
        } else if (result.resources && result.resources.length > 0) {
          // Fallback to old behavior if no report data
          messagesHandler.addMessage({
            type: "system",
            content: `Found ${result.resources.length} relevant sources:`,
          });

          result.resources.forEach((resultItem: SearchResultItem) => {
            messagesHandler.addMessage({
              type: "result",
              content: resultItem.content || resultItem.title,
              data: {
                title: resultItem.title,
                url: resultItem.url,
                source: new URL(resultItem.url).hostname,
                content: resultItem.content,
                score: resultItem.score,
                image: resultItem.image,
                search_query: resultItem.search_query,
              },
            });
          });
        } else {
          messagesHandler.addMessage({
            type: "system",
            content: "No search results found for your query. Try adjusting your search terms.",
          });
        }
      } else if (result.status === 'error') {
        setIsLoading(false);
        
        // Remove loading message if provided
        if (loadingMessageId) {
          messagesHandler.removeMessage(loadingMessageId);
        }
        
        messagesHandler.addMessage({
          type: "system",
          content: `Search error: ${result.error}`,
        });
      } else {
        // Still processing, poll again after 3 seconds
        setTimeout(() => pollForResults(sessionId, loadingMessageId), 3000);
      }
    } catch (error) {
      console.error('Error polling for results:', error);
      setIsLoading(false);
      
      // Remove loading message if provided
      if (loadingMessageId) {
        messagesHandler.removeMessage(loadingMessageId);
      }
      
      messagesHandler.addMessage({
        type: "system",
        content: "Error retrieving results. Please try again.",
      });
    }
  }, [search, messagesHandler]);

  const startSearchFlow = useCallback(async (query: string, provider: LLMProvider, mode: SearchMode) => {
    setIsLoading(true);
    setCurrentStep("query");
    setSearchMode(mode); // Store the search mode for later use
    
    // Clear previous session data
    search.clearSession();
    messagesHandler.clearMessages();

    // Add user message
    messagesHandler.addMessage({
      type: "user",
      content: query,
    });

    // Add loading message
    const loadingMessageId = messagesHandler.addMessage({
      type: "loading",
      content: "Analyzing your query and preparing clarification questions...",
    });

    try {
      const response = await search.startSearch(query, provider);
      
      // Remove loading message
      messagesHandler.removeMessage(loadingMessageId);
      
      // Move to questions step
      setCurrentStep("questions");
      

      // Add clarification questions as messages
      response.clarification.forEach((question) => {
        messagesHandler.addMessage({
          type: "question",
          content: question.text,
          choices: question.choices,
          data: { question_id: question.question_id },
        });
      });

      setIsLoading(false);

    } catch (error) {
      // Remove loading message
      messagesHandler.removeMessage(loadingMessageId);
      setIsLoading(false);
      
      if (error instanceof Error && error.message === 'API_KEY_MISSING') {
        throw error; // Re-throw to handle in component
      }
      
      const errorMessage = handleSearchError(error);
      messagesHandler.addMessage({
        type: "system",
        content: errorMessage,
      });
    }
  }, [search, messagesHandler]);

  const handleChoiceSelect = useCallback((messageId: string, choice: string) => {
    // Update the message with selected choice
    messagesHandler.updateMessage(messageId, { selectedChoice: choice });
    
    // Find the question this choice belongs to
    const questionMessage = messagesHandler.findMessage(messageId);
    if (questionMessage?.data?.question_id) {
      search.answerQuestion(questionMessage.data.question_id as string, choice);
    }
  }, [messagesHandler, search]);

  const submitAnswers = useCallback(async () => {
    if (!search.session.sessionId) return;

    setCurrentStep("answers");
    setIsLoading(true);
    
    // Add summary of answers with loading animation
    const answeredCount = Object.keys(search.session.answeredQuestions).length;
    const skippedCount = search.session.pendingQuestions.length - answeredCount;
    
    const submitLoadingMessageId = messagesHandler.addMessage({
      type: "loading",
      content: `Processing ${answeredCount} answers${skippedCount > 0 ? ` (${skippedCount} skipped)` : ''}...`,
    });

    try {
      const originalQuery = messagesHandler.getUserQuery();
      const response = await search.submitAnswers(originalQuery, searchMode);

      // Remove submit loading message
      messagesHandler.removeMessage(submitLoadingMessageId);
      
      setCurrentStep("results");
      setIsLoading(false);
      
      if (response.status === "completed") {
        messagesHandler.addMessage({
          type: "system",
          content: "Search completed immediately - this is unexpected. Please check results.",
        });
      } else if (response.status === "started_search") {
        // Add loading message for search processing
        const searchLoadingMessageId = messagesHandler.addMessage({
          type: "loading",
          content: "Searching the web and generating comprehensive results...",
        });
        
        // Start polling for results with loading message ID to remove later
        pollForResults(response.session_id, searchLoadingMessageId);
      } else {
        const errorMessage = response.error || "Search could not be completed.";
        setIsLoading(false);
        messagesHandler.addMessage({
          type: "system",
          content: `Search error: ${errorMessage}`,
        });
      }

    } catch (error) {
      // Remove submit loading message
      messagesHandler.removeMessage(submitLoadingMessageId);
      setIsLoading(false);
      search.answerQuestion('', ''); // Reset to show submit button again
      
      const errorMessage = handleSubmitError(error);
      messagesHandler.addMessage({
        type: "system",
        content: errorMessage,
      });
    }
  }, [search, messagesHandler, pollForResults, searchMode]);

  return {
    currentStep,
    isLoading,
    messages: messagesHandler.messages,
    showSubmitButton: search.showSubmitButton,
    startSearchFlow,
    handleChoiceSelect,
    submitAnswers,
  };
};
