# Free LLM Setup Guide

This guide shows you how to use free and open-source LLMs with the SQL to MongoDB translator instead of OpenAI.

## 🆓 Option 1: Ollama (Recommended - Local LLMs)

Ollama allows you to run LLMs locally on your machine for free.

### Installation

1. **Install Ollama**:
   ```bash
   # On Linux/macOS
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # On Windows
   # Download from https://ollama.ai/download
   ```

2. **Pull a model**:
   ```bash
   # Pull Llama 2 (7B parameters, ~4GB)
   ollama pull llama2
   
   # Or try other models:
   ollama pull mistral    # Smaller, faster
   ollama pull codellama  # Good for code
   ollama pull phi2       # Very small, fast
   ```

3. **Start Ollama**:
   ```bash
   ollama serve
   ```

4. **Test the model**:
   ```bash
   ollama run llama2 "Hello, how are you?"
   ```

### Usage with the Application

The application will automatically detect if Ollama is available and use it instead of OpenAI. No additional configuration needed!

## 🆓 Option 2: Hugging Face Inference API (Free Tier)

Some models have free inference endpoints.

### Setup

1. **Get a Hugging Face token**:
   - Go to https://huggingface.co/
   - Create an account
   - Go to Settings → Access Tokens
   - Create a new token

2. **Add to .env file**:
   ```bash
   echo "HUGGINGFACE_API_KEY=your_token_here" >> .env
   ```

3. **Update the agent** (if needed):
   ```python
   from langchain_community.llms import HuggingFaceHub
   
   llm = HuggingFaceHub(
       repo_id="google/flan-t5-base",
       huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY")
   )
   ```

## 🆓 Option 3: Local Models with Transformers

Run models directly with the transformers library.

### Installation

```bash
pip install transformers torch
```

### Usage

```python
from transformers import pipeline

# Load a small model
generator = pipeline('text-generation', model='gpt2')

# Use in your application
response = generator("Translate this SQL query", max_length=100)
```

## 🔧 Current Implementation

The application now supports:

1. **OpenAI** (if API key is provided)
2. **Ollama** (automatic fallback)
3. **Fallback LLM** (rule-based explanations if nothing else works)

### How it works:

```python
# The agent automatically chooses the best available option:
if openai_api_key:
    agent = SQLToMongoDBAgent(llm_type="openai", openai_api_key=openai_api_key)
else:
    agent = SQLToMongoDBAgent(llm_type="ollama", model_name="llama2")
```

## 🚀 Quick Start with Ollama

1. **Install Ollama**:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Pull a model**:
   ```bash
   ollama pull llama2
   ```

3. **Start Ollama**:
   ```bash
   ollama serve
   ```

4. **Run the application**:
   ```bash
   python run_webapp.py
   ```

5. **Test the "Explain Translation" button** - it should now work without any API costs!

## 📊 Model Comparison

| Model | Size | Speed | Quality | Setup |
|-------|------|-------|---------|-------|
| Llama 2 | ~4GB | Medium | Good | Easy |
| Mistral | ~4GB | Fast | Good | Easy |
| CodeLlama | ~7GB | Medium | Excellent | Easy |
| Phi-2 | ~1.4GB | Very Fast | Good | Easy |
| GPT-2 | ~500MB | Very Fast | Basic | Easy |

## 🛠️ Troubleshooting

### Ollama Issues

1. **"Connection refused"**:
   ```bash
   ollama serve
   ```

2. **"Model not found"**:
   ```bash
   ollama pull llama2
   ```

3. **Out of memory**:
   - Try a smaller model: `ollama pull phi2`
   - Or use quantization: `ollama pull llama2:7b-q4_0`

### Performance Tips

1. **Use smaller models** for faster responses
2. **Use quantization** to reduce memory usage
3. **Run Ollama in background** for better performance

## 🎯 Benefits of Free LLMs

- ✅ **No API costs**
- ✅ **No rate limits**
- ✅ **Privacy** (runs locally)
- ✅ **Always available**
- ✅ **Customizable**

The application will now work completely offline with free local LLMs! 