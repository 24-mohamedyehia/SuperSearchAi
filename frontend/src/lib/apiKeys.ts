export type LLMProvider = "openrouter" | "ollama";

export const providerLabels: Record<LLMProvider, string> = {
  openrouter: "OpenRouter",
  ollama: "Ollama",
};

export const defaultModels: Record<LLMProvider, string> = {
  openrouter: "deepseek/deepseek-r1-0528:free",
  ollama: "llama3.2",
};

export const defaultBaseUrls: Record<LLMProvider, string> = {
  openrouter: "",
  ollama: "http://localhost:11434",
};

export const defaultApiKeys: Record<LLMProvider, string | null> = {
  openrouter: "",
  ollama: "null",
};

export function getApiKey(provider: LLMProvider): string | null {
  return localStorage.getItem(`apiKey_${provider}`) || defaultApiKeys[provider];
}

export function setApiKey(provider: LLMProvider, apiKey: string): void {
  localStorage.setItem(`apiKey_${provider}`, apiKey);
}

export function deleteApiKey(provider: LLMProvider): void {
  localStorage.removeItem(`apiKey_${provider}`);
}

export function getModel(provider: LLMProvider): string {
  return localStorage.getItem(`model_${provider}`) || defaultModels[provider];
}

export function setModel(provider: LLMProvider, model: string): void {
  localStorage.setItem(`model_${provider}`, model);
}

export function getBaseUrl(provider: LLMProvider): string {
  return localStorage.getItem(`baseUrl_${provider}`) || defaultBaseUrls[provider];
}

export function setBaseUrl(provider: LLMProvider, baseUrl: string): void {
  localStorage.setItem(`baseUrl_${provider}`, baseUrl);
}

export function hasApiKey(provider: LLMProvider): boolean {
  const key = getApiKey(provider);
  return key !== null && key.trim() !== "";
}

export function getAllApiKeys(): Record<LLMProvider, string | null> {
  const keys = {} as Record<LLMProvider, string | null>;
  Object.keys(providerLabels).forEach(provider => {
    keys[provider as LLMProvider] = getApiKey(provider as LLMProvider);
  });
  return keys;
}
