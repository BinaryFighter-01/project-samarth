import pandas as pd
import os

def create_sample_datasets():
    """Create realistic sample datasets for testing"""
    
    os.makedirs('datasets', exist_ok=True)
    
    # 1. Crop Production Data
    crop_production = pd.DataFrame({
        'state': ['Maharashtra', 'Maharashtra', 'Maharashtra', 'Punjab', 'Punjab', 'Punjab',
                  'Kerala', 'Kerala', 'Kerala', 'Uttar Pradesh', 'Uttar Pradesh', 'Uttar Pradesh'] * 3,
        'district': ['Pune', 'Nagpur', 'Mumbai', 'Ludhiana', 'Amritsar', 'Patiala',
                     'Ernakulam', 'Thrissur', 'Palakkad', 'Lucknow', 'Kanpur', 'Varanasi'] * 3,
        'crop': ['Rice', 'Cotton', 'Wheat', 'Wheat', 'Rice', 'Cotton',
                 'Coconut', 'Rice', 'Banana', 'Wheat', 'Rice', 'Sugarcane'] * 3,
        'crop_type': ['Cereals', 'Cash Crops', 'Cereals', 'Cereals', 'Cereals', 'Cash Crops',
                      'Plantation', 'Cereals', 'Fruits', 'Cereals', 'Cereals', 'Cash Crops'] * 3,
        'year': [2021] * 12 + [2022] * 12 + [2023] * 12,
        'production_tonnes': [
            # 2021
            1500000, 800000, 600000, 2500000, 900000, 500000,
            400000, 350000, 200000, 3000000, 1200000, 1500000,
            # 2022
            1550000, 820000, 610000, 2600000, 920000, 510000,
            410000, 360000, 210000, 3100000, 1250000, 1550000,
            # 2023
            1600000, 850000, 620000, 2700000, 950000, 530000,
            420000, 370000, 220000, 3200000, 1300000, 1600000
        ],
        'area_hectares': [
            # 2021
            50000, 30000, 25000, 60000, 35000, 20000,
            15000, 14000, 8000, 70000, 40000, 45000,
            # 2022
            51000, 31000, 25500, 61000, 35500, 20500,
            15200, 14200, 8100, 71000, 41000, 45500,
            # 2023
            52000, 32000, 26000, 62000, 36000, 21000,
            15400, 14400, 8200, 72000, 42000, 46000
        ],
        'yield_kg_per_hectare': [
            30000, 26667, 24000, 41667, 25714, 25000,
            26667, 25000, 25000, 42857, 30000, 33333
        ] * 3
    })
    crop_production.to_csv('datasets/crop_production.csv', index=False)
    print("✓ Created crop_production.csv")
    
    # 2. Rainfall Data
    rainfall_data = pd.DataFrame({
        'state': ['Maharashtra', 'Punjab', 'Kerala', 'Uttar Pradesh'] * 5,
        'year': [2019] * 4 + [2020] * 4 + [2021] * 4 + [2022] * 4 + [2023] * 4,
        'annual_rainfall_mm': [
            # 2019
            850, 620, 3100, 980,
            # 2020
            820, 600, 3050, 960,
            # 2021
            880, 640, 3150, 1000,
            # 2022
            900, 660, 3200, 1020,
            # 2023
            870, 630, 3180, 990
        ],
        'monsoon_rainfall_mm': [
            # 2019
            720, 500, 2800, 850,
            # 2020
            700, 480, 2750, 830,
            # 2021
            750, 520, 2850, 870,
            # 2022
            770, 540, 2900, 890,
            # 2023
            740, 510, 2880, 860
        ],
        'rainy_days': [
            # 2019
            65, 45, 150, 70,
            # 2020
            62, 42, 148, 68,
            # 2021
            68, 47, 152, 72,
            # 2022
            70, 49, 155, 74,
            # 2023
            66, 46, 153, 71
        ]
    })
    rainfall_data.to_csv('datasets/rainfall_data.csv', index=False)
    print("✓ Created rainfall_data.csv")
    
    # 3. Agricultural Statistics
    agri_stats = pd.DataFrame({
        'state': ['Maharashtra', 'Punjab', 'Kerala', 'Uttar Pradesh'] * 3,
        'year': [2021] * 4 + [2022] * 4 + [2023] * 4,
        'total_agricultural_area_hectares': [
            # 2021
            225000, 175000, 45000, 250000,
            # 2022
            226000, 176000, 45200, 251000,
            # 2023
            227000, 177000, 45400, 252000
        ],
        'irrigated_area_hectares': [
            # 2021
            180000, 160000, 35000, 220000,
            # 2022
            182000, 162000, 35500, 222000,
            # 2023
            184000, 164000, 36000, 224000
        ],
        'number_of_farmers': [
            # 2021
            138000, 152000, 98000, 178000,
            # 2022
            140000, 154000, 99000, 180000,
            # 2023
            142000, 156000, 100000, 182000
        ],
        'avg_farm_size_hectares': [
            1.63, 1.15, 0.46, 1.40
        ] * 3
    })
    agri_stats.to_csv('datasets/agricultural_statistics.csv', index=False)
    print("✓ Created agricultural_statistics.csv")
    
    print("\n✅ All sample datasets created successfully!")
    print("📁 Location: datasets/")
    print("📊 Files: crop_production.csv, rainfall_data.csv, agricultural_statistics.csv")

if __name__ == '__main__':
    create_sample_datasets()