import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { cn } from "@/lib/utils";
import { User, Bot, CheckCircle } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { LoadingMessage } from "./LoadingMessage";

export type MessageType =
  | "user"
  | "system"
  | "question"
  | "answer"
  | "result"
  | "loading";

export interface ChatMessage {
  id: string;
  type: MessageType;
  content: string;
  timestamp: Date;
  choices?: string[];
  selectedChoice?: string;
  data?: Record<string, unknown>;
}

interface ChatMessageProps {
  message: ChatMessage;
  onChoiceSelect?: (messageId: string, choice: string) => void;
  className?: string;
}

export function ChatMessage({
  message,
  onChoiceSelect,
  className,
}: ChatMessageProps) {
  const isUser = message.type === "user";
  const isSystem = message.type === "system";
  const isQuestion = message.type === "question";
  const isAnswer = message.type === "answer";
  const isResult = message.type === "result";
  const isLoading = message.type === "loading";

  // Handle loading messages with special component
  if (isLoading) {
    return <LoadingMessage message={message.content} className={className} />;
  }

  const getIcon = () => {
    if (isUser) return <User className="h-4 w-4" />;
    if (isSystem || isQuestion) return <Bot className="h-4 w-4" />;
    if (isAnswer) return <CheckCircle className="h-4 w-4 text-success" />;
    return <Bot className="h-4 w-4" />;
  };

  const getAlignment = () => {
    return isUser ? "flex-row-reverse" : "flex-row";
  };

  const getMessageStyles = () => {
    if (isUser) {
      return "bg-secondary text-white ml-16 shadow-sm";
    }
    if (isSystem) {
      return "bg-surface-50 border border-surface-300 mr-16 shadow-sm";
    }
    if (isQuestion) {
      return "bg-primary-50 border border-primary-200 mr-16 shadow-sm";
    }
    if (isAnswer) {
      return "bg-success-50 border border-success-200 mr-16 shadow-sm";
    }
    if (isResult) {
      return "bg-transparent border-0 mr-0 p-0";
    }
    return "bg-surface-50 border border-surface-300 mr-16 shadow-sm";
  };

  const renderResultMarkdown = () => {
    if (isResult && message.content) {
      const images = (message.data?.images as string[]) || [];
      const resourcesRaw = message.data?.resources;
      let resources: Array<{ title: string; url: string }> = [];
      if (Array.isArray(resourcesRaw) && resourcesRaw.length > 0) {
        if (typeof resourcesRaw[0] === "string") {
          resources = (resourcesRaw as string[]).map((url) => ({
            title: "Link",
            url,
          }));
        } else {
          resources = resourcesRaw as Array<{ title: string; url: string }>;
        }
      }
      return (
        <div className="prose prose-sm max-w-none bg-primary-50 rounded-xl p-6 border border-primary-200 text-sm leading-7 text-neutral-800">
          {/* Markdown Report */}
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              h1: ({ children }) => (
                <h1 className="text-lg font-bold mb-4 text-neutral-900">
                  {children}
                </h1>
              ),
              h2: ({ children }) => (
                <h2 className="text-md font-semibold mb-3 text-neutral-900">
                  {children}
                </h2>
              ),
              h3: ({ children }) => (
                <h3 className="text-sm font-semibold mb-2 text-neutral-900">
                  {children}
                </h3>
              ),
              p: ({ children }) => <p className="mb-3 last:mb-0">{children}</p>,
              strong: ({ children }) => <strong>{children}</strong>,
              em: ({ children }) => <em>{children}</em>,
              ul: ({ children }) => (
                <ul className="list-disc list-inside mb-3 space-y-1">
                  {children}
                </ul>
              ),
              ol: ({ children }) => (
                <ol className="list-decimal list-inside mb-3 space-y-1">
                  {children}
                </ol>
              ),
              li: ({ children }) => <li>{children}</li>,
              blockquote: ({ children }) => (
                <blockquote className="border-l-4 border-primary-300 pl-4 italic bg-primary-25 py-2 my-3 rounded-r">
                  {children}
                </blockquote>
              ),
              code: ({ children }) => (
                <code className="bg-neutral-100 px-1 py-0.5 rounded text-xs font-mono">
                  {children}
                </code>
              ),
              pre: ({ children }) => (
                <pre className="bg-neutral-100 p-3 rounded-lg overflow-x-auto text-xs font-mono my-3">
                  {children}
                </pre>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>

          {/* Images Section */}
          {images.length > 0 && (
            <div className="mt-6">
              <div className="flex items-center gap-3 text-sm font-semibold text-neutral-900 mb-2">
                <span className="h-6 w-6 rounded-full bg-warning flex items-center justify-center mr-2">
                  🖼️
                </span>
                Related Images ({images.length})
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                {images.slice(0, 8).map((image, index) => (
                  <div
                    key={index}
                    className="relative aspect-square bg-surface-100 rounded-xl overflow-hidden cursor-pointer hover:scale-105 transition-transform group ring-2 ring-transparent hover:ring-primary-200"
                  >
                    <img
                      src={image}
                      alt={`Related image ${index + 1}`}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        (
                          e.target as HTMLImageElement
                        ).parentElement!.style.display = "none";
                      }}
                    />
                  </div>
                ))}
                {images.length > 8 && (
                  <div className="aspect-square bg-gray-100 rounded-xl flex items-center justify-center cursor-pointer hover:scale-105 transition-transform ring-2 ring-transparent hover:ring-primary-200">
                    <div className="text-center text-sm text-neutral-600">
                      <span className="text-2xl">+{images.length - 8}</span>
                      <div>more</div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Resources Section */}
          {resources.length > 0 && (
            <div className="mt-6">
              <div className="flex items-center gap-3 text-sm font-semibold text-neutral-900 mb-2">
                <span className="h-6 w-6 rounded-full bg-success flex items-center justify-center mr-2">
                  🔗
                </span>
                Sources ({resources.length})
              </div>
              <div className="grid gap-3">
                {resources.map((resource, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-4 p-4 bg-surface-100 rounded-xl hover:bg-surface-200 transition-all group border border-surface-300 hover:border-surface-400"
                  >
                    <div className="flex-1 min-w-0">
                      <a
                        href={resource.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm font-semibold text-primary hover:text-primary-700 transition-colors line-clamp-1 group-hover:underline"
                      >
                        {resource.title}
                      </a>
                      <p className="text-xs text-neutral-500 mt-1 line-clamp-1">
                        {(() => {
                          try {
                            return new URL(resource.url).hostname;
                          } catch {
                            return resource.url;
                          }
                        })()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className={cn("flex gap-4 mb-6", getAlignment(), className)}>
      <div className="flex-shrink-0 w-9 h-9 rounded-full bg-surface-50 border-2 border-surface-300 flex items-center justify-center shadow-sm">
        {getIcon()}
      </div>
      <div className="flex-1 min-w-0">
        {isResult ? (
          // For comprehensive results, render without the card wrapper
          <div>
            {renderResultMarkdown()}
            <div className="text-xs text-neutral-500 mt-3 px-1">
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        ) : (
          <>
            <Card className={cn("", getMessageStyles())}>
              <CardContent className="p-4">
                <div className="prose prose-sm max-w-none">
                  <p className="whitespace-pre-wrap m-0 text-sm leading-relaxed">
                    {message.content}
                  </p>
                </div>

                {/* Render choices for questions */}
                {isQuestion &&
                  message.choices &&
                  message.choices.length > 0 && (
                    <div className="mt-4 space-y-2">
                      {message.choices.map((choice, index) => (
                        <Button
                          key={index}
                          variant={
                            message.selectedChoice === choice
                              ? "default"
                              : "outline"
                          }
                          size="sm"
                          onClick={() => onChoiceSelect?.(message.id, choice)}
                          disabled={message.selectedChoice !== undefined}
                          className="w-full justify-start text-left transition-all duration-200 hover:shadow-sm"
                        >
                          {choice}
                        </Button>
                      ))}
                      {/*  Skip option */}
                      <Button
                        variant={
                          message.selectedChoice === "Skip"
                            ? "secondary"
                            : "ghost"
                        }
                        size="sm"
                        onClick={() => onChoiceSelect?.(message.id, "Skip")}
                        disabled={message.selectedChoice !== undefined}
                        className="w-full justify-start text-left text-neutral-500 hover:text-neutral-700 transition-colors duration-200"
                      >
                        Skip this question
                      </Button>
                    </div>
                  )}

                {/* No result card here; handled in result branch */}
              </CardContent>
            </Card>
            <div className="text-xs text-neutral-500 mt-2 px-1">
              {message.timestamp.toLocaleTimeString()}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
