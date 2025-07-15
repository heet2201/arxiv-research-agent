"""
Query analysis module for understanding user research intent
"""
from typing import Dict, Any, List
from ..core.models import QueryAnalysis

class QueryAnalyzer:
    """Analyze user queries to determine research intent"""
    
    def analyze_query(self, query: str) -> QueryAnalysis:
        """
        Simple query analysis based on keywords
        
        Args:
            query: User's research query
            
        Returns:
            QueryAnalysis object with intent, complexity, and keywords
        """
        query_lower = query.lower()
        
        # Detect intent based on keywords
        search_keywords = [
            'find', 'search', 'papers', 'research', 'literature', 'look', 
            'seek', 'locate', 'discover', 'explore', 'investigate', 'study', 
            'review', 'survey', 'publications', 'articles', 'documents'
        ]
        
        analyze_keywords = [
            'analyze', 'explain', 'understand', 'insights', 'examine', 
            'evaluate', 'assess', 'interpret', 'investigate', 'study', 
            'breakdown', 'dissect', 'clarify', 'describe', 'elaborate', 'detail'
        ]
        
        compare_keywords = [
            'compare', 'difference', 'versus', 'vs', 'contrast', 'distinguish', 
            'differentiate', 'between', 'relative', 'similarities', 'differences', 
            'comparison', 'relate', 'correlation', 'against'
        ]
        
        # Determine primary intent
        intent = 'search'  # default
        if any(word in query_lower for word in analyze_keywords):
            intent = 'analyze'
        elif any(word in query_lower for word in compare_keywords):
            intent = 'compare'
        
        # Estimate complexity based on query length and structure
        complexity = 'medium'
        word_count = len(query.split())
        if word_count < 5:
            complexity = 'simple'
        elif word_count > 15:
            complexity = 'complex'
        
        # Extract keywords (simple tokenization)
        keywords = query.split()
        
        # Check if comparison is needed
        needs_comparison = any(word in query_lower for word in compare_keywords)
        
        return QueryAnalysis(
            intent=intent,
            complexity=complexity,
            keywords=keywords,
            needs_comparison=needs_comparison
        )
    
    def is_followup_query(self, query: str, conversation_history: List[Any]) -> bool:
        """
        Determine if the current query is a follow-up to previous queries
        
        Args:
            query: Current user query
            conversation_history: List of previous conversation contexts
            
        Returns:
            Boolean indicating if this is a follow-up query
        """
        if not conversation_history:
            return False
            
        query_lower = query.lower().strip()
        
        # Common follow-up indicators
        followup_indicators = [
            # Direct references
            'tell me more', 'give me more', 'explain further', 'more details', 'elaborate',
            'what about', 'how about', 'why', 'how', 'when', 'where',
            
            # Reference words
            'this', 'that', 'these', 'those', 'it', 'they', 'them',
            'above', 'previous', 'mentioned', 'discussed', 'earlier',
            
            # Comparison words
            'compare', 'difference', 'versus', 'vs', 'contrast',
            'similar', 'different', 'same', 'like',
            
            # Continuation words
            'additionally', 'furthermore', 'besides', 'in addition',
            'but', 'however', 'still', 'yet', 'then', 'next'
        ]
        
        # Count matches with follow-up indicators
        matches = sum(1 for indicator in followup_indicators if indicator in query_lower)
        is_short_query = len(query.split()) < 3
        
        # Check if query starts with common question words (typically follow-ups)
        question_starters = ['what', 'how', 'why', 'which', 'when', 'where', 'is', 'are', 'can', 'could', 'would']
        starts_with_question = any(query_lower.startswith(starter) for starter in question_starters)
        
        # Decision logic
        return (matches >= 1) or (is_short_query) or (starts_with_question and len(query.split()) < 5)
    
    def contextualize_query(self, query: str, conversation_history: List[Any]) -> str:
        """
        Add context to a follow-up query based on conversation history
        
        Args:
            query: Current user query
            conversation_history: List of previous conversation contexts
            
        Returns:
            Contextualized query string
        """
        if not self.is_followup_query(query, conversation_history):
            return query
            
        # Get recent queries for context (last 2 interactions)
        recent_queries = []
        for item in conversation_history[-2:]:
            if hasattr(item, 'query'):
                recent_queries.append(item.query.lower())
            elif isinstance(item, dict) and 'query' in item:
                recent_queries.append(item['query'].lower())
        
        if recent_queries:
            context_text = ' '.join(recent_queries)
            return f"Context: {context_text} \nCurrent question: {query}"
        
        return query 