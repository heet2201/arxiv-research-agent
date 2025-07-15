"""
Core data models and enums for ArXiv Research Agent
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional

class StepStatus(Enum):
    """Status of execution steps"""
    PENDING = "⏳ Pending"
    RUNNING = "🔄 Running" 
    COMPLETED = "✅ Completed"
    FAILED = "❌ Failed"

class TaskType(Enum):
    """Types of tasks the agent can perform"""
    ANALYZE_QUERY = "analyze_query"
    SEARCH_PAPERS = "search_papers"
    EXTRACT_VISUALS = "extract_visuals"
    ANALYZE_PAPERS = "analyze_papers"
    SYNTHESIZE = "synthesize"

@dataclass
class VisualData:
    """Data structure for visual content extracted from papers"""
    type: str  # 'chart', 'table', 'diagram', 'image'
    description: str
    text_content: str  # Extracted text from visual
    base64_image: str = ""
    page_number: int = 0

@dataclass
class AgentStep:
    """Represents a single execution step in the agent workflow"""
    id: int
    name: str
    description: str
    task_type: TaskType
    status: StepStatus = StepStatus.PENDING
    result: str = ""
    reasoning: str = ""
    execution_time: float = 0.0

@dataclass
class ResearchPaper:
    """Represents a research paper with metadata and content"""
    title: str
    authors: List[str]
    abstract: str
    url: str
    published_date: str
    categories: List[str]
    relevance_score: float = 0.0
    visual_data: List[VisualData] = field(default_factory=list)

@dataclass
class SearchResult:
    """Generic search result from various sources"""
    title: str
    url: str
    snippet: str
    source: str  # 'arxiv', 'serper', 'semantic_scholar', etc.
    publication_date: str = ""
    authors: List[str] = field(default_factory=list)
    relevance_score: float = 0.0

@dataclass
class QueryAnalysis:
    """Analysis result of user query"""
    intent: str  # 'search', 'analyze', 'compare'
    complexity: str  # 'simple', 'medium', 'complex'
    keywords: List[str]
    needs_comparison: bool = False

@dataclass
class ConversationContext:
    """Context for conversation history"""
    query: str
    summary: str
    timestamp: float 