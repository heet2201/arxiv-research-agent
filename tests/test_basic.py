"""
Basic tests for ArXiv Research Agent
"""
import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.arxiv_agent.core.models import StepStatus, TaskType, VisualData, ResearchPaper
from src.arxiv_agent.analysis.query_analyzer import QueryAnalyzer
from config.config import Config

class TestModels:
    """Test data models and enums"""
    
    def test_step_status_enum(self):
        """Test StepStatus enum"""
        assert StepStatus.PENDING.value == "⏳ Pending"
        assert StepStatus.RUNNING.value == "🔄 Running"
        assert StepStatus.COMPLETED.value == "✅ Completed"
        assert StepStatus.FAILED.value == "❌ Failed"
    
    def test_task_type_enum(self):
        """Test TaskType enum"""
        assert TaskType.ANALYZE_QUERY.value == "analyze_query"
        assert TaskType.SEARCH_PAPERS.value == "search_papers"
        assert TaskType.EXTRACT_VISUALS.value == "extract_visuals"
    
    def test_visual_data_creation(self):
        """Test VisualData dataclass"""
        visual = VisualData(
            type="chart",
            description="Test chart",
            text_content="Chart showing results"
        )
        assert visual.type == "chart"
        assert visual.description == "Test chart"
        assert visual.text_content == "Chart showing results"
        assert visual.base64_image == ""
        assert visual.page_number == 0
    
    def test_research_paper_creation(self):
        """Test ResearchPaper dataclass"""
        paper = ResearchPaper(
            title="Test Paper",
            authors=["Author 1", "Author 2"],
            abstract="This is a test abstract",
            url="https://arxiv.org/abs/test",
            published_date="2024-01-01",
            categories=["cs.AI"]
        )
        assert paper.title == "Test Paper"
        assert len(paper.authors) == 2
        assert paper.relevance_score == 0.0
        assert len(paper.visual_data) == 0

class TestQueryAnalyzer:
    """Test query analysis functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = QueryAnalyzer()
    
    def test_search_intent_detection(self):
        """Test search intent detection"""
        query = "find papers about machine learning"
        analysis = self.analyzer.analyze_query(query)
        assert analysis.intent == "search"
    
    def test_analyze_intent_detection(self):
        """Test analyze intent detection"""
        query = "explain how neural networks work"
        analysis = self.analyzer.analyze_query(query)
        assert analysis.intent == "analyze"
    
    def test_compare_intent_detection(self):
        """Test compare intent detection"""
        query = "compare transformer vs RNN architectures"
        analysis = self.analyzer.analyze_query(query)
        assert analysis.intent == "compare"
        assert analysis.needs_comparison == True
    
    def test_complexity_detection(self):
        """Test complexity detection"""
        simple_query = "AI"
        complex_query = "comprehensive analysis of state-of-the-art transformer architectures and their applications in natural language processing tasks"
        
        simple_analysis = self.analyzer.analyze_query(simple_query)
        complex_analysis = self.analyzer.analyze_query(complex_query)
        
        assert simple_analysis.complexity == "simple"
        assert complex_analysis.complexity == "complex"
    
    def test_followup_detection(self):
        """Test follow-up query detection"""
        conversation_history = [
            {"query": "machine learning algorithms"}
        ]
        
        followup_query = "tell me more about this"
        regular_query = "quantum computing applications"
        
        assert self.analyzer.is_followup_query(followup_query, conversation_history) == True
        assert self.analyzer.is_followup_query(regular_query, conversation_history) == False
    
    def test_query_contextualization(self):
        """Test query contextualization"""
        conversation_history = [
            {"query": "neural networks"}
        ]
        
        followup_query = "how do they work?"
        contextualized = self.analyzer.contextualize_query(followup_query, conversation_history)
        
        assert "neural networks" in contextualized.lower()
        assert "how do they work?" in contextualized

class TestConfig:
    """Test configuration management"""
    
    def test_config_creation(self):
        """Test configuration creation"""
        config = Config()
        assert config.LLM_MODEL == "anthropic/claude-sonnet-4"
        assert config.LLM_TEMPERATURE == 0.3
        assert config.GRADIO_SERVER_PORT == 7861
    
    def test_headers_generation(self):
        """Test API headers generation"""
        config = Config()
        headers = config.get_headers()
        assert "Authorization" in headers
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"

class TestIntegration:
    """Integration tests"""
    
    def test_query_analysis_integration(self):
        """Test full query analysis workflow"""
        analyzer = QueryAnalyzer()
        
        # Test a realistic research query
        query = "latest developments in large language models for code generation"
        analysis = analyzer.analyze_query(query)
        
        assert analysis.intent in ["search", "analyze", "compare"]
        assert analysis.complexity in ["simple", "medium", "complex"]
        assert isinstance(analysis.keywords, list)
        assert len(analysis.keywords) > 0

# Test fixtures
@pytest.fixture
def sample_paper():
    """Sample research paper for testing"""
    return ResearchPaper(
        title="Attention Is All You Need",
        authors=["Vaswani, Ashish", "Shazeer, Noam"],
        abstract="The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
        url="https://arxiv.org/abs/1706.03762",
        published_date="2017-06-12",
        categories=["cs.CL", "cs.LG"]
    )

@pytest.fixture
def sample_visual():
    """Sample visual data for testing"""
    return VisualData(
        type="table",
        description="Performance comparison table",
        text_content="Model | BLEU Score | Time\nTransformer | 28.4 | 3.5h",
        page_number=3
    )

def test_paper_with_visuals(sample_paper, sample_visual):
    """Test paper with visual data"""
    sample_paper.visual_data = [sample_visual]
    assert len(sample_paper.visual_data) == 1
    assert sample_paper.visual_data[0].type == "table"

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 