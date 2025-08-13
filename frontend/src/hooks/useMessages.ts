import { useState, useCallback } from 'react';
import type { ChatMessage } from '@/components/ChatMessage';

export const useMessages = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const addMessage = useCallback((message: Omit<ChatMessage, 'id' | 'timestamp'>) => {
    const newMessage: ChatMessage = {
      ...message,
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
    return newMessage.id;
  }, []);

  const updateMessage = useCallback((messageId: string, updates: Partial<ChatMessage>) => {
    setMessages(prev => 
      prev.map(msg => 
        msg.id === messageId ? { ...msg, ...updates } : msg
      )
    );
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  const findMessage = useCallback((messageId: string) => {
    return messages.find(msg => msg.id === messageId);
  }, [messages]);

  const removeMessage = useCallback((messageId: string) => {
    setMessages(prev => prev.filter(msg => msg.id !== messageId));
  }, []);

  const getUserQuery = useCallback(() => {
    return messages.find(msg => msg.type === "user")?.content || "";
  }, [messages]);

  return {
    messages,
    addMessage,
    updateMessage,
    removeMessage,
    clearMessages,
    findMessage,
    getUserQuery,
  };
};
