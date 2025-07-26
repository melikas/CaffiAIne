import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, memory_file: str = "agent_memory.json"):
        """
        Initialize the memory manager
        
        Args:
            memory_file (str): Path to the memory storage file
        """
        self.memory_file = memory_file
        self.memory_data = self._load_memory()
        logger.info(f"Memory manager initialized with file: {memory_file}")
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    'conversations': [],
                    'task_results': [],
                    'user_preferences': {},
                    'learned_patterns': [],
                    'metadata': {
                        'created_at': datetime.now().isoformat(),
                        'version': '1.0'
                    }
                }
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            return {
                'conversations': [],
                'task_results': [],
                'user_preferences': {},
                'learned_patterns': [],
                'metadata': {
                    'created_at': datetime.now().isoformat(),
                    'version': '1.0'
                }
            }
    
    def _save_memory(self):
        """Save memory to file"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory_data, f, indent=2, ensure_ascii=False)
            logger.info("Memory saved successfully")
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def store_conversation(self, user_input: str, agent_response: str, 
                          task_results: Optional[List[Dict]] = None):
        """
        Store a conversation interaction
        
        Args:
            user_input (str): User's input
            agent_response (str): Agent's response
            task_results (List[Dict], optional): Results from task execution
        """
        conversation = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'agent_response': agent_response,
            'task_results': task_results or [],
            'id': self._generate_id(user_input + agent_response)
        }
        
        self.memory_data['conversations'].append(conversation)
        self._save_memory()
        logger.info(f"Stored conversation with ID: {conversation['id']}")
    
    def store_task_result(self, task_description: str, result: Dict[str, Any]):
        """
        Store a task execution result
        
        Args:
            task_description (str): Description of the task
            result (Dict[str, Any]): Task execution result
        """
        task_record = {
            'timestamp': datetime.now().isoformat(),
            'task_description': task_description,
            'result': result,
            'id': self._generate_id(task_description)
        }
        
        self.memory_data['task_results'].append(task_record)
        self._save_memory()
        logger.info(f"Stored task result for: {task_description}")
    
    def store_user_preference(self, key: str, value: Any):
        """
        Store user preferences
        
        Args:
            key (str): Preference key
            value (Any): Preference value
        """
        self.memory_data['user_preferences'][key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        self._save_memory()
        logger.info(f"Stored user preference: {key} = {value}")
    
    def recall_conversations(self, limit: int = 5) -> List[Dict]:
        """
        Recall recent conversations
        
        Args:
            limit (int): Number of conversations to recall
            
        Returns:
            List[Dict]: Recent conversations
        """
        conversations = self.memory_data['conversations']
        return conversations[-limit:] if conversations else []
    
    def recall_task_results(self, task_keyword: str = None, limit: int = 10) -> List[Dict]:
        """
        Recall task results, optionally filtered by keyword
        
        Args:
            task_keyword (str, optional): Keyword to filter tasks
            limit (int): Number of results to return
            
        Returns:
            List[Dict]: Task results
        """
        results = self.memory_data['task_results']
        
        if task_keyword:
            filtered_results = [
                result for result in results 
                if task_keyword.lower() in result['task_description'].lower()
            ]
        else:
            filtered_results = results
        
        return filtered_results[-limit:] if filtered_results else []
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """
        Get all user preferences
        
        Returns:
            Dict[str, Any]: User preferences
        """
        return self.memory_data['user_preferences']
    
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """
        Get a specific user preference
        
        Args:
            key (str): Preference key
            default (Any): Default value if preference not found
            
        Returns:
            Any: Preference value
        """
        preferences = self.memory_data['user_preferences']
        if key in preferences:
            return preferences[key]['value']
        return default
    
    def learn_pattern(self, pattern_type: str, pattern_data: Dict[str, Any]):
        """
        Learn and store patterns from interactions
        
        Args:
            pattern_type (str): Type of pattern
            pattern_data (Dict[str, Any]): Pattern data
        """
        pattern = {
            'type': pattern_type,
            'data': pattern_data,
            'timestamp': datetime.now().isoformat(),
            'frequency': 1
        }
        
        # Check if pattern already exists
        existing_patterns = [
            p for p in self.memory_data['learned_patterns'] 
            if p['type'] == pattern_type
        ]
        
        if existing_patterns:
            # Update existing pattern
            existing_patterns[0]['frequency'] += 1
            existing_patterns[0]['data'].update(pattern_data)
        else:
            # Add new pattern
            self.memory_data['learned_patterns'].append(pattern)
        
        self._save_memory()
        logger.info(f"Learned pattern: {pattern_type}")
    
    def get_learned_patterns(self, pattern_type: str = None) -> List[Dict]:
        """
        Get learned patterns, optionally filtered by type
        
        Args:
            pattern_type (str, optional): Type of pattern to filter
            
        Returns:
            List[Dict]: Learned patterns
        """
        patterns = self.memory_data['learned_patterns']
        
        if pattern_type:
            return [p for p in patterns if p['type'] == pattern_type]
        
        return patterns
    
    def _generate_id(self, content: str) -> str:
        """Generate a unique ID for content"""
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def clear_memory(self):
        """Clear all memory data"""
        self.memory_data = {
            'conversations': [],
            'task_results': [],
            'user_preferences': {},
            'learned_patterns': [],
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'version': '1.0'
            }
        }
        self._save_memory()
        logger.info("Memory cleared")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics
        
        Returns:
            Dict[str, Any]: Memory statistics
        """
        return {
            'total_conversations': len(self.memory_data['conversations']),
            'total_task_results': len(self.memory_data['task_results']),
            'total_user_preferences': len(self.memory_data['user_preferences']),
            'total_learned_patterns': len(self.memory_data['learned_patterns']),
            'memory_size_mb': os.path.getsize(self.memory_file) / (1024 * 1024) if os.path.exists(self.memory_file) else 0
        }

# Global memory manager instance
memory_manager = None

def get_memory_manager() -> MemoryManager:
    """Get or create the global memory manager instance"""
    global memory_manager
    if memory_manager is None:
        memory_manager = MemoryManager()
    return memory_manager

def store_conversation(user_input: str, agent_response: str, task_results: Optional[List[Dict]] = None):
    """Convenience function to store a conversation"""
    get_memory_manager().store_conversation(user_input, agent_response, task_results)

def store_task_result(task_description: str, result: Dict[str, Any]):
    """Convenience function to store a task result"""
    get_memory_manager().store_task_result(task_description, result)

def recall_conversations(limit: int = 5) -> List[Dict]:
    """Convenience function to recall conversations"""
    return get_memory_manager().recall_conversations(limit)

def recall_task_results(task_keyword: str = None, limit: int = 10) -> List[Dict]:
    """Convenience function to recall task results"""
    return get_memory_manager().recall_task_results(task_keyword, limit)

def get_user_preferences() -> Dict[str, Any]:
    """Convenience function to get user preferences"""
    return get_memory_manager().get_user_preferences()

def get_user_preference(key: str, default: Any = None) -> Any:
    """Convenience function to get a specific user preference"""
    return get_memory_manager().get_user_preference(key, default)
