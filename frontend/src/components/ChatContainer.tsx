import { useEffect, useRef } from "react";
import { ChatMessage, type ChatMessage as ChatMessageType } from "./ChatMessage";
import { Button } from "./ui/button";
import { cn } from "@/lib/utils";
import { Bot, Send } from "lucide-react";

interface ChatContainerProps {
  messages: ChatMessageType[];
  onChoiceSelect?: (messageId: string, choice: string) => void;
  showSubmitButton?: boolean;
  onSubmitAnswers?: () => void;
  isLoading?: boolean;
  className?: string;
}

export function ChatContainer({ 
  messages, 
  onChoiceSelect, 
  showSubmitButton = false,
  onSubmitAnswers,
  isLoading = false,
  className 
}: ChatContainerProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className={cn("flex-1 overflow-y-auto p-6 bg-white", className)}>
      <div className="max-w-4xl mx-auto">
        {messages.length === 0 ? (
          <div className="text-center py-20">
            <div className="max-w-md mx-auto space-y-6">
              <div className="w-20 h-20 bg-primary-600 rounded-2xl flex items-center justify-center mx-auto shadow-lg">
                <Bot className="h-10 w-10 text-secondary" />
              </div>
              <div className="space-y-3">
                <h3 className="text-2xl font-bold text-gray-900">
                  Welcome to Super Search AI
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  Ask me anything and I'll search the web intelligently. 
                </p>
              </div>
              <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                <p className="text-sm text-blue-800">
                  💡 <strong>Tip:</strong> Be specific with your queries for better results
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={message}
                onChoiceSelect={onChoiceSelect}
              />
            ))}
            
            {/* Submit Button */}
            {showSubmitButton && (
              <div className="flex justify-center py-6">
                <Button
                  onClick={onSubmitAnswers}
                  disabled={isLoading}
                  size="lg"
                >
                  <Send className="h-4 w-4 mr-2" />
                  {isLoading ? "Processing..." : "Submit Answers"}
                </Button>
              </div>
            )}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
