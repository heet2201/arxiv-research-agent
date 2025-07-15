"""
Base search engine class for multi-source academic search
"""
import requests
import time
import logging
import re
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
from ..core.models import SearchResult, ResearchPaper

logger = logging.getLogger(__name__)

class BaseSearchEngine:
    """Base class for search engines with common functionality"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Academic-Agent/1.0'})
        
        # Initialize TF-IDF vectorizer for relevance scoring
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=10000,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            analyzer='word',
            sublinear_tf=True,
            strip_accents='unicode'
        )
    
    def clean_query(self, query: str) -> str:
        """
        Clean and optimize query for academic search
        
        Args:
            query: Raw user query
            
        Returns:
            Cleaned query string
        """
        # Academic keywords that should be preserved
        academic_keywords = {
            'research', 'study', 'analysis', 'method', 'approach', 'technique',
            'algorithm', 'model', 'learning', 'neural', 'network', 'deep',
            'machine', 'artificial', 'intelligence', 'data', 'science',
            'computer', 'vision', 'processing', 'natural', 'language',
            'quantum', 'computing', 'robotics', 'optimization', 'classification',
            'regression', 'clustering', 'supervised', 'unsupervised',
            'reinforcement', 'transformer', 'attention', 'convolution',
            'graph', 'embedding', 'feature', 'detection', 'recognition',
            'segmentation', 'generation', 'prediction', 'evaluation',
            'performance', 'accuracy', 'precision', 'recall', 'framework',
            'architecture', 'implementation', 'application', 'development',
            'latest', 'recent', 'new', 'novel', 'advanced', 'state-of-the-art',
            'compared', 'comparison', 'survey', 'review', 'comprehensive'
        }
        
        # Convert to lowercase and clean
        text = query.lower()
        words = re.sub(r'[^\w\s]', ' ', text).split()
        
        # Filter words: keep if not a stop word OR if it's an academic keyword
        filtered_words = [
            word for word in words 
            if len(word) > 2 and (word not in ENGLISH_STOP_WORDS or word in academic_keywords)
        ]
        
        # If too few words remain, keep original query
        if len(filtered_words) < 2:
            return query
        
        return ' '.join(filtered_words)
    
    def calculate_relevance_scores(self, papers: List[ResearchPaper], query: str) -> List[ResearchPaper]:
        """
        Calculate relevance scores using TF-IDF similarity
        
        Args:
            papers: List of research papers
            query: Original search query
            
        Returns:
            List of papers with updated relevance scores
        """
        if not papers:
            return papers

        documents = []
        for paper in papers:
            doc = f"{paper.title} {paper.abstract}"
            documents.append(doc)
        documents.append(query)

        try:
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            query_vector = tfidf_matrix[-1]
            paper_vectors = tfidf_matrix[:-1]
            similarities = cosine_similarity(query_vector, paper_vectors).flatten()

            for i, paper in enumerate(papers):
                paper.relevance_score = float(similarities[i])

        except Exception as e:
            logger.error(f"Error calculating relevance scores: {str(e)}")
            # Fallback to simple keyword matching
            query_keywords = set(query.lower().split())
            for paper in papers:
                text = f"{paper.title} {paper.abstract}".lower()
                matches = sum(1 for keyword in query_keywords if keyword in text)
                paper.relevance_score = matches / len(query_keywords)

        return papers
    
    def deduplicate_papers(self, papers: List[ResearchPaper]) -> List[ResearchPaper]:
        """
        Remove duplicate papers based on title similarity
        
        Args:
            papers: List of papers that may contain duplicates
            
        Returns:
            List of unique papers
        """
        seen_titles = set()
        unique_papers = []
        
        for paper in papers:
            if not paper.title:
                continue
                
            # Normalize title for comparison
            normalized_title = re.sub(r'[^\w\s]', '', paper.title.lower()).strip()
            if normalized_title and normalized_title not in seen_titles:
                seen_titles.add(normalized_title)
                unique_papers.append(paper)
        
        return unique_papers
    
    def rate_limit(self, delay: float = 1.0):
        """Apply rate limiting between API calls"""
        time.sleep(delay) 