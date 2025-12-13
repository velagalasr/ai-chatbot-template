"""
Evaluation script for the chatbot system.
Tests chatbot performance using various metrics.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import AgentManager
from src.rag import RAGManager
from src.utils import get_config, setup_logger

logger = setup_logger(name="evaluation", level="INFO")


class ChatbotEvaluator:
    """Evaluates chatbot performance."""
    
    def __init__(self):
        """Initialize the evaluator."""
        self.config = get_config()
        self.eval_config = self.config.get_evaluation_config()
        
        # Initialize components
        self.rag_manager = RAGManager()
        retriever = self.rag_manager.get_retriever() if self.rag_manager.enabled else None
        self.agent_manager = AgentManager(rag_retriever=retriever)
        
        # Load test set
        self.test_set = self._load_test_set()
    
    def _load_test_set(self) -> List[Dict[str, Any]]:
        """Load test dataset."""
        test_set_path = Path(self.eval_config.get('test_set_path', './data/evaluation/test_set.json'))
        
        if not test_set_path.exists():
            logger.warning(f"Test set not found: {test_set_path}")
            logger.info("Creating sample test set...")
            return self._create_sample_test_set(test_set_path)
        
        with open(test_set_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _create_sample_test_set(self, path: Path) -> List[Dict[str, Any]]:
        """Create a sample test set."""
        sample_tests = [
            {
                "question": "What is artificial intelligence?",
                "expected_keywords": ["AI", "machine", "learning", "computer", "intelligence"],
                "context": "General AI question"
            },
            {
                "question": "How does machine learning work?",
                "expected_keywords": ["data", "algorithm", "pattern", "model", "training"],
                "context": "Technical ML question"
            },
            {
                "question": "What are the benefits of using AI?",
                "expected_keywords": ["efficiency", "automation", "accuracy", "productivity"],
                "context": "Benefits question"
            }
        ]
        
        # Save sample test set
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(sample_tests, f, indent=2)
        
        logger.info(f"Created sample test set at {path}")
        return sample_tests
    
    def evaluate_response_quality(
        self,
        question: str,
        response: str,
        expected_keywords: List[str]
    ) -> Dict[str, Any]:
        """
        Evaluate response quality.
        
        Args:
            question: Test question
            response: Chatbot response
            expected_keywords: Expected keywords in response
            
        Returns:
            Evaluation metrics
        """
        # Keyword presence
        response_lower = response.lower()
        keywords_found = sum(1 for kw in expected_keywords if kw.lower() in response_lower)
        keyword_score = keywords_found / len(expected_keywords) if expected_keywords else 0
        
        # Response length check
        word_count = len(response.split())
        length_adequate = 20 <= word_count <= 500
        
        # Basic coherence check (simple heuristics)
        has_proper_sentences = '.' in response or '!' in response or '?' in response
        not_too_short = len(response) > 10
        
        coherence_score = (has_proper_sentences + not_too_short + length_adequate) / 3
        
        return {
            "keyword_score": keyword_score,
            "keywords_found": keywords_found,
            "total_keywords": len(expected_keywords),
            "word_count": word_count,
            "length_adequate": length_adequate,
            "coherence_score": coherence_score,
            "overall_score": (keyword_score + coherence_score) / 2
        }
    
    def run_evaluation(self, agent_name: str = None) -> Dict[str, Any]:
        """
        Run evaluation on test set.
        
        Args:
            agent_name: Optional specific agent to evaluate
            
        Returns:
            Evaluation results
        """
        logger.info("Starting evaluation...")
        
        if agent_name:
            logger.info(f"Evaluating agent: {agent_name}")
        else:
            agent_name = self.agent_manager.current_agent_name
            logger.info(f"Evaluating default agent: {agent_name}")
        
        results = {
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "test_count": len(self.test_set),
            "tests": [],
            "summary": {}
        }
        
        total_scores = {
            "keyword_score": 0,
            "coherence_score": 0,
            "overall_score": 0
        }
        
        for i, test_case in enumerate(self.test_set, 1):
            logger.info(f"Running test {i}/{len(self.test_set)}: {test_case['question'][:50]}...")
            
            try:
                # Get response
                start_time = datetime.now()
                response = self.agent_manager.chat(test_case['question'], agent_name=agent_name)
                end_time = datetime.now()
                latency = (end_time - start_time).total_seconds()
                
                # Evaluate response
                metrics = self.evaluate_response_quality(
                    test_case['question'],
                    response,
                    test_case.get('expected_keywords', [])
                )
                
                metrics['latency'] = latency
                
                # Store result
                test_result = {
                    "test_id": i,
                    "question": test_case['question'],
                    "response": response,
                    "context": test_case.get('context', ''),
                    "metrics": metrics
                }
                results['tests'].append(test_result)
                
                # Accumulate scores
                total_scores["keyword_score"] += metrics["keyword_score"]
                total_scores["coherence_score"] += metrics["coherence_score"]
                total_scores["overall_score"] += metrics["overall_score"]
                
                logger.info(f"Test {i} completed - Score: {metrics['overall_score']:.2f}")
            
            except Exception as e:
                logger.error(f"Error in test {i}: {e}")
                results['tests'].append({
                    "test_id": i,
                    "question": test_case['question'],
                    "error": str(e)
                })
        
        # Calculate averages
        test_count = len(self.test_set)
        results['summary'] = {
            "avg_keyword_score": total_scores["keyword_score"] / test_count,
            "avg_coherence_score": total_scores["coherence_score"] / test_count,
            "avg_overall_score": total_scores["overall_score"] / test_count,
            "tests_passed": sum(1 for t in results['tests'] if 'metrics' in t and t['metrics']['overall_score'] >= 0.5),
            "tests_failed": sum(1 for t in results['tests'] if 'error' in t or ('metrics' in t and t['metrics']['overall_score'] < 0.5))
        }
        
        logger.info("Evaluation complete!")
        logger.info(f"Average Overall Score: {results['summary']['avg_overall_score']:.2f}")
        
        return results
    
    def save_results(self, results: Dict[str, Any]):
        """Save evaluation results."""
        output_path = Path(self.eval_config.get('output_path', './data/evaluation/results'))
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"evaluation_{results['agent']}_{timestamp}.json"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to: {filepath}")
        
        # Also save summary
        summary_file = output_path / "latest_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"Evaluation Summary\n")
            f.write(f"==================\n\n")
            f.write(f"Agent: {results['agent']}\n")
            f.write(f"Timestamp: {results['timestamp']}\n")
            f.write(f"Tests: {results['test_count']}\n\n")
            f.write(f"Average Keyword Score: {results['summary']['avg_keyword_score']:.2f}\n")
            f.write(f"Average Coherence Score: {results['summary']['avg_coherence_score']:.2f}\n")
            f.write(f"Average Overall Score: {results['summary']['avg_overall_score']:.2f}\n\n")
            f.write(f"Tests Passed: {results['summary']['tests_passed']}\n")
            f.write(f"Tests Failed: {results['summary']['tests_failed']}\n")
        
        logger.info(f"Summary saved to: {summary_file}")


def main():
    """Main evaluation function."""
    logger.info("=" * 60)
    logger.info("Chatbot Evaluation Script")
    logger.info("=" * 60)
    
    try:
        # Initialize evaluator
        evaluator = ChatbotEvaluator()
        
        # Run evaluation
        results = evaluator.run_evaluation()
        
        # Save results
        evaluator.save_results(results)
        
        # Print summary
        print("\n" + "=" * 60)
        print("EVALUATION SUMMARY")
        print("=" * 60)
        print(f"Agent: {results['agent']}")
        print(f"Tests: {results['test_count']}")
        print(f"Average Overall Score: {results['summary']['avg_overall_score']:.2%}")
        print(f"Tests Passed: {results['summary']['tests_passed']}")
        print(f"Tests Failed: {results['summary']['tests_failed']}")
        print("=" * 60)
    
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
