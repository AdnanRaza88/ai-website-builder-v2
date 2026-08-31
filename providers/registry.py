from typing import Dict, Any, Optional, List

PROVIDERS: Dict[str, Dict[str, Any]] = {
    "openai": {"name": "OpenAI", "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "o1-mini"], "env": "OPENAI_API_KEY"},
    "anthropic": {"name": "Anthropic", "models": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"], "env": "ANTHROPIC_API_KEY"},
    "google": {"name": "Google Gemini", "models": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash"], "env": "GOOGLE_API_KEY"},
    "groq": {"name": "Groq", "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"], "env": "GROQ_API_KEY"},
    "xai": {"name": "xAI Grok", "models": ["grok-2", "grok-beta", "grok-2-mini"], "env": "XAI_API_KEY"},
    "deepseek": {"name": "DeepSeek", "models": ["deepseek-chat", "deepseek-coder"], "env": "DEEPSEEK_API_KEY"},
    "mistral": {"name": "Mistral", "models": ["mistral-large-latest", "mistral-medium", "mistral-small"], "env": "MISTRAL_API_KEY"},
    "together": {"name": "Together AI", "models": ["meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"], "env": "TOGETHER_API_KEY"},
    "fireworks": {"name": "Fireworks", "models": ["accounts/fireworks/models/llama-v3p1-70b-instruct"], "env": "FIREWORKS_API_KEY"},
    "perplexity": {"name": "Perplexity", "models": ["llama-3.1-sonar-large-128k-online"], "env": "PERPLEXITY_API_KEY"},
    "cohere": {"name": "Cohere", "models": ["command-r-plus", "command-r"], "env": "COHERE_API_KEY"},
    "ollama": {"name": "Ollama (local)", "models": ["llama3.1", "mistral", "codellama"], "env": None},
}

def list_providers() -> Dict[str, Dict[str, Any]]:
    return PROVIDERS

def get_provider(name: str) -> Optional[Dict[str, Any]]:
    return PROVIDERS.get(name.lower())

def list_models(provider_id: str) -> List[str]:
    p = get_provider(provider_id)
    return p["models"] if p else []
