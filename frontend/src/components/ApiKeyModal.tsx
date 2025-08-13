import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "./ui/dialog";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Key } from "lucide-react";
import type { LLMProvider } from "@/lib/apiKeys";
import { providerLabels } from "@/lib/apiKeys";

interface ApiKeyModalProps {
  isOpen: boolean;
  onClose: () => void;
  provider: LLMProvider;
  onSave: () => void;
}

export function ApiKeyModal({
  isOpen,
  onClose,
  provider,
  onSave,
}: ApiKeyModalProps) {
  const [apiKey, setApiKey] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      // Load existing API key from localStorage
      const existingKey = localStorage.getItem(`apiKey_${provider}`);
      if (existingKey) {
        setApiKey(existingKey);
      }
    }
  }, [isOpen, provider]);

  const handleSave = async () => {
    if (!apiKey.trim()) return;

    setIsLoading(true);
    try {
      // Save to localStorage
      localStorage.setItem(`apiKey_${provider}`, apiKey.trim());
      onSave();
      onClose();
    } catch (error) {
      console.error("Error saving API key:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    setApiKey("");
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Key className="h-5 w-5" />
            {providerLabels[provider]} API Key
          </DialogTitle>
          <DialogDescription>
            Enter your API key for {providerLabels[provider]}. This will be
            stored securely in your browser.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="apiKey">API Key</Label>
            <Input
              id="apiKey"
              type="password"
              placeholder="Enter your API key..."
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSave();
                }
              }}
            />
          </div>
          <div className="flex justify-end space-x-2">
            <Button variant="outline" onClick={handleClose}>
              Cancel
            </Button>
            <Button onClick={handleSave} disabled={!apiKey.trim() || isLoading}>
              {isLoading ? "Saving..." : "Save"}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
