"""
LLM Evaluation Metrics
Custom metrics for evaluating chatbot performance.
"""

from typing import List, Dict, Any
import re


class EvaluationMetrics:
    """Custom evaluation metrics for LLM responses."""
    
    @staticmethod
    def keyword_presence(response: str, keywords: List[str]) -> float:
        """
        Calculate percentage of expected keywords present in response.
        
        Args:
            response: LLM response text
            keywords: List of expected keywords
            
        Returns:
            Score between 0 and 1
        """
        if not keywords:
            return 1.0
        
        response_lower = response.lower()
        found = sum(1 for kw in keywords if kw.lower() in response_lower)
        return found / len(keywords)
    
    @staticmethod
    def response_length_score(response: str, min_words: int = 20, max_words: int = 500) -> float:
        """
        Score response based on appropriate length.
        
        Args:
            response: LLM response text
            min_words: Minimum expected words
            max_words: Maximum expected words
            
        Returns:
            Score between 0 and 1
        """
        word_count = len(response.split())
        
        if word_count < min_words:
            return word_count / min_words
        elif word_count > max_words:
            return max(0, 1 - (word_count - max_words) / max_words)
        else:
            return 1.0
    
    @staticmethod
    def coherence_score(response: str) -> float:
        """
        Simple coherence scoring based on structure.
        
        Args:
            response: LLM response text
            
        Returns:
            Score between 0 and 1
        """
        if not response or len(response) < 10:
            return 0.0
        
        score = 0.0
        
        # Check for proper sentence structure
        if '.' in response or '!' in response or '?' in response:
            score += 0.3
        
        # Check for reasonable length
        if 20 <= len(response.split()) <= 500:
            score += 0.3
        
        # Check for proper capitalization
        if response[0].isupper():
            score += 0.2
        
        # Check for lack of repetition
        words = response.lower().split()
        unique_ratio = len(set(words)) / len(words) if words else 0
        if unique_ratio > 0.5:
            score += 0.2
        
        return min(score, 1.0)
    
    @staticmethod
    def relevance_score(question: str, response: str) -> float:
        """
        Score relevance of response to question (simple keyword overlap).
        
        Args:
            question: User question
            response: LLM response
            
        Returns:
            Score between 0 and 1
        """
        # Extract keywords from question (simple approach)
        question_words = set(re.findall(r'\b\w+\b', question.lower()))
        # Remove common stop words
        stop_words = {'what', 'is', 'the', 'a', 'an', 'how', 'why', 'when', 'where', 'who', 'do', 'does', 'can', 'will'}
        question_words -= stop_words
        
        if not question_words:
            return 0.5  # Neutral score if no keywords
        
        response_words = set(re.findall(r'\b\w+\b', response.lower()))
        
        overlap = len(question_words & response_words)
        return overlap / len(question_words)
    
    @staticmethod
    def calculate_overall_score(metrics: Dict[str, float], weights: Dict[str, float] = None) -> float:
        """
        Calculate weighted overall score.
        
        Args:
            metrics: Dictionary of metric scores
            weights: Optional custom weights
            
        Returns:
            Overall score between 0 and 1
        """
        if weights is None:
            weights = {
                'keyword_score': 0.3,
                'coherence_score': 0.3,
                'relevance_score': 0.2,
                'length_score': 0.2
            }
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric, score in metrics.items():
            if metric in weights:
                total_score += score * weights[metric]
                total_weight += weights[metric]
        
        return total_score / total_weight if total_weight > 0 else 0.0


# Convenience functions
def evaluate_response(
    question: str,
    response: str,
    expected_keywords: List[str] = None
) -> Dict[str, Any]:
    """
    Evaluate a single response with multiple metrics.
    
    Args:
        question: User question
        response: LLM response
        expected_keywords: Optional expected keywords
        
    Returns:
        Dictionary of evaluation metrics
    """
    metrics_calc = EvaluationMetrics()
    
    metrics = {
        'coherence_score': metrics_calc.coherence_score(response),
        'length_score': metrics_calc.response_length_score(response),
        'relevance_score': metrics_calc.relevance_score(question, response)
    }
    
    if expected_keywords:
        metrics['keyword_score'] = metrics_calc.keyword_presence(response, expected_keywords)
    
    metrics['overall_score'] = metrics_calc.calculate_overall_score(metrics)
    
    return metrics
