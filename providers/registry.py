from typing import Dict, Any, Optional
import os

PROVIDERS = {
    "openai": {"name": "OpenAI", "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"], "env": "OPENAI_API_KEY"},
    "anthropic": {"name": "Anthropic", "models": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229"], "env": "ANTHROPIC_API_KEY"},
    "google": {"name": "Google Gemini", "models": ["gemini-1.5-pro", "gemini-1.5-flash"], "env": "GOOGLE_API_KEY"},
    "groq": {"name": "Groq", "models": ["llama-3.1-70b-versatile", "mixtral-8x7b-32768"], "env": "GROQ_API_KEY"},
    "together": {"name": "Together AI", "models": ["meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"], "env": "TOGETHER_API_KEY"},
    "fireworks": {"name": "Fireworks", "models": ["accounts/fireworks/models/llama-v3p1-70b-instruct"], "env": "FIREWORKS_API_KEY"},
    "mistral": {"name": "Mistral", "models": ["mistral-large-latest", "mistral-medium"], "env": "MISTRAL_API_KEY"},
    "cohere": {"name": "Cohere", "models": ["command-r-plus"], "env": "COHERE_API_KEY"},
    "perplexity": {"name": "Perplexity", "models": ["llama-3.1-sonar-large-128k-online"], "env": "PERPLEXITY_API_KEY"},
    "deepseek": {"name": "DeepSeek", "models": ["deepseek-chat", "deepseek-coder"], "env": "DEEPSEEK_API_KEY"},
    "xai": {"name": "xAI Grok", "models": ["grok-beta", "grok-2"], "env": "XAI_API_KEY"},
    "azure": {"name": "Azure OpenAI", "models": ["gpt-4o"], "env": "AZURE_OPENAI_API_KEY"},
    "ollama": {"name": "Ollama (local)", "models": ["llama3.1", "mistral"], "env": None},
}

def get_provider(name: str) -> Optional[Dict[str, Any]]:
    return PROVIDERS.get(name.lower())

def list_providers() -> Dict[str, Any]:
    return PROVIDERS
