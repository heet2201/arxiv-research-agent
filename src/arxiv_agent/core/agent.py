"""
Main autonomous research agent
"""
import time
import requests
import logging
from typing import List, Dict, Any, Optional, Generator
from .models import AgentStep, StepStatus, TaskType, ConversationContext
from ..analysis.query_analyzer import QueryAnalyzer
from ..analysis.visual_extractor import VisualExtractor
from ..search.enhanced_search import EnhancedSearchEngine
try:
    from config.config import Config
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from config.config import Config

logger = logging.getLogger(__name__)

class DecisionEngine:
    """Simple decision engine to determine next steps"""
    
    def __init__(self, llm_caller):
        self.llm_caller = llm_caller
    
    def plan_steps(self, query: str, analysis: Dict) -> List[AgentStep]:
        """Plan execution steps based on query analysis"""
        steps = []
        
        # Step 1: Always analyze query
        steps.append(AgentStep(
            id=1,
            name="Query Analysis",
            description="Analyze user query to understand research intent",
            task_type=TaskType.ANALYZE_QUERY,
            reasoning="First step to understand what the user is looking for"
        ))
        
        # Step 2: Search for papers
        steps.append(AgentStep(
            id=2,
            name="Search Papers",
            description="Search multiple sources (ArXiv, Serper.dev, Google Scholar, Semantic Scholar, CrossRef) for relevant research papers",
            task_type=TaskType.SEARCH_PAPERS,
            reasoning="Find papers related to the research query"
        ))
        
        # Step 3: Extract visual data
        steps.append(AgentStep(
            id=3,
            name="Extract Visual Data",
            description="Extract charts, tables, and diagrams from top papers",
            task_type=TaskType.EXTRACT_VISUALS,
            reasoning="Extract visual information to provide richer context"
        ))
        
        # Step 4: Analyze papers
        steps.append(AgentStep(
            id=4,
            name="Analyze Papers",
            description="Analyze found papers for key insights using extracted content",
            task_type=TaskType.ANALYZE_PAPERS,
            reasoning="Extract meaningful insights from the research papers with their content"
        ))
        
        # Step 5: Synthesize response
        steps.append(AgentStep(
            id=5,
            name="Synthesize Response",
            description="Create comprehensive response for the user",
            task_type=TaskType.SYNTHESIZE,
            reasoning="Combine all findings into a coherent response"
        ))
        
        return steps

class AutonomousResearchAgent:
    """Autonomous ArXiv research agent with real-time updates and content extraction"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.config.validate_config()
        
        # Initialize components
        self.query_analyzer = QueryAnalyzer()
        self.searcher = EnhancedSearchEngine(
            serper_api_key=self.config.SERPER_API_KEY,
            semantic_scholar_api_key=self.config.SEMANTIC_SCHOLAR_API_KEY
        )
        self.visual_extractor = VisualExtractor()
        self.decision_engine = DecisionEngine(self.call_llm)
        
        # State management
        self.current_steps = []
        self.context = {}
        self.conversation_history: List[ConversationContext] = []
        
        logger.info("Autonomous Research Agent initialized")
    
    def call_llm(self, messages: List[Dict], temperature: Optional[float] = None) -> str:
        """Call LLM API"""
        temperature = temperature or self.config.LLM_TEMPERATURE
        
        try:
            payload = {
                "model": self.config.LLM_MODEL,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": self.config.LLM_MAX_TOKENS
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=self.config.get_headers(),
                json=payload,
                timeout=self.config.LLM_TIMEOUT
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    return response_data['choices'][0]['message']['content']
                else:
                    return "API Error: No response content received"
            else:
                error_msg = f"Error querying LLM: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return f"API Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            error_msg = f"Connection Error: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def process_query_streaming(self, query: str) -> Generator[tuple, None, None]:
        """Process research query with streaming updates"""
        if not query.strip():
            yield "Please enter a research query.", "No steps to execute."
            return
        
        try:
            # Initialize
            self.context = {'query': query}
            analysis = self.query_analyzer.analyze_query(query)
            self.current_steps = self.decision_engine.plan_steps(query, analysis)
            
            # Show initial steps
            steps_display = self.format_steps()
            yield "🚀 Starting enhanced research with content extraction...", steps_display
            
            # Execute each step
            for step in self.current_steps:
                # Update step to running
                step.status = StepStatus.RUNNING
                steps_display = self.format_steps()
                yield f"🔄 Executing: {step.name}", steps_display
                
                # Execute step
                result = self.execute_step(step)
                
                # Update step to completed
                steps_display = self.format_steps()
                yield f"✅ Completed: {step.name}", steps_display
            
            # Final result
            final_response = self.context.get('final_response', 'Research completed!')
            yield final_response, steps_display
                
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            logger.error(error_msg)
            yield error_msg, "Execution failed."
    
    def execute_step(self, step: AgentStep) -> str:
        """Execute a single step and return result"""
        step.status = StepStatus.RUNNING
        start_time = time.time()
        
        try:
            if step.task_type == TaskType.ANALYZE_QUERY:
                result = self._execute_query_analysis()
            elif step.task_type == TaskType.SEARCH_PAPERS:
                result = self._execute_paper_search()
            elif step.task_type == TaskType.EXTRACT_VISUALS:
                result = self._execute_visual_extraction()
            elif step.task_type == TaskType.ANALYZE_PAPERS:
                result = self._execute_paper_analysis()
            elif step.task_type == TaskType.SYNTHESIZE:
                result = self._execute_synthesis()
            else:
                result = "Unknown step type"
            
            step.status = StepStatus.COMPLETED
            step.result = result
            
        except Exception as e:
            step.status = StepStatus.FAILED
            step.result = f"Error: {str(e)}"
            result = step.result
            logger.error(f"Step {step.name} failed: {e}")
        
        step.execution_time = time.time() - start_time
        return result
    
    def _execute_query_analysis(self) -> str:
        """Execute query analysis step"""
        query = self.context['query']
        
        # Check for follow-up queries
        contextualized_query = self.query_analyzer.contextualize_query(query, self.conversation_history)
        
        analysis = self.query_analyzer.analyze_query(contextualized_query)
        self.context['analysis'] = analysis
        self.context['contextualized_query'] = contextualized_query
        
        return f"Intent: {analysis.intent}, Complexity: {analysis.complexity}"
    
    def _execute_paper_search(self) -> str:
        """Execute paper search step"""
        search_query = self.context.get('contextualized_query', self.context['query'])
        top_papers, total_papers = self.searcher.search_papers(
            search_query, 
            max_results=self.config.MAX_SEARCH_RESULTS
        )
        self.context['papers'] = top_papers
        
        return f"Found {total_papers} papers, selected top {len(top_papers)}"
    
    def _execute_visual_extraction(self) -> str:
        """Execute visual data extraction step"""
        papers = self.context.get('papers', [])
        
        if not papers:
            return "No papers to extract visuals from"
        
        visual_count = 0
        # Extract from top papers only
        for paper in papers[:self.config.MAX_VISUAL_EXTRACTIONS]:
            try:
                visuals = self.visual_extractor.extract_visuals_from_paper(
                    paper.url, 
                    max_visuals=3
                )
                paper.visual_data = visuals
                visual_count += len(visuals)
            except Exception as e:
                logger.error(f"Error extracting visuals from {paper.title}: {e}")
                paper.visual_data = []
        
        return f"Extracted {visual_count} visual elements from top {self.config.MAX_VISUAL_EXTRACTIONS} papers"
    
    def _execute_paper_analysis(self) -> str:
        """Execute paper analysis step using LLM with extracted visuals"""
        papers = self.context.get('papers', [])
        query = self.context.get('contextualized_query', self.context['query'])
        
        if not papers:
            return "No papers found to analyze"

        # Prepare paper summaries with visual data
        paper_summaries = []
        for i, paper in enumerate(papers[:self.config.MAX_PAPERS_FOR_ANALYSIS], 1):
            summary = f"Paper {i}: {paper.title}\n"
            summary += f"URL: {paper.url}\n"
            summary += f"Published: {paper.published_date}\n"
            summary += f"Categories: {', '.join(paper.categories)}\n"
            summary += f"Authors: {', '.join(paper.authors[:3])}\n"
            summary += f"Abstract: {paper.abstract[:3000]}...\n"
            
            # Add visual data
            if paper.visual_data:
                summary += f"\nVisual Data Found:\n"
                for j, visual in enumerate(paper.visual_data):
                    summary += f"- {visual.type.title()} {j+1}: {visual.description}\n"
                    if visual.text_content:
                        summary += f"  Content: {visual.text_content[:1500]}...\n"
            
            paper_summaries.append(summary)
        
        prompt = f"""Analyze these research papers for the query: "{query}"

        Papers with extracted visuals:
        {chr(10).join(paper_summaries)}
        
        Provide the following:
        1. Answer the question with clear, well-researched and structured technical information
        2. Reference relevant research areas or methodologies that support your explanation
        3. Offer actionable insights or next steps where appropriate

        Along with the above, provide comprehensive analysis including:
        1. Key findings and quantitative results
        2. Methodological approaches used
        3. Notable contributions and innovations
        4. Research trends and patterns
        5. Limitations and future work mentioned

        Focus on specific results, numbers, and concrete findings from the papers."""
        
        messages = [
            {"role": "system", "content": "You are a research assistant specialized in analyzing scientific papers. Focus on extracting concrete findings, methodologies, and quantitative results. Provide detailed technical insights."},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self.call_llm(messages)
        self.context['paper_analysis'] = analysis
        
        return "Enhanced paper analysis with extracted content completed"
    
    def _execute_synthesis(self) -> str:
        """Execute final synthesis step"""
        query = self.context['query']
        papers = self.context.get('papers', [])
        analysis = self.context.get('paper_analysis', '')
        
        response_parts = [
            f"## Research Report: {query}",
        ]
        
        if analysis:
            response_parts.append("\n --- \n ## Key Insights \n --- \n")
            response_parts.append(analysis)
        
        if papers:
            response_parts.append("\n --- \n ## Top 3 Papers \n --- \n")
            for i, paper in enumerate(papers[:3], 1):
                response_parts.append(f"**{i}. {paper.title}**")
                response_parts.append(f"Authors: {', '.join(paper.authors[:3])}")
                response_parts.append(f"[Paper Link]({paper.url})")
                response_parts.append("")
        
        final_response = "\n".join(response_parts)
        self.context['final_response'] = final_response
        
        # Save to conversation history
        context = ConversationContext(
            query=query,
            summary=analysis[:500] + "..." if len(analysis) > 500 else analysis,
            timestamp=time.time()
        )
        self.conversation_history.append(context)
        
        # Keep only recent interactions
        self.conversation_history = self.conversation_history[-self.config.MAX_CONVERSATION_HISTORY:]
            
        return "Synthesis completed"
    
    def format_steps(self) -> str:
        """Format steps for display with real-time status"""
        if not self.current_steps:
            return "No steps planned yet..."
        
        output = ["# 🤖 Agent Execution Progress\n"]
        
        for step in self.current_steps:
            # Use different styling based on status
            output.append(f"#### {step.status.value} Step {step.id}: {step.name}\n")
            output.append(f"**Task:** {step.description}\n")
            output.append(f"**Reasoning:** {step.reasoning}\n")
            
            if step.result and step.status in [StepStatus.COMPLETED, StepStatus.FAILED]:
                output.append(f"**Result:** {step.result}\n")
            
            if step.execution_time > 0:
                output.append(f"**Duration:** {step.execution_time:.2f}s \n")
            
            output.append("---\n")
        
        return "\n".join(output) 