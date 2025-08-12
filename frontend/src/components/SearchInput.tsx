import { useState, useRef, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Search, Settings } from "lucide-react";
import { cn } from "@/lib/utils";
import type { LLMProvider } from "@/lib/apiKeys";
import { providerLabels, hasApiKey } from "@/lib/apiKeys";

export type SearchMode = "quick" | "deep";

interface SearchInputProps {
  onSearch: (query: string, provider: LLMProvider, mode: SearchMode) => void;
  onProviderChange: (provider: LLMProvider) => void;
  onOpenApiKeyModal: () => void;
  isLoading?: boolean;
  className?: string;
}

export function SearchInput({
  onSearch,
  onProviderChange,
  onOpenApiKeyModal,
  isLoading = false,
  className,
}: SearchInputProps) {
  const [query, setQuery] = useState("");
  const [provider, setProvider] = useState<LLMProvider>("openrouter");
  const [mode, setMode] = useState<SearchMode>("quick");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    onProviderChange(provider);
  }, [provider, onProviderChange]);

  const handleSubmit = () => {
    if (!query.trim()) return;

    // Check if API key exists for selected provider
    if (!hasApiKey(provider)) {
      onOpenApiKeyModal();
      return;
    }

    onSearch(query.trim(), provider, mode);

    // Clear the input after submission
    setQuery("");
  };

  return (
    <div className={cn("w-full bg-white max-w-5xl mx-auto flex items-center justify-between gap-1", className)}>
      {/* Provider and Mode Selection Tabs */}
      <div className="mb-3 flex items-center justify-between">
        {/* Provider Tabs */}
        <div className="flex-col items-center gap-1 bg-neutral-100 rounded-md p-1">
          {Object.entries(providerLabels).map(([key, label]) => (
            <button
              key={key}
              onClick={() => setProvider(key as LLMProvider)}
              disabled={isLoading}
              className={cn(
                "px-3 py-1.5 w-full rounded-md text-sm font-medium transition-all duration-200 flex items-center gap-1.5",
                provider === key
                  ? "bg-white text-primary shadow-sm"
                  : "text-neutral-600 hover:text-neutral-800 hover:bg-neutral-100"
              )}
            >
              <span>{label}</span>
              {!hasApiKey(key as LLMProvider) && (
                <Settings className="h-3 w-3 text-warning" />
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Search Input */}
      <div className="bg-white border w-full  shadow-sm p-4">
        <div className="flex items-center gap-3">
          {/* Main search input */}
          <div className="flex-1 relative">
            <Input
              ref={inputRef}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit();
                }
              }}
              placeholder="Ask me anything... "
              className="h-12 text-base border-0 bg-transparent focus-visible:ring-0  placeholder:text-gray-400 shadow-none"
              disabled={isLoading}
            />
          </div>

          {/* Search button */}
          <Button onClick={handleSubmit} disabled={!query.trim() || isLoading}>
            <Search className="h-4 w-4 mr-2" />
            {isLoading ? "Searching..." : "Search"}
          </Button>
        </div>
      </div>
      <div className="mb-3 flex items-center justify-between">
        {/* Mode Tabs */}
        <div className="flex-col items-center gap-1 bg-neutral-100 rounded-md p-1">
          <button
            onClick={() => setMode("quick")}
            disabled={isLoading}
            className={cn(
              "px-3  py-1.5 w-full rounded-md text-sm font-medium transition-all duration-200 flex items-center gap-2",
              mode === "quick"
                ? "bg-white text-primary shadow-sm"
                : "text-neutral-600 hover:text-neutral-800 hover:bg-neutral-200"
            )}
          >
            Quick
          </button>
          <button
            onClick={() => setMode("deep")}
            disabled={isLoading}
            className={cn(
              "px-3 py-1.5 rounded-md w-full text-sm font-medium transition-all duration-200 flex items-center gap-2",
              mode === "deep"
                ? "bg-white text-primary shadow-sm"
                : "text-neutral-600 hover:text-neutral-800 hover:bg-neutral-200"
            )}
          >
            Deep
          </button>
        </div>
      </div>
    </div>
  );
}
