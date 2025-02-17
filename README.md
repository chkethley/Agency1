# Agency1 Usage Guide

## Installation

### Standard Installation

```bash
pip install agency1
```

### Development Installation

```bash
git clone https://github.com/agency1/agency1.git
cd agency1
pip install -e ".[dev]"
```

## Command Line Interface

Agency1 provides a comprehensive command-line interface for direct interaction.

### Starting Interactive Mode

```bash
agency1 --interactive
```

This launches the CLI interface with the following commands:

- `process <signal>`: Process a signal through the neural processor
- `recall <key>`: Recall a memory from storage
- `store <key> <data> [--long-term]`: Store a memory
- `consolidate`: Manually trigger memory consolidation
- `stats`: View processing performance statistics
- `metadata [--verbose]`: Show system metadata
- `exit`: Exit the program

### Running with Custom Configuration

```bash
agency1 --config /path/to/config.json
```

## Programmatic Usage

### Basic Usage

```python
from agency1 import AgencyController

# Initialize with default configuration
controller = AgencyController()

# Process a simple task
result = controller.process_task({
    'id': 'task-001',
    'content': 'This is the content to process',
    'requires_context': False
})

print(result)
```

### With Custom Configuration

```python
from agency1 import AgencyController

# Initialize with custom configuration
controller = AgencyController(config_path='/path/to/config.json')

# Start the interactive mode
controller.start_interactive()
```

### Working with Memory

```python
from agency1 import AgencyController

controller = AgencyController()

# Store memory
controller.memory.store_memory('key1', 'This is important information', long_term=True)

# Recall memory
data = controller.memory.recall_memory('key1')
print(data)

# Trigger consolidation
controller.memory.auto_consolidate()
```

### Using External Services

```python
from agency1 import AgencyController

controller = AgencyController()

# Get context from API
context = controller.api_service.get_context('context-123')

# Store result in persistent storage
controller.storage_service.store_result('task-456', {'status': 'completed'})

# Retrieve stored result
result = controller.storage_service.retrieve_result('task-456')
```

## Configuration

### Configuration File Format

Configuration files use JSON format:

```json
{
  "log_level": "INFO",
  "console_logging": true,
  "log_file": "agency1.log",
  
  "memory": {
    "short_term_capacity": 100,
    "persistence_file": "data/long_term_memory.json",
    "consolidation_interval": 3600
  },
  
  "processor": {
    "quality_threshold": 0.75,
    "default_pathway": "standard"
  },
  
  "api": {
    "base_url": "https://api.example.com",
    "timeout": 30,
    "retry_attempts": 3,
    "api_key": "your-api-key-here"
  },
  
  "storage": {
    "location": "data/",
    "backup_interval": 86400
  }
}
```

### Environment Variables

You can also configure Agency1 using environment variables:

```bash
# Set log level
export AGENCY1_LOG_LEVEL=DEBUG

# Set API key
export AGENCY1_API_KEY=your-api-key-here

# Start Agency1
agency1 --interactive
```

## Best Practices

1. **Memory Management**:
   - Use short-term memory for transient information
   - Only store essential information in long-term memory
   - Regularly consolidate memory to optimize performance

2. **Signal Processing**:
   - Use the appropriate pathway for your signals
   - Provide clear, well-structured input for best results
   - Check quality metrics to identify processing issues

3. **Integration**:
   - Use API service for real-time external data
   - Use storage service for persistence
   - Configure appropriate timeout and retry settings for your environment

4. **Backup Strategy**:
   - The storage service automatically backs up data
   - Configure backup_interval based on your data criticality
   - For mission-critical applications, consider additional external backups
