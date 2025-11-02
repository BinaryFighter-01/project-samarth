import requests as re
import pandas as pd
from typing import Dict, List
import os
import json
from datetime import datetime

class DataFetcher:
    def __init__(self):
        self.cache_dir = 'datasets'
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Key datasets from data.gov.in with data.gov API keys
        # These URLs are examples - you'll need to find actual dataset IDs
        self.datasets = {
            'crop_production': {
                'resource_id': 'e75f8edb-1c01-4c6e-95fd-9c98f9e4e0cd',
                'url': 'https://api.data.gov.in/resource/e75f8edb-1c01-4c6e-95fd-9c98f9e4e0cd',
                'description': 'District-wise Crop Production Statistics'
            },
            'rainfall_data': {
                'resource_id': 'rainfall-2018-2023',
                'url': 'https://data.gov.in/resource/rainfall-district-wise',
                'description': 'IMD District-wise Rainfall Data'
            },
            'agricultural_statistics': {
                'resource_id': 'agri-stats-state',
                'url': 'https://data.gov.in/resource/agricultural-statistics',
                'description': 'State-wise Agricultural Statistics'
            }
        }
    
    def fetch_data(self, query_plan: Dict) -> Dict:
        """
        Fetch data based on the query plan
        """
        fetched_data = {}
        
        # Determine which datasets to fetch
        needed_datasets = self._determine_datasets(query_plan)
        
        for dataset_key in needed_datasets:
            try:
                data = self._fetch_dataset(dataset_key, query_plan)
                if data is not None:
                    fetched_data[self.datasets[dataset_key]['description']] = {
                        'data': data,
                        'url': self.datasets[dataset_key]['url']
                    }
            except Exception as e:
                print(f"Error fetching {dataset_key}: {e}")
        
        return fetched_data
    
    def _determine_datasets(self, query_plan: Dict) -> List[str]:
        """Determine which datasets are needed based on query plan"""
        needed = []
        
        data_types = query_plan.get('data_types', [])
        
        if 'production' in data_types or 'crops' in str(query_plan.get('crops', [])):
            needed.append('crop_production')
        
        if 'rainfall' in data_types or 'climate' in str(data_types):
            needed.append('rainfall_data')
        
        # Always include general agricultural statistics
        needed.append('agricultural_statistics')
        
        return list(set(needed))
    
    def _fetch_dataset(self, dataset_key: str, query_plan: Dict) -> pd.DataFrame:
        """
        Fetch a specific dataset from data.gov.in or cache
        """
        cache_file = os.path.join(self.cache_dir, f'{dataset_key}.csv')
        
        # Check cache first
        if os.path.exists(cache_file):
            df = pd.read_csv(cache_file)
            return self._filter_data(df, query_plan)
        
        # Fetch from API
        dataset_info = self.datasets[dataset_key]
        
        try:
            # Method 1: Try data.gov.in API
            api_key = os.getenv('DATA_GOV_IN_API_KEY', '')
            params = {
                'api-key': api_key,
                'format': 'json',
                'limit': 10000
            }
            
            response = requests.get(dataset_info['url'], params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data.get('records', []))
                
                # Cache the data
                df.to_csv(cache_file, index=False)
                
                return self._filter_data(df, query_plan)
            else:
                print(f"API request failed: {response.status_code}")
                return self._load_sample_data(dataset_key)
                
        except Exception as e:
            print(f"Error fetching from API: {e}")
            return self._load_sample_data(dataset_key)
    
    def _filter_data(self, df: pd.DataFrame, query_plan: Dict) -> pd.DataFrame:
        """Filter dataframe based on query parameters"""
        filtered = df.copy()
        
        # Filter by states
        if query_plan.get('states') and 'state' in df.columns:
            filtered = filtered[filtered['state'].isin(query_plan['states'])]
        
        # Filter by crops
        if query_plan.get('crops') and 'crop' in df.columns:
            filtered = filtered[filtered['crop'].isin(query_plan['crops'])]
        
        # Filter by time period
        time_period = query_plan.get('time_period', {})
        if time_period and 'year' in df.columns:
            start_year = time_period.get('start_year', 0)
            end_year = time_period.get('end_year', 9999)
            filtered = filtered[(filtered['year'] >= start_year) & (filtered['year'] <= end_year)]
        
        return filtered
    
    def _load_sample_data(self, dataset_key: str) -> pd.DataFrame:
        """Load sample data when API fails"""
        # Create sample data for demonstration
        if dataset_key == 'crop_production':
            return pd.DataFrame({
                'state': ['Maharashtra', 'Punjab', 'Kerala'] * 3,
                'district': ['Pune', 'Ludhiana', 'Ernakulam'] * 3,
                'crop': ['Rice', 'Wheat', 'Coconut'] * 3,
                'year': [2021, 2022, 2023] * 3,
                'production': [1500000, 2000000, 500000] * 3,
                'area': [50000, 60000, 30000] * 3
            })
        elif dataset_key == 'rainfall_data':
            return pd.DataFrame({
                'state': ['Maharashtra', 'Punjab'] * 3,
                'year': [2021, 2022, 2023] * 2,
                'annual_rainfall': [850, 620] * 3
            })
        else:
            return pd.DataFrame()
    
    def list_available_datasets(self) -> List[Dict]:
        """List all available datasets"""
        return [
            {
                'key': key,
                'description': info['description'],
                'url': info['url']
            }
            for key, info in self.datasets.items()
        ]
