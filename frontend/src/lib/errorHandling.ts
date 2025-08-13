import axios from 'axios';

export const handleSearchError = (error: unknown): string => {
  console.error('Search error:', error);
  
  if (axios.isAxiosError(error)) {
    console.error('Response data:', error.response?.data);
    console.error('Response status:', error.response?.status);
    console.error('Response headers:', error.response?.headers);
    
    // Log detailed validation errors
    if (error.response?.data?.detail) {
      console.error('Validation errors:', error.response.data.detail);
      error.response.data.detail.forEach((err: unknown, index: number) => {
        console.error(`Error ${index + 1}:`, err);
      });
    }
    
    // Handle specific backend signals
    if (error.response?.data?.signal === 'no_related_questions') {
      return "Please make sure your API key is valid and try again.";
    }

    // Handle specific error messages from backend
    if (error.response?.data?.error) {
      return `Search error: ${error.response.data.error}`;
    }
  }
  
  return "Sorry, there was an error starting your search. Please try again.";
};

export const handleSubmitError = (error: unknown): string => {
  console.error('Error submitting search:', error);
  
  if (axios.isAxiosError(error)) {
    console.error('Search error response:', error.response?.data);
    console.error('Search error status:', error.response?.status);
    
    if (error.response?.data?.error) {
      return `Search error: ${error.response.data.error}`;
    }
  }
  
  return "Error processing your search. Please try again.";
};
