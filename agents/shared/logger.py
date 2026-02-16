"""
Shared logging utility for all MindBridge agents.
Provides centralized, structured logging with automatic rotation.
"""
import logging
import os
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)


def get_logger(agent_name):
    """
    Get a configured logger for an agent.
    
    Args:
        agent_name: Name of the agent (e.g., 'mentor', 'job_hunter', 'auto_apply')
    
    Returns:
        logging.Logger: Configured logger instance
    
    Example:
        >>> from agents.shared.logger import get_logger
        >>> logger = get_logger('mentor')
        >>> logger.info("Quiz session started")
    """
    logger = logging.getLogger(agent_name)
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # File handler - daily log file
        log_file = LOGS_DIR / f"{agent_name}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler - for real-time feedback
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter - structured logging
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def log_session(agent_name, session_type, details):
    """
    Log a session with structured data.
    
    Args:
        agent_name: Name of the agent
        session_type: Type of session (e.g., 'quiz', 'interview', 'job_search')
        details: Dictionary of session details
    
    Example:
        >>> log_session('mentor', 'quiz', {
        ...     'score': '5/5',
        ...     'duration_minutes': 8,
        ...     'topics': ['Docker', 'PostgreSQL']
        ... })
    """
    logger = get_logger(agent_name)
    
    # Format details for logging
    details_str = " | ".join([f"{k}={v}" for k, v in details.items()])
    
    logger.info(f"{session_type.upper()} | {details_str}")


def log_error(agent_name, error_type, error_message, context=None):
    """
    Log an error with context.
    
    Args:
        agent_name: Name of the agent
        error_type: Type of error (e.g., 'DatabaseError', 'APIError')
        error_message: Error message
        context: Optional context dictionary
    
    Example:
        >>> log_error('mentor', 'DatabaseError', 'Failed to connect', 
        ...           {'db_path': '/path/to/db'})
    """
    logger = get_logger(agent_name)
    
    context_str = ""
    if context:
        context_str = " | " + " | ".join([f"{k}={v}" for k, v in context.items()])
    
    logger.error(f"{error_type} | {error_message}{context_str}")


# Example usage and testing
if __name__ == "__main__":
    # Test the logger
    print("Testing MindBridge Shared Logger...")
    print(f"Logs directory: {LOGS_DIR}")
    print()
    
    # Test mentor agent logging
    logger = get_logger('mentor')
    logger.info("Mentor agent initialized")
    
    log_session('mentor', 'quiz', {
        'score': '5/5',
        'duration_minutes': 8,
        'cards_reviewed': 5,
        'perfect_recalls': 5
    })
    
    log_error('mentor', 'DatabaseError', 'Connection timeout', {
        'db_path': 'agents/mentor/mentor.db',
        'retry_attempt': 1
    })
    
    print(f"\n✅ Logs written to: {LOGS_DIR}")
    print(f"   Check: {LOGS_DIR / 'mentor.log'}")
