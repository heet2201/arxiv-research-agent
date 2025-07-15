# ArXiv Research Agent 🔬

An enhanced autonomous research agent that searches multiple academic sources, extracts visual content from papers, and provides comprehensive analysis using AI. Built with real-time streaming updates and a beautiful Gradio interface.

## ✨ Features

### 🚀 **Multi-Source Academic Search**
- **ArXiv**: Advanced search with multiple strategies
- **Google Scholar**: Via Serper.dev API integration
- **Semantic Scholar**: Direct API access
- **CrossRef**: Academic paper database
- **Smart deduplication** across sources

### 📊 **Visual Content Extraction**
- Automatically extracts **charts, graphs, and diagrams** from PDFs
- **Table detection** and text extraction
- **Figure captions** and contextual information
- Base64 encoding for visual data preservation

### 🤖 **AI-Powered Analysis**
- **Claude Sonnet 4** integration for deep paper analysis
- **Contextual follow-up** question handling
- **Quantitative results** extraction
- **Methodology identification**
- **Research trend analysis**

### 🎯 **Real-Time Interface**
- **Live streaming updates** during execution
- **Step-by-step progress** tracking
- **Beautiful Gradio interface**
- **Example queries** for quick start
- **Conversation context** maintenance

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/arxiv-research-agent.git
cd arxiv-research-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional but recommended)
export OPENROUTER_API_KEY="your-openrouter-key"
export SERPER_API_KEY="your-serper-key"  # Optional
export SEMANTIC_SCHOLAR_API_KEY="your-semantic-scholar-key"  # Optional

# Run the application
python main.py
```

### Using pip (when published)
```bash
pip install arxiv-research-agent
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file or set these environment variables:

```bash
# Required
OPENROUTER_API_KEY=your-openrouter-api-key-here

# Optional (for enhanced search)
SERPER_API_KEY=your-serper-api-key-here
SEMANTIC_SCHOLAR_API_KEY=your-semantic-scholar-key-here
```

### API Keys Setup

1. **OpenRouter API** (Required)
   - Sign up at [OpenRouter](https://openrouter.ai/)
   - Get your API key from the dashboard
   - Provides access to Claude Sonnet 4

2. **Serper.dev API** (Optional)
   - Sign up at [Serper.dev](https://serper.dev/)
   - Get 2,500 free searches per month
   - Enables Google Scholar integration

3. **Semantic Scholar** (Optional)
   - Register at [Semantic Scholar API](https://www.semanticscholar.org/product/api)
   - Free tier available
   - Enhanced academic search capabilities

## 🚀 Usage

### Web Interface
1. Run `python main.py`
2. Open your browser to `http://localhost:7861`
3. Enter your research query
4. Watch the agent work in real-time!

### Example Queries
- "latest research on transformer architectures"
- "quantum computing applications in machine learning"
- "computer vision for medical imaging"
- "reinforcement learning in robotics"
- "attention mechanisms in neural networks"

### Programmatic Usage
```python
from src.arxiv_agent.core.agent import AutonomousResearchAgent
from config.config import Config

# Initialize agent
config = Config()
agent = AutonomousResearchAgent(config)

# Process a query
for response, steps in agent.process_query_streaming("your research query"):
    print(f"Response: {response}")
    print(f"Steps: {steps}")
```

## 📁 Project Structure

```
arxiv-research-agent/
├── src/
│   └── arxiv_agent/
│       ├── core/
│       │   ├── models.py          # Data models and enums
│       │   └── agent.py           # Main agent logic
│       ├── search/
│       │   ├── base_search.py     # Base search functionality
│       │   └── enhanced_search.py # Multi-source search engine
│       ├── analysis/
│       │   ├── query_analyzer.py  # Query intent analysis
│       │   └── visual_extractor.py # PDF visual extraction
│       └── ui/
│           └── gradio_interface.py # Web interface
├── config/
│   └── config.py                  # Configuration management
├── docs/                          # Documentation
├── examples/                      # Example scripts
├── tests/                         # Unit tests
├── main.py                        # Entry point
├── requirements.txt               # Dependencies
├── setup.py                       # Package setup
└── README.md                      # This file
```

## 🔍 How It Works

### 1. **Query Analysis**
- Analyzes user intent (search, analyze, compare)
- Determines query complexity
- Handles follow-up questions with context

### 2. **Multi-Source Search**
- Searches ArXiv using multiple strategies
- Integrates Google Scholar via Serper API
- Queries Semantic Scholar and CrossRef
- Deduplicates and ranks results by relevance

### 3. **Visual Content Extraction**
- Downloads paper PDFs from ArXiv
- Extracts images, charts, and diagrams
- Identifies tables and structured data
- Captures figure captions and context

### 4. **AI Analysis**
- Uses Claude Sonnet 4 for deep analysis
- Extracts key findings and methodologies
- Identifies quantitative results
- Summarizes research trends

### 5. **Response Synthesis**
- Combines insights from all sources
- Provides structured, comprehensive reports
- Maintains conversation context
- Offers actionable next steps

## 🎛️ Configuration Options

### `config/config.py`
```python
class Config:
    # API Configuration
    OPENROUTER_API_KEY: str
    SERPER_API_KEY: Optional[str]
    SEMANTIC_SCHOLAR_API_KEY: Optional[str]
    
    # Model Configuration
    LLM_MODEL: str = "anthropic/claude-sonnet-4"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 5000
    
    # Search Configuration
    MAX_SEARCH_RESULTS: int = 20
    MAX_VISUAL_EXTRACTIONS: int = 3
    MAX_PAPERS_FOR_ANALYSIS: int = 3
    
    # UI Configuration
    GRADIO_SERVER_PORT: int = 7861
    GRADIO_SHARE: bool = True
```

## 🧪 Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Code formatting
black src/
isort src/

# Linting
flake8 src/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/arxiv-research-agent.git
cd arxiv-research-agent

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ArXiv** for providing open access to research papers
- **OpenRouter** for LLM API access
- **Serper.dev** for Google search integration
- **Semantic Scholar** for academic search API
- **Gradio** for the beautiful web interface
- **PyMuPDF** for PDF processing capabilities

## 🐛 Issues and Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/arxiv-research-agent/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/arxiv-research-agent/discussions)
- 📧 **Email**: heetshah221@gmail.com

---

**Built with ❤️ for the research community by Heet Shah** 