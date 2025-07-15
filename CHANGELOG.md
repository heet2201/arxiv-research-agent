# Changelog

All notable changes to the ArXiv Research Agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-15

### Added
- **Multi-Source Academic Search**: Integration with ArXiv, Google Scholar (via Serper), Semantic Scholar, and CrossRef
- **Visual Content Extraction**: Automatic extraction of charts, tables, and diagrams from research papers
- **AI-Powered Analysis**: Claude Sonnet 4 integration for deep paper analysis
- **Real-Time Streaming Interface**: Live updates during execution with Gradio
- **Query Analysis**: Intent detection and complexity analysis for user queries
- **Conversation Context**: Follow-up question handling with context maintenance
- **Modular Architecture**: Clean separation of concerns with proper Python packaging
- **Comprehensive Documentation**: README, examples, and API documentation
- **Test Suite**: Unit tests and integration tests for core functionality
- **Configuration Management**: Environment-based configuration with sensible defaults

### Features
- Search multiple academic sources simultaneously
- Extract visual content from PDF papers
- Real-time progress tracking and streaming updates
- Contextual follow-up question support
- Relevance scoring and result ranking
- Beautiful web interface with example queries
- Programmatic API for integration
- Docker support for easy deployment
- Comprehensive error handling and logging

### Technical Details
- **Backend**: Python 3.8+ with modern async/await patterns
- **UI**: Gradio for beautiful, responsive web interface
- **AI Integration**: OpenRouter API for Claude Sonnet 4 access
- **PDF Processing**: PyMuPDF for robust document parsing
- **Search**: TF-IDF vectorization for relevance scoring
- **Architecture**: Modular design with clear separation of concerns

## [Unreleased]

### Planned Features
- Database integration for paper storage and indexing
- Citation graph analysis and visualization
- Enhanced visual content types (equations, flowcharts)
- Export functionality (PDF, Word reports)
- Collaborative workspaces
- Mobile-responsive interface improvements
- RESTful API endpoints
- Advanced filtering and search options
- Paper recommendation system
- Integration with reference managers (Zotero, Mendeley)

---

**Legend:**
- **Added** for new features
- **Changed** for changes in existing functionality  
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes 