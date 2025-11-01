from flask import Flask, request, jsonify
from flask_cors import CORS
from query_processor import QueryProcessor
from data_fetcher import DataFetcher
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
data_fetcher = DataFetcher()
query_processor = QueryProcessor()

@app.route('/api/query', methods=['POST'])
def handle_query():
    """
    Main endpoint to handle user questions
    """
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        logger.info(f"Processing question: {question}")
        
        # Step 1: Analyze the question using LLM
        query_plan = query_processor.analyze_question(question)
        logger.info(f"Query plan: {query_plan}")
        
        # Step 2: Fetch relevant data
        fetched_data = data_fetcher.fetch_data(query_plan)
        
        # Step 3: Generate answer with citations
        answer, citations = query_processor.generate_answer(
            question, 
            query_plan, 
            fetched_data
        )
        
        return jsonify({
            'answer': answer,
            'citations': citations,
            'query_plan': query_plan
        })
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({
            'error': str(e),
            'answer': 'Sorry, I encountered an error processing your question. Please try again.'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Project Samarth API is running'})

@app.route('/api/datasets', methods=['GET'])
def list_datasets():
    """List available datasets"""
    datasets = data_fetcher.list_available_datasets()
    return jsonify({'datasets': datasets})

if __name__ == '__main__':
    logger.info("Starting Project Samarth API...")
    app.run(debug=True, host='0.0.0.0', port=5000)