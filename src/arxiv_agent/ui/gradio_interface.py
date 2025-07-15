"""
Gradio interface for the ArXiv Research Agent
"""
import gradio as gr
import logging
from ..core.agent import AutonomousResearchAgent
try:
    from config.config import Config
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from config.config import Config

logger = logging.getLogger(__name__)

class GradioInterface:
    """Gradio web interface for the research agent"""
    
    def __init__(self, config: Config):
        self.config = config
        self.agent = AutonomousResearchAgent(config)
        
    def process_research_query_streaming(self, query):
        """Process research query with streaming updates"""
        try:
            for response_text, steps_text in self.agent.process_query_streaming(query):
                yield response_text, steps_text
        except Exception as e:
            logger.error(f"Error in processing query: {e}")
            yield f"❌ Error: {str(e)}", "Execution failed."
    
    def create_interface(self) -> gr.Blocks:
        """Create and return the Gradio interface"""
        
        with gr.Blocks(theme=gr.themes.Soft(), title="ArXiv Research Agent") as demo:
            gr.Markdown("# 🔬 Enhanced ArXiv Research Agent")
            gr.Markdown("Enter your research question and watch the agent extract key results, methodology, and conclusions from research papers!")
            
            with gr.Row():
                with gr.Column():
                    query_input = gr.Textbox(
                        label="Research Query",
                        placeholder="e.g., 'latest developments in large language models'",
                        lines=2
                    )
                    submit_btn = gr.Button("🔍 Start Enhanced Research", variant="primary", size="lg")
            
            with gr.Row():
                with gr.Column(scale=3):
                    response_output = gr.Markdown(
                        label="Research Results with Extracted Content",
                        value="🎯 **Ready to start enhanced research!**\n\nEnter your query above and click 'Start Enhanced Research' to begin extracting key results, methodology, and conclusions from research papers...",
                        height=600
                    )
                
                with gr.Column(scale=2):
                    steps_output = gr.Markdown(
                        label="Live Agent Steps",
                        value="📋 **Enhanced agent steps will appear here...**\n\nReal-time execution progress including content extraction will be shown as the agent works.",
                        height=600
                    )
            
            # Connect the streaming function
            submit_btn.click(
                fn=self.process_research_query_streaming,
                inputs=[query_input],
                outputs=[response_output, steps_output]
            )
            
            # Example queries
            gr.Examples(
                examples=[
                    "latest research on transformer architectures",
                    "quantum computing applications in machine learning", 
                    "computer vision for medical imaging",
                    "reinforcement learning in robotics",
                    "attention mechanisms in neural networks",
                    "graph neural networks for drug discovery"
                ],
                inputs=query_input
            )
            
            # Add usage instructions
            with gr.Accordion("📖 How to Use Enhanced Agent", open=False):
                gr.Markdown("""
                ### Enhanced Research Agent Features:

                - **Multi-Source Search**: Searches ArXiv, Google Scholar, Semantic Scholar, CrossRef, and more
                - **Visual Content Extraction**: Automatically extracts charts, tables, and diagrams from papers
                - **Live Updates**: Watch each step execute in real-time
                - **Progress Tracking**: See current progress and remaining steps
                - **Detailed Logging**: View reasoning and results for each step
                - **Enhanced AI Analysis**: Uses Claude to analyze papers with extracted content
                - **Structured Results**: Presents findings with quantitative results and methodologies
                - **Conversation Context**: Maintains context for follow-up questions
                
                ### Tips for Better Results:
                - Be specific in your research queries
                - Use academic terminology when possible
                - Try different phrasings if results aren't satisfactory
                - The agent works best with technical/research-oriented questions
                - Content extraction works best with recent ArXiv papers
                - Ask follow-up questions to dive deeper into specific aspects
                """)
        
        return demo
    
    def launch(self, **kwargs):
        """Launch the Gradio interface"""
        # Override default config with any provided kwargs
        launch_config = {
            'server_name': self.config.GRADIO_SERVER_NAME,
            'server_port': self.config.GRADIO_SERVER_PORT,
            'share': self.config.GRADIO_SHARE,
            'inbrowser': True,
            'show_error': True,
            'debug': self.config.GRADIO_DEBUG,
            'quiet': False
        }
        launch_config.update(kwargs)
        
        demo = self.create_interface()
        logger.info(f"Launching Gradio interface on {launch_config['server_name']}:{launch_config['server_port']}")
        demo.launch(**launch_config) 