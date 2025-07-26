import logging
from typing import List, Dict, Any
from executor import execute_task
from memory import recall_conversations, recall_task_results, get_user_preferences

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskPlanner:
    def __init__(self):
        """Initialize the task planner"""
        logger.info("Task planner initialized")
    
    def plan_tasks(self, user_input: str) -> List[Dict[str, Any]]:
        """
        Plan tasks based on user input using Gemini API
        
        Args:
            user_input (str): User's request
            
        Returns:
            List[Dict[str, Any]]: List of planned tasks with metadata
        """
        try:
            # Get context from memory
            recent_conversations = recall_conversations(limit=3)
            user_preferences = get_user_preferences()
            
            # Build context for planning
            context = {
                'recent_conversations': recent_conversations,
                'user_preferences': user_preferences,
                'user_input': user_input
            }
            
            # Use Gemini API to plan tasks
            planning_prompt = f"""
            Analyze the user's request and break it down into specific, actionable tasks.
            
            User Request: {user_input}
            
            Recent Conversations: {recent_conversations}
            User Preferences: {user_preferences}
            
            Please provide a JSON response with the following structure:
            {{
                "tasks": [
                    {{
                        "id": "task_1",
                        "description": "Detailed task description",
                        "priority": 1,
                        "dependencies": [],
                        "estimated_time": "5 minutes",
                        "tools_needed": ["gemini_api", "memory"],
                        "success_criteria": "What defines success for this task"
                    }}
                ],
                "overall_goal": "The main objective",
                "estimated_total_time": "Total estimated time",
                "complexity": "low/medium/high"
            }}
            
            Focus on creating specific, measurable tasks that can be executed by an AI agent.
            Consider user preferences and past interactions when planning.
            """
            
            # Execute planning task
            planning_result = execute_task(planning_prompt, context)
            
            if planning_result['status'] == 'success':
                # Parse the response (assuming it returns JSON-like structure)
                # In a real implementation, you'd parse the JSON response
                # For now, we'll create a structured task list
                tasks = self._create_structured_tasks(user_input, planning_result['response'])
                logger.info(f"Planned {len(tasks)} tasks for user input: {user_input}")
                return tasks
            else:
                logger.error(f"Planning failed: {planning_result.get('error', 'Unknown error')}")
                return self._create_fallback_tasks(user_input)
                
        except Exception as e:
            logger.error(f"Error in task planning: {e}")
            return self._create_fallback_tasks(user_input)
    
    def _create_structured_tasks(self, user_input: str, planning_response: str) -> List[Dict[str, Any]]:
        """
        Create structured tasks from planning response
        
        Args:
            user_input (str): Original user input
            planning_response (str): Response from Gemini API
            
        Returns:
            List[Dict[str, Any]]: Structured task list
        """
        # This is a simplified implementation
        # In a real system, you'd parse the JSON response from Gemini
        
        tasks = []
        
        # Analyze user input for common patterns
        input_lower = user_input.lower()
        
        if 'search' in input_lower or 'find' in input_lower:
            tasks.append({
                'id': 'search_task',
                'description': f'Search for information related to: {user_input}',
                'priority': 1,
                'dependencies': [],
                'estimated_time': '2-3 minutes',
                'tools_needed': ['gemini_api'],
                'success_criteria': 'Relevant information found and presented'
            })
        
        if 'analyze' in input_lower or 'analyze' in input_lower:
            tasks.append({
                'id': 'analysis_task',
                'description': f'Analyze the provided information: {user_input}',
                'priority': 2,
                'dependencies': ['search_task'],
                'estimated_time': '3-5 minutes',
                'tools_needed': ['gemini_api', 'memory'],
                'success_criteria': 'Comprehensive analysis completed'
            })
        
        if 'recommend' in input_lower or 'suggest' in input_lower:
            tasks.append({
                'id': 'recommendation_task',
                'description': f'Generate recommendations based on: {user_input}',
                'priority': 3,
                'dependencies': ['search_task', 'analysis_task'],
                'estimated_time': '2-3 minutes',
                'tools_needed': ['gemini_api', 'memory'],
                'success_criteria': 'Actionable recommendations provided'
            })
        
        # If no specific patterns found, create a general task
        if not tasks:
            tasks.append({
                'id': 'general_task',
                'description': f'Process user request: {user_input}',
                'priority': 1,
                'dependencies': [],
                'estimated_time': '3-5 minutes',
                'tools_needed': ['gemini_api'],
                'success_criteria': 'Request processed and response provided'
            })
        
        return tasks
    
    def _create_fallback_tasks(self, user_input: str) -> List[Dict[str, Any]]:
        """
        Create fallback tasks when planning fails
        
        Args:
            user_input (str): User input
            
        Returns:
            List[Dict[str, Any]]: Basic task list
        """
        return [{
            'id': 'fallback_task',
            'description': f'Process user request: {user_input}',
            'priority': 1,
            'dependencies': [],
            'estimated_time': '3-5 minutes',
            'tools_needed': ['gemini_api'],
            'success_criteria': 'Request processed and response provided'
        }]
    
    def prioritize_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prioritize tasks based on dependencies and importance
        
        Args:
            tasks (List[Dict[str, Any]]): List of tasks
            
        Returns:
            List[Dict[str, Any]]: Prioritized task list
        """
        # Sort by priority (lower number = higher priority)
        return sorted(tasks, key=lambda x: x.get('priority', 999))
    
    def validate_task_dependencies(self, tasks: List[Dict[str, Any]]) -> bool:
        """
        Validate that task dependencies are satisfied
        
        Args:
            tasks (List[Dict[str, Any]]): List of tasks
            
        Returns:
            bool: True if dependencies are valid
        """
        task_ids = {task['id'] for task in tasks}
        
        for task in tasks:
            dependencies = task.get('dependencies', [])
            for dep in dependencies:
                if dep not in task_ids:
                    logger.warning(f"Task {task['id']} depends on {dep} which doesn't exist")
                    return False
        
        return True

# Global planner instance
planner = None

def get_planner() -> TaskPlanner:
    """Get or create the global planner instance"""
    global planner
    if planner is None:
        planner = TaskPlanner()
    return planner

def plan(user_input: str) -> List[Dict[str, Any]]:
    """
    Plan tasks for user input
    
    Args:
        user_input (str): User's request
        
    Returns:
        List[Dict[str, Any]]: Planned tasks
    """
    return get_planner().plan_tasks(user_input)

def prioritize_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Prioritize a list of tasks
    
    Args:
        tasks (List[Dict[str, Any]]): Tasks to prioritize
        
    Returns:
        List[Dict[str, Any]]: Prioritized tasks
    """
    return get_planner().prioritize_tasks(tasks)

def validate_task_dependencies(tasks: List[Dict[str, Any]]) -> bool:
    """
    Validate task dependencies
    
    Args:
        tasks (List[Dict[str, Any]]): Tasks to validate
        
    Returns:
        bool: True if dependencies are valid
    """
    return get_planner().validate_task_dependencies(tasks)
