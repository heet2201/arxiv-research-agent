#!/usr/bin/env python3
"""
Basic usage example for ArXiv Research Agent
"""
import sys
import os

# Add src and root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.arxiv_agent.core.agent import AutonomousResearchAgent
from config.config import Config

def basic_example():
    """Basic example of using the research agent programmatically"""
    
    print("🔬 ArXiv Research Agent - Basic Example")
    print("=" * 50)
    
    try:
        # Initialize configuration
        config = Config()
        config.validate_config()
        
        # Create agent
        agent = AutonomousResearchAgent(config)
        
        # Example query
        query = "transformer architectures in natural language processing"
        print(f"🔍 Searching for: {query}")
        print("-" * 50)
        
        # Process query with streaming updates
        for i, (response, steps) in enumerate(agent.process_query_streaming(query)):
            print(f"\n📊 Update {i+1}:")
            print(f"Response: {response[:100]}...")
            print(f"Steps: {steps[:100]}...")
            
            # Break after getting final result
            if "Research Report:" in response:
                print("\n✅ Final Result:")
                print(response)
                break
        
        print("\n🎉 Research completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("1. Set your OPENROUTER_API_KEY environment variable")
        print("2. Installed all dependencies: pip install -r requirements.txt")

def simple_search_example():
    """Example of just using the search functionality"""
    
    print("\n🔍 Search Only Example")
    print("=" * 30)
    
    try:
        from src.arxiv_agent.search.enhanced_search import EnhancedSearchEngine
        
        # Initialize search engine
        searcher = EnhancedSearchEngine()
        
        # Search for papers
        query = "machine learning"
        papers, total = searcher.search_papers(query, max_results=5)
        
        print(f"Found {total} papers for '{query}':")
        print("-" * 40)
        
        for i, paper in enumerate(papers[:3], 1):
            print(f"\n{i}. {paper.title}")
            print(f"   Authors: {', '.join(paper.authors[:2])}")
            print(f"   Score: {paper.relevance_score:.3f}")
            print(f"   URL: {paper.url}")
        
    except Exception as e:
        print(f"❌ Search Error: {e}")

def query_analysis_example():
    """Example of query analysis functionality"""
    
    print("\n🧠 Query Analysis Example")
    print("=" * 30)
    
    try:
        from src.arxiv_agent.analysis.query_analyzer import QueryAnalyzer
        
        analyzer = QueryAnalyzer()
        
        queries = [
            "find papers about neural networks",
            "compare transformer vs RNN architectures",
            "explain how attention mechanisms work"
        ]
        
        for query in queries:
            analysis = analyzer.analyze_query(query)
            print(f"\nQuery: '{query}'")
            print(f"Intent: {analysis.intent}")
            print(f"Complexity: {analysis.complexity}")
            print(f"Needs comparison: {analysis.needs_comparison}")
        
    except Exception as e:
        print(f"❌ Analysis Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting ArXiv Research Agent Examples")
    
    # Run examples
    basic_example()
    simple_search_example()
    query_analysis_example()
    
    print("\n" + "=" * 60)
    print("✨ Examples completed!")
    print("💡 Try running 'python main.py' for the full web interface") 