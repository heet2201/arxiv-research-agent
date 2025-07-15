"""
Enhanced search engine that combines multiple academic sources
"""
import feedparser
import requests
import logging
from urllib.parse import quote
from typing import List, Tuple, Optional
from .base_search import BaseSearchEngine
from ..core.models import SearchResult, ResearchPaper
import re

logger = logging.getLogger(__name__)

class EnhancedSearchEngine(BaseSearchEngine):
    """Enhanced search engine with multiple academic sources"""
    
    def __init__(self, serper_api_key: Optional[str] = None, semantic_scholar_api_key: Optional[str] = None):
        super().__init__()
        self.serper_api_key = serper_api_key
        self.semantic_scholar_api_key = semantic_scholar_api_key
        
        logger.info(f"Enhanced search initialized with Serper: {bool(serper_api_key)}")
    
    def search_papers(self, query: str, max_results: int = 20) -> Tuple[List[ResearchPaper], int]:
        """
        Enhanced search across multiple sources
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Tuple of (papers_list, total_count)
        """
        logger.info(f"Enhanced search for: {query}")
        
        # Clean and optimize query
        cleaned_query = self.clean_query(query)
        logger.info(f"Cleaned query: {cleaned_query}")
        
        all_results = []
        
        # 1. ArXiv search
        arxiv_papers = self._search_arxiv(cleaned_query, max_results // 2)
        all_results.extend(self._convert_papers_to_results(arxiv_papers))
        
        # 2. Serper search (if API key available)
        if self.serper_api_key:
            serper_results = self._search_serper(cleaned_query, max_results // 2)
            all_results.extend(serper_results)
            self.rate_limit()
        
        # 3. Semantic Scholar search
        semantic_results = self._search_semantic_scholar(cleaned_query, max_results // 3)
        all_results.extend(semantic_results)
        self.rate_limit()
        
        # 4. CrossRef search
        crossref_results = self._search_crossref(cleaned_query, max_results // 4)
        all_results.extend(crossref_results)
        
        # Convert back to ResearchPaper format and deduplicate
        unique_papers = self._deduplicate_and_convert(all_results, query)
        
        # Calculate relevance scores and sort
        scored_papers = self.calculate_relevance_scores(unique_papers, query)
        sorted_papers = sorted(scored_papers, key=lambda x: x.relevance_score, reverse=True)
        
        return sorted_papers[:max_results], len(sorted_papers)
    
    def _search_arxiv(self, query: str, max_results: int) -> List[ResearchPaper]:
        """Search ArXiv using multiple strategies"""
        clean_query = ' '.join(query.split())
        papers = []
        
        # Different search strategies
        strategies = [
            f'all:"{clean_query}"',
            f'ti:({clean_query})',
            f'abs:({clean_query})',
            f"cat:cs.* AND all:{query}",
            f"all:{query} AND cat:cs.LG",
            f"all:{query} AND cat:cs.CV",
        ]

        strategy_limit = max(1, max_results // len(strategies))
        
        for strategy in strategies:
            try:
                encoded_query = quote(strategy)
                url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&start=0&max_results={strategy_limit}&sortBy=relevance&sortOrder=descending"

                response = self.session.get(url, timeout=15)
                if response.status_code == 200:
                    new_papers = self._parse_arxiv_response(response.text)
                    papers.extend(new_papers)
                self.rate_limit()
                
            except Exception as e:
                logger.error(f"Error in ArXiv strategy '{strategy}': {str(e)}")
                continue

        logger.info(f"ArXiv search returned {len(papers)} results")
        return papers
    
    def _parse_arxiv_response(self, xml_content: str) -> List[ResearchPaper]:
        """Parse ArXiv XML response"""
        papers = []
        try:
            feed = feedparser.parse(xml_content)
            if hasattr(feed, 'entries') and len(feed.entries) > 0:
                for entry in feed.entries:
                    title = entry.get('title', '').replace('\n', ' ').strip()
                    authors = [author.name for author in getattr(entry, 'authors', [])]
                    abstract = entry.get('summary', '').replace('\n', ' ').strip()
                    url = entry.get('link', '')
                    pub_date = entry.get('published', '')
                    categories = [tag.term for tag in getattr(entry, 'tags', [])]
                    
                    if title and abstract:
                        papers.append(ResearchPaper(
                            title=title,
                            authors=authors,
                            abstract=abstract,
                            url=url,
                            published_date=pub_date,
                            categories=categories
                        ))
        except Exception as e:
            logger.error(f"XML parsing error: {e}")
        
        return papers
    
    def _search_serper(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search using Serper.dev Google Search API"""
        if not self.serper_api_key:
            return []
            
        results = []
        try:
            # Academic-focused search
            academic_query = f"{query} site:arxiv.org OR site:scholar.google.com OR site:researchgate.net OR site:ieee.org OR site:acm.org OR filetype:pdf"
            
            payload = {
                "q": academic_query,
                "num": max_results,
                "gl": "us",
                "hl": "en"
            }
            
            headers = {
                "X-API-KEY": self.serper_api_key,
                "Content-Type": "application/json"
            }
            
            response = self.session.post(
                "https://google.serper.dev/search",
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Process organic results
                for item in data.get('organic', []):
                    result = SearchResult(
                        title=item.get('title', ''),
                        url=item.get('link', ''),
                        snippet=item.get('snippet', ''),
                        source='serper',
                        publication_date=item.get('date', '')
                    )
                    results.append(result)
                
                # Process scholar results if available
                for item in data.get('scholar', []):
                    result = SearchResult(
                        title=item.get('title', ''),
                        url=item.get('link', ''),
                        snippet=item.get('snippet', ''),
                        source='serper_scholar',
                        publication_date=item.get('publicationInfo', {}).get('summary', '')
                    )
                    results.append(result)
                    
            logger.info(f"Serper search returned {len(results)} results")
            
        except Exception as e:
            logger.error(f"Serper search error: {e}")
            
        return results
    
    def _search_semantic_scholar(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search using Semantic Scholar API"""
        results = []
        try:
            headers = {}
            if self.semantic_scholar_api_key:
                headers["x-api-key"] = self.semantic_scholar_api_key
            
            params = {
                "query": query,
                "limit": max_results,
                "fields": "title,abstract,authors,year,url,venue,citationCount"
            }
            
            response = self.session.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                headers=headers,
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                for paper in data.get('data', []):
                    authors = []
                    if paper.get('authors'):
                        authors = [author.get('name', '') for author in paper['authors']]
                    
                    result = SearchResult(
                        title=paper.get('title', ''),
                        url=paper.get('url', ''),
                        snippet=paper.get('abstract', '')[:500] + "..." if paper.get('abstract') else '',
                        source='semantic_scholar',
                        publication_date=str(paper.get('year', '')),
                        authors=authors
                    )
                    results.append(result)
                    
            logger.info(f"Semantic Scholar search returned {len(results)} results")
            
        except Exception as e:
            logger.error(f"Semantic Scholar search error: {e}")
            
        return results
    
    def _search_crossref(self, query: str, max_results: int = 5) -> List[SearchResult]:
        """Search using CrossRef API for academic papers"""
        results = []
        try:
            params = {
                "query": query,
                "rows": max_results,
                "select": "title,author,abstract,published-print,URL,DOI"
            }
            
            response = self.session.get(
                "https://api.crossref.org/works",
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                for item in data.get('message', {}).get('items', []):
                    authors = []
                    if item.get('author'):
                        authors = [f"{auth.get('given', '')} {auth.get('family', '')}" 
                                 for auth in item['author']]
                    
                    # Get publication date
                    pub_date = ""
                    if item.get('published-print', {}).get('date-parts'):
                        date_parts = item['published-print']['date-parts'][0]
                        pub_date = f"{date_parts[0]}"
                    
                    result = SearchResult(
                        title=' '.join(item.get('title', [''])),
                        url=item.get('URL', ''),
                        snippet=item.get('abstract', '')[:500] + "..." if item.get('abstract') else '',
                        source='crossref',
                        publication_date=pub_date,
                        authors=authors
                    )
                    results.append(result)
                    
            logger.info(f"CrossRef search returned {len(results)} results")
            
        except Exception as e:
            logger.error(f"CrossRef search error: {e}")
            
        return results
    
    def _convert_papers_to_results(self, papers: List[ResearchPaper]) -> List[SearchResult]:
        """Convert ResearchPaper objects to SearchResult objects"""
        results = []
        for paper in papers:
            result = SearchResult(
                title=paper.title,
                url=paper.url,
                snippet=paper.abstract,
                source='arxiv',
                publication_date=paper.published_date,
                authors=paper.authors
            )
            results.append(result)
        return results
    
    def _deduplicate_and_convert(self, results: List[SearchResult], query: str) -> List[ResearchPaper]:
        """Remove duplicates and convert back to ResearchPaper format"""
        seen_titles = set()
        unique_papers = []
        
        for result in results:
            if not result.title:
                continue
                
            normalized_title = re.sub(r'[^\w\s]', '', result.title.lower()).strip()
            if normalized_title and normalized_title not in seen_titles:
                seen_titles.add(normalized_title)
                
                # Convert back to ResearchPaper
                paper = ResearchPaper(
                    title=result.title,
                    authors=result.authors or [],
                    abstract=result.snippet,
                    url=result.url,
                    published_date=result.publication_date,
                    categories=[result.source]  # Use source as category
                )
                unique_papers.append(paper)
        
        return unique_papers 