import google.generativeai as genai
import json
import os
from typing import Dict, List, Tuple

class QueryProcessor:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_question(self, question: str) -> Dict:
        """
        Use Gemini to analyze the question and create a query plan
        """
        prompt = f"""You are a data analyst assistant for Indian government data.
Analyze this question and extract information in JSON format:

Question: {question}

Extract and return ONLY a JSON object with these fields:
{{
    "states": ["state1", "state2"],
    "districts": ["district1"],
    "crops": ["crop1", "crop2"],
    "crop_types": ["cereals", "pulses"],
    "time_period": {{"start_year": 2018, "end_year": 2023}},
    "data_types": ["production", "rainfall"],
    "analysis_type": "comparison",
    "key_metrics": ["top_n_crops", "average_rainfall"]
}}

Rules:
- Use full state names (e.g., "Maharashtra", "Punjab")
- Extract years mentioned or use last 5 years as default
- Identify if they want production, rainfall, area, yield data
- Analysis type can be: comparison, trend, correlation, recommendation
- Return ONLY valid JSON, no additional text
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean up response to get just JSON
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            query_plan = json.loads(text)
            return query_plan
            
        except Exception as e:
            print(f"Error in query analysis: {e}")
            # Return a basic fallback plan
            return {
                "states": [],
                "crops": [],
                "time_period": {"start_year": 2019, "end_year": 2024},
                "data_types": ["production"],
                "analysis_type": "general",
                "key_metrics": []
            }
    
    def generate_answer(self, question: str, query_plan: Dict, data: Dict) -> Tuple[str, List[Dict]]:
        """
        Generate a natural language answer from the data using Gemini
        """
        # Prepare data summary for LLM
        data_summary = self._prepare_data_summary(data)
        
        prompt = f"""You are an expert data analyst for Indian agriculture and climate data.

USER QUESTION: {question}

QUERY PLAN: {json.dumps(query_plan, indent=2)}

AVAILABLE DATA:
{data_summary}

TASK: Provide a comprehensive, accurate answer to the question using the data provided.

REQUIREMENTS:
1. Use specific numbers and statistics from the data
2. Structure your answer clearly with comparisons if needed
3. Mention which dataset each piece of information comes from
4. If data is insufficient, say so clearly
5. Keep the tone professional but accessible
6. Include year ranges when discussing trends

Provide your answer now:"""
        
        try:
            response = self.model.generate_content(prompt)
            answer = response.text
            
            # Extract citations from data sources
            citations = self._extract_citations(data)
            
            return answer, citations
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            return f"I found relevant data but encountered an error generating the answer: {str(e)}", []
    
    def _prepare_data_summary(self, data: Dict) -> str:
        """Convert data dictionary to readable summary"""
        summary = []
        for source, dataset in data.items():
            summary.append(f"\n--- {source} ---")
            if isinstance(dataset, dict) and 'data' in dataset:
                df_data = dataset['data']
                if hasattr(df_data, 'to_dict'):
                    # It's a DataFrame
                    summary.append(f"Records: {len(df_data)}")
                    if len(df_data) > 0:
                        summary.append(f"Columns: {', '.join(df_data.columns.tolist())}")
                        summary.append(f"Sample records (first 3):")
                        summary.append(df_data.head(3).to_string())
                elif isinstance(df_data, list) and len(df_data) > 0:
                    summary.append(f"Records: {len(df_data)}")
                    summary.append(f"Sample: {json.dumps(df_data[0], indent=2)}")
        
        result = "\n".join(summary)
        # Limit summary length to avoid token limits
        if len(result) > 3000:
            result = result[:3000] + "\n... (truncated)"
        return result
    
    def _extract_citations(self, data: Dict) -> List[Dict]:
        """Extract citation information from data sources"""
        citations = []
        for source_name, dataset_info in data.items():
            if isinstance(dataset_info, dict):
                data_content = dataset_info.get('data', [])
                record_count = len(data_content) if hasattr(data_content, '__len__') else 'N/A'
                
                citations.append({
                    "dataset": source_name,
                    "url": dataset_info.get('url', 'https://data.gov.in'),
                    "records": record_count
                })
        return citations