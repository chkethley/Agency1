# Agency1/main.py
import logging
import json
import os
from typing import Dict, Any, Optional

from brain_v4.core.memory import EnhancedHippocampus
from brain_v4.core.processing import NeuralProcessor
from brain_v4.interfaces.cli import CLIInterface
from brain_v4.utils.metadata_manager import MetadataManager

from integrations.api_service import APIService
from integrations.storage_service import StorageService

class AgencyController:
    """Main controller for Agency1 operations"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self._setup_logging()
        
        # Initialize brain components
        self.memory = EnhancedHippocampus(self.config.get('memory', {}))
        self.processor = NeuralProcessor(self.config.get('processor', {}), self.memory)
        self.metadata = MetadataManager(self.config.get('metadata', {}))
        
        # Initialize integration services
        self.api_service = APIService(self.config.get('api', {}))
        self.storage_service = StorageService(self.config.get('storage', {}))
        
        self.logger.info("Agency1 system initialized successfully")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
        default_path = os.path.join(os.path.dirname(__file__), 'brain_v4/config/default_config.json')
        try:
            with open(default_path, 'r') as f:
                default_config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            default_config = {}
        
        # Add Agency1-specific defaults
        default_config.update({
            'api': {
                'base_url': 'https://api.example.com',
                'timeout': 30,
                'retry_attempts': 3
            },
            'storage': {
                'location': 'data/',
                'backup_interval': 86400  # 24 hours
            }
        })
        
        return default_config
    
    def _setup_logging(self):
        """Configure logging for Agency1"""
        log_level = getattr(logging, self.config.get('log_level', 'INFO'))
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        logging.basicConfig(
            level=log_level,
            format=log_format,
            filename=self.config.get('log_file'),
            filemode='a'
        )
        
        # Create console handler if requested
        if self.config.get('console_logging', True):
            console = logging.StreamHandler()
            console.setLevel(log_level)
            formatter = logging.Formatter(log_format)
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
        
        self.logger = logging.getLogger('Agency1')
    
    def start_interactive(self):
        """Start the interactive CLI interface"""
        cli = CLIInterface(self.processor, self.memory, self.metadata)
        cli.start()
    
    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task through the Agency1 pipeline"""
        self.logger.info(f"Processing task: {task_data.get('id', 'unknown')}")
        
        # Get additional context from API if needed
        if task_data.get('requires_context', False):
            context = self.api_service.get_context(task_data.get('context_id'))
            task_data['context'] = context
        
        # Process the main signal
        result = self.processor.process_signal(task_data.get('content', ''))
        
        # Store results if processing was successful
        if result:
            task_id = task_data.get('id', str(hash(task_data.get('content', ''))))
            self.storage_service.store_result(task_id, result)
            
            response = {
                'success': True,
                'task_id': task_id,
                'result': result,
                'metadata': self.metadata.get_all(verbose=False)
            }
        else:
            response = {
                'success': False,
                'error': 'Processing failed or input was invalid',
                'metadata': self.metadata.get_all(verbose=False)
            }
            
        self.logger.info(f"Task processing complete: {response['success']}")
        return response


def main():
    """Entry point for Agency1"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Agency1 - Advanced Neural Processing System')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--interactive', action='store_true', help='Start in interactive mode')
    args = parser.parse_args()
    
    controller = AgencyController(config_path=args.config)
    
    if args.interactive:
        controller.start_interactive()
    else:
        # Default to processing a simple test task
        test_task = {
            'id': 'test-001',
            'content': 'This is a test task for Agency1',
            'requires_context': False
        }
        result = controller.process_task(test_task)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()