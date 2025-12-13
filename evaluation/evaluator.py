"""
Chatbot Evaluator
Main evaluation framework.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import AgentManager
from src.rag import RAGManager
from src.utils import get_config, get_logger
from .metrics import evaluate_response

logger = get_logger(__name__)


class Evaluator:
    """Main evaluator class."""
    
    def __init__(self):
        """Initialize evaluator."""
        self.config = get_config()
        self.eval_config = self.config.get_evaluation_config()
        
        # Initialize components
        self.rag_manager = RAGManager()
        retriever = self.rag_manager.get_retriever() if self.rag_manager.enabled else None
        self.agent_manager = AgentManager(rag_retriever=retriever)
    
    def evaluate_test_set(
        self,
        test_set: List[Dict[str, Any]],
        agent_name: str = None
    ) -> Dict[str, Any]:
        """
        Evaluate chatbot on a test set.
        
        Args:
            test_set: List of test cases
            agent_name: Optional specific agent to evaluate
            
        Returns:
            Evaluation results
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'agent': agent_name or self.agent_manager.current_agent_name,
            'test_count': len(test_set),
            'tests': []
        }
        
        for test_case in test_set:
            question = test_case['question']
            expected_keywords = test_case.get('expected_keywords', [])
            
            try:
                # Get response
                response = self.agent_manager.chat(question, agent_name=agent_name)
                
                # Evaluate
                metrics = evaluate_response(question, response, expected_keywords)
                
                results['tests'].append({
                    'question': question,
                    'response': response,
                    'metrics': metrics,
                    'passed': metrics['overall_score'] >= 0.5
                })
            
            except Exception as e:
                logger.error(f"Error evaluating question: {e}")
                results['tests'].append({
                    'question': question,
                    'error': str(e),
                    'passed': False
                })
        
        # Calculate summary
        passed = sum(1 for t in results['tests'] if t.get('passed', False))
        results['summary'] = {
            'passed': passed,
            'failed': len(test_set) - passed,
            'pass_rate': passed / len(test_set) if test_set else 0
        }
        
        return results
    
    def save_results(self, results: Dict[str, Any], output_path: str = None):
        """Save evaluation results."""
        if output_path is None:
            output_dir = Path(self.eval_config.get('output_path', './data/evaluation/results'))
            output_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = output_dir / f"eval_{timestamp}.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to {output_path}")
