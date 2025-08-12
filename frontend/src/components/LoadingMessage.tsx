import { Card, CardContent } from "./ui/card";
import { Bot, Search, Brain, Globe } from "lucide-react";
import { cn } from "@/lib/utils";

interface LoadingMessageProps {
  message: string;
  className?: string;
}

export function LoadingMessage({ message, className }: LoadingMessageProps) {
  // Choose icon based on message content
  const getIcon = () => {
    if (message.toLowerCase().includes('analyzing') || message.toLowerCase().includes('clarification')) {
      return <Brain className="h-4 w-4" />;
    }
    if (message.toLowerCase().includes('searching') || message.toLowerCase().includes('web')) {
      return <Globe className="h-4 w-4" />;
    }
    if (message.toLowerCase().includes('processing')) {
      return <Search className="h-4 w-4" />;
    }
    return <Bot className="h-4 w-4" />;
  };

  return (
    <div className={cn("flex gap-4 mb-6", className)}>
      <div className="flex-shrink-0 w-9 h-9 rounded-full bg-surface-50 border-2 border-surface-300 flex items-center justify-center shadow-sm">
        {getIcon()}
      </div>
      <div className="flex-1 min-w-0">
        <Card className="bg-blue-50 border-blue-200 mr-16 shadow-sm">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-secondary rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-secondary rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-secondary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
              <span className="text-sm text-primary-800 font-medium">{message}</span>
            </div>
          </CardContent>
        </Card>
        <div className="text-xs text-gray-500 mt-2 px-1">
          {new Date().toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}
