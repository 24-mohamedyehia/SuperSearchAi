import { useState } from "react";
import { ProgressSteps } from "./components/ProgressSteps";
import { SearchInput } from "./components/SearchInput";
import { ChatContainer } from "./components/ChatContainer";
import { ApiKeyModal } from "./components/ApiKeyModal";
import SettingsModal from "./components/SettingsModal";
import type { LLMProvider } from "./lib/apiKeys";
import type { SearchMode } from "./components/SearchInput";
import { Button } from "./components/ui/button";
import { Settings } from "lucide-react";
import { useSearchFlow } from "./hooks/useSearchFlow";

function App() {
  const [selectedProvider, setSelectedProvider] =
    useState<LLMProvider>("openrouter");
  const [isApiKeyModalOpen, setIsApiKeyModalOpen] = useState(false);
  const [isSettingsModalOpen, setIsSettingsModalOpen] = useState(false);

  const {
    currentStep,
    isLoading,
    messages,
    showSubmitButton,
    startSearchFlow,
    handleChoiceSelect,
    submitAnswers,
  } = useSearchFlow();

  const handleSearch = async (
    query: string,
    provider: LLMProvider,
    mode: SearchMode
  ) => {
    try {
      await startSearchFlow(query, provider, mode);
    } catch (error) {
      if (error instanceof Error && error.message === "API_KEY_MISSING") {
        setIsApiKeyModalOpen(true);
      }
    }
  };

  const handleApiKeySave = () => {
    // API key is already saved in the modal component
  };

  return (
    <div className="min-h-screen bg-surface flex flex-col">
      {/* Settings Button - Fixed position */}
      <div className="fixed top-4 right-4 z-50">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsSettingsModalOpen(true)}
          className="shadow-sm border-surface-300 bg-surface-50 hover:bg-surface-100 transition-all duration-200"
          title="Settings"
        >
          <Settings className="h-4 w-4" />
        </Button>
      </div>

      {/* Progress Steps */}
      <ProgressSteps currentStep={currentStep} />

      {/* Chat Container */}
      <div className="flex-1 overflow-hidden">
        <ChatContainer
          messages={messages}
          onChoiceSelect={handleChoiceSelect}
          showSubmitButton={showSubmitButton}
          onSubmitAnswers={submitAnswers}
          isLoading={isLoading}
          className="h-full"
        />
      </div>

      {/* Search Input */}
      <div className="sticky bottom-0 w-full p-3">
        <SearchInput
          onSearch={handleSearch}
          onProviderChange={setSelectedProvider}
          onOpenApiKeyModal={() => setIsApiKeyModalOpen(true)}
          isLoading={isLoading}
        />
      </div>

      {/* API Key Modal */}
      <ApiKeyModal
        isOpen={isApiKeyModalOpen}
        onClose={() => setIsApiKeyModalOpen(false)}
        provider={selectedProvider}
        onSave={handleApiKeySave}
      />

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsModalOpen}
        onClose={() => setIsSettingsModalOpen(false)}
      />
    </div>
  );
}

export default App;
