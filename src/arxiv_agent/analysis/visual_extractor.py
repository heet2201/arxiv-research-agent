"""
Visual content extraction module for research papers
"""
import requests
import base64
import fitz  # PyMuPDF
import re
import logging
from typing import List
from ..core.models import VisualData

logger = logging.getLogger(__name__)

class VisualExtractor:
    """Extract visual information from PDFs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Academic-Agent/1.0'})
    
    def extract_visuals_from_paper(self, paper_url: str, max_visuals: int = 3) -> List[VisualData]:
        """
        Extract visual data from paper PDF
        
        Args:
            paper_url: URL of the research paper
            max_visuals: Maximum number of visuals to extract
            
        Returns:
            List of VisualData objects
        """
        visuals = []
        try:
            # Convert ArXiv URL to PDF URL
            pdf_url = self._convert_to_pdf_url(paper_url)
            
            # Download PDF
            response = self.session.get(pdf_url, timeout=30)
            if response.status_code != 200:
                logger.warning(f"Failed to download PDF from {pdf_url}")
                return visuals
            
            # Process PDF
            pdf_document = fitz.open(stream=response.content, filetype="pdf")
            
            # Process first 5 pages only (for performance)
            max_pages = min(5, len(pdf_document))
            for page_num in range(max_pages):
                page = pdf_document.load_page(page_num)
                
                # Extract images
                page_visuals = self._extract_images_from_page(page, page_num + 1, pdf_document)
                visuals.extend(page_visuals)
                
                # Extract tables
                table_visuals = self._extract_tables_from_page(page, page_num + 1)
                visuals.extend(table_visuals)
                
                # Stop if we have enough visuals
                if len(visuals) >= max_visuals:
                    break
            
            pdf_document.close()
            
        except Exception as e:
            logger.error(f"Error processing PDF {paper_url}: {e}")
        
        return visuals[:max_visuals]
    
    def _convert_to_pdf_url(self, paper_url: str) -> str:
        """Convert paper URL to PDF download URL"""
        if 'arxiv.org' in paper_url:
            return paper_url.replace('/abs/', '/pdf/') + '.pdf'
        # Add other conversions for different sources as needed
        return paper_url
    
    def _extract_images_from_page(self, page, page_num: int, pdf_document) -> List[VisualData]:
        """Extract images from a PDF page"""
        visuals = []
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                pix = fitz.Pixmap(pdf_document, xref)
                
                # Skip non-color images or very small images
                if pix.n - pix.alpha < 4 or pix.width < 100 or pix.height < 100:
                    pix = None
                    continue
                
                # Convert to PNG and encode in base64
                img_data = pix.tobytes("png")
                img_b64 = base64.b64encode(img_data).decode()
                
                # Get surrounding text for context
                text_blocks = page.get_text("blocks")
                context_text = self._get_image_context(text_blocks)
                
                visual = VisualData(
                    type="image",
                    description=f"Figure from page {page_num}",
                    text_content=context_text,
                    base64_image=img_b64,
                    page_number=page_num
                )
                visuals.append(visual)
                
                pix = None
                
            except Exception as e:
                logger.error(f"Error extracting image {img_index} from page {page_num}: {e}")
                continue
        
        return visuals
    
    def _extract_tables_from_page(self, page, page_num: int) -> List[VisualData]:
        """Extract table-like structures from page text"""
        tables = []
        text = page.get_text()
        
        # Find potential table content using simple heuristics
        table_candidates = self._find_table_candidates(text)
        
        for table_text in table_candidates:
            if len(table_text.strip()) > 50:  # Only include substantial tables
                table = VisualData(
                    type="table",
                    description=f"Table from page {page_num}",
                    text_content=table_text,
                    page_number=page_num
                )
                tables.append(table)
        
        return tables[:2]  # Max 2 tables per page
    
    def _get_image_context(self, text_blocks: List) -> str:
        """Get text context around an image"""
        context_texts = []
        for block in text_blocks:
            text = block[4].strip()
            # Look for figure/table captions and references
            if any(keyword in text.lower() for keyword in ['figure', 'fig', 'table', 'chart', 'graph']):
                context_texts.append(text)
        
        return ' '.join(context_texts[:2])  # First 2 relevant text blocks
    
    def _find_table_candidates(self, text: str) -> List[str]:
        """Find potential table content in text"""
        lines = text.split('\n')
        table_candidates = []
        current_table = []
        in_table = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if in_table and len(current_table) > 2:
                    # End of table
                    table_text = '\n'.join(current_table)
                    table_candidates.append(table_text)
                current_table = []
                in_table = False
                continue
            
            # Heuristics for table detection
            is_table_line = (
                len(re.findall(r'\d+\.?\d*', line)) > 2 or  # Multiple numbers
                line.count('\t') > 1 or  # Multiple tabs
                len(re.findall(r'\s{3,}', line)) > 1 or  # Multiple large spaces
                re.search(r'\|\s*\w+\s*\|', line)  # Pipe-separated values
            )
            
            if is_table_line:
                current_table.append(line)
                in_table = True
            else:
                if in_table and len(current_table) > 2:
                    # End of table
                    table_text = '\n'.join(current_table)
                    table_candidates.append(table_text)
                current_table = []
                in_table = False
        
        # Handle table at end of text
        if in_table and len(current_table) > 2:
            table_text = '\n'.join(current_table)
            table_candidates.append(table_text)
        
        return table_candidates 