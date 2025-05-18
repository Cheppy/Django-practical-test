import asyncio
from pyppeteer import launch

import logging
import traceback

logger = logging.getLogger(__name__)

async def generate_pdf(url: str) -> bytes:
    """Generate PDF using pyppeteer
    
    Args:
        url: The URL to generate PDF from
        
    Returns:
        bytes: The generated PDF content
    """
    browser = None
    try:
        logger.info(f"Starting PDF generation for URL: {url}")
        
        browser = await launch(
            headless=True,
            handleSIGINT=False,  
            handleSIGTERM=False,  
            handleSIGHUP=False,  
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--no-zygote',  
                '--single-process'  
            ]
        )
        logger.debug("Browser launched successfully")
        
        # Create new page
        page = await browser.newPage()
        logger.debug("New page created")
        
        await page.setViewport({'width': 1200, 'height': 1600})
        logger.debug("Viewport set")
        
        await page.goto(url, {'waitUntil': 'networkidle0', 'timeout': 30000})
        logger.debug("Page loaded successfully")
        
        await page.waitForSelector('body', {'timeout': 5000})
        logger.debug("Body content loaded")
        
        pdf: bytes = await page.pdf({
            'format': 'A4',
            'printBackground': True,
            'margin': {
                'top': '20px',
                'right': '20px',
                'bottom': '20px',
                'left': '20px'
            },
            'preferCSSPageSize': True,
            'timeout': 30000
        })
        logger.info("PDF generated successfully")
        
        return pdf
        
    except Exception as e:
        logger.error(f"Error during PDF generation: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise
        
    finally:
        if browser:
            await browser.close()
            logger.debug("Browser closed")

def generate_pdf_sync(url: str) -> bytes:
    """Synchronous wrapper for generate_pdf
    
    Args:
        url: The URL to generate PDF from
        
    Returns:
        bytes: The generated PDF content
    """
    logger.info("Starting PDF generation with asyncio.run")
    try:
        loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        pdf: bytes = loop.run_until_complete(generate_pdf(url))
        
        loop.close()
        
        return pdf
        
    except Exception as e:
        logger.error(f"Error in generate_pdf_sync: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise 