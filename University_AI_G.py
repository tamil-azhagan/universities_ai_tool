# import streamlit as st
# import requests
# import json
# import os
# import re
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from datetime import datetime
# from typing import Dict, Any, Optional, Tuple
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# # API Key directly in script
# API_KEY = st.secrets["OPENROUTER_API_KEY"]
# OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

# # Configuration - Using GitHub raw URL
# MASTER_JSON_URL = "https://raw.githubusercontent.com/tamil-azhagan/universities_ai_tool/main/universities_master.json"
# # Local backup path (optional)
# LOCAL_JSON_PATH = "universities_master.json"

# # Page configuration
# st.set_page_config(
#     page_title="Global University Comparison",
#     page_icon="🎓",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         font-weight: 700;
#         color: #1E3A8A;
#         text-align: center;
#         margin-bottom: 1rem;
#         padding: 1rem;
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }
#     .sub-header {
#         font-size: 1.5rem;
#         font-weight: 600;
#         color: #2C3E50;
#         margin-top: 1rem;
#         margin-bottom: 1rem;
#         padding-bottom: 0.5rem;
#         border-bottom: 2px solid #3498db;
#     }
#     .info-card {
#         background-color: #f8f9fa;
#         padding: 1.5rem;
#         border-radius: 10px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         margin-bottom: 1rem;
#     }
#     .metric-card {
#         background-color: white;
#         padding: 1rem;
#         border-radius: 8px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.05);
#         border-left: 4px solid #3498db;
#     }
#     .location-badge {
#         background-color: #e3f2fd;
#         padding: 0.5rem 1rem;
#         border-radius: 20px;
#         display: inline-block;
#         margin-bottom: 1rem;
#     }
#     .stButton>button {
#         background-color: #1E3A8A;
#         color: white;
#         font-weight: 600;
#         padding: 0.75rem 2rem;
#         border-radius: 30px;
#         border: none;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.2);
#     }
#     .stButton>button:hover {
#         background-color: #2E4A9A;
#     }
#     .reset-button>button {
#         background-color: #dc3545;
#     }
#     .reset-button>button:hover {
#         background-color: #c82333;
#     }
# </style>
# """, unsafe_allow_html=True)

# class UniversityInfoSystem:
#     def __init__(self):
#         self.current_year = datetime.now().year
#         self.last_year = self.current_year - 1
#         self.master_data = self.load_master_json()
    
#     def levenshtein_distance(self, s1: str, s2: str) -> int:
#         if len(s1) < len(s2):
#             return self.levenshtein_distance(s2, s1)
#         if len(s2) == 0:
#             return len(s1)
#         previous_row = range(len(s2) + 1)
#         for i, c1 in enumerate(s1):
#             current_row = [i + 1]
#             for j, c2 in enumerate(s2):
#                 insertions = previous_row[j + 1] + 1
#                 deletions = current_row[j] + 1
#                 substitutions = previous_row[j] + (c1 != c2)
#                 current_row.append(min(insertions, deletions, substitutions))
#             previous_row = current_row
#         return previous_row[-1]
    
#     def similarity_score(self, s1: str, s2: str) -> float:
#         if not s1 and not s2:
#             return 1.0
#         if not s1 or not s2:
#             return 0.0
#         distance = self.levenshtein_distance(s1.lower(), s2.lower())
#         max_len = max(len(s1), len(s2))
#         similarity = 1 - (distance / max_len)
#         return similarity
    
#     def search_university(self, query: str) -> Tuple[Optional[Dict], float]:
#         query = query.lower().strip()
#         best_match = None
#         best_score = 0.0
#         threshold = 0.7
        
#         for uni_name, uni_data in self.master_data.items():
#             name_score = self.similarity_score(query, uni_name)
#             aliases = [
#                 uni_name.replace("University", "").strip(),
#                 uni_name.replace("Institute", "").strip(),
#                 uni_name.replace("IIT", "Indian Institute of Technology"),
#                 uni_name.replace("NIT", "National Institute of Technology"),
#             ]
#             alias_scores = [self.similarity_score(query, alias) for alias in aliases if alias]
#             max_score = max([name_score] + alias_scores)
            
#             if max_score > best_score and max_score >= threshold:
#                 best_score = max_score
#                 best_match = {uni_name: uni_data}
        
#         return best_match, best_score
    
#     def load_master_json(self) -> Dict:
#         # Try to load from GitHub first
#         try:
#             response = requests.get(MASTER_JSON_URL, timeout=10)
#             if response.status_code == 200:
#                 data = response.json()
#                 # Save a local backup
#                 with open(LOCAL_JSON_PATH, 'w', encoding='utf-8') as f:
#                     json.dump(data, f, indent=4, ensure_ascii=False)
#                 return data
#         except:
#             pass
        
#         # Fallback to local file if GitHub fails
#         if os.path.exists(LOCAL_JSON_PATH):
#             try:
#                 with open(LOCAL_JSON_PATH, 'r', encoding='utf-8') as f:
#                     return json.load(f)
#             except:
#                 return {}
#         return {}
    
#     def save_to_master_json(self, university_name: str, data: Dict):
#         clean_name = university_name.strip()
#         self.master_data[clean_name] = {
#             "data": data,
#             "last_accessed": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             "search_count": self.master_data.get(clean_name, {}).get("search_count", 0) + 1
#         }
#         # Save locally (you'll need to manually upload to GitHub)
#         with open(LOCAL_JSON_PATH, 'w', encoding='utf-8') as f:
#             json.dump(self.master_data, f, indent=4, ensure_ascii=False)
    
   
#      def fetch_university_details(self, university_name: str) -> Dict[str, Any]:
#         prompt = f"""You are a university research assistant with REAL-TIME INTERNET ACCESS. 
#     Search for latest information about "{university_name}".
    
#     CURRENT YEAR: 2026
    
#     Return ONLY valid JSON in this exact structure (include 7-8 items per list where applicable):
    
#     {{
#         "university_name": "{university_name}",
#         "location": {{
#             "city": "City name",
#             "state": "State name", 
#             "country": "Country"
#         }},
#         "country": "India/Other",
#         "last_updated": "{datetime.now().strftime('%Y-%m-%d')}",
#         "academic_info": {{
#             "nirf_rank": "Rank or Not Applicable",
#             "nirf_rank_numeric": 0,
#             "courses": {{
#                 "ug": ["8 main UG courses"],
#                 "pg": ["8 main PG courses"],
#                 "phd": ["8 main PhD areas"]
#             }},
#             "entrance_exams": ["8 main entrance exams"],
#             "official_website": "URL",
#             "fees_link": "URL",
#             "placements": {{
#                 "year": "2025",
#                 "highest_package": "Amount",
#                 "average_package": "Amount",
#                 "top_recruiters": ["8 top companies"],
#                 "companies_visited": 0
#             }}
#         }},
#         "research_info": {{
#             "publications": {{
#                 "last_year_2025": 0,
#                 "total": 0
#             }},
#             "patents": {{
#                 "filed_total": 0,
#                 "granted_total": 0
#             }},
#             "funded_projects": {{
#                 "count": 0,
#                 "total_value_crores": 0
#             }},
#             "centralized_facilities": ["7 main facilities"]
#         }},
#         "sports_cultural": {{
#             "cultural_events": [
#                 {{"event_name": "Event", "dates": "Dates"}}
#             ],
#             "sports_events": [
#                 {{"event_name": "Event", "dates": "Dates"}}
#             ],
#             "extra_curricular": ["8 main activities"]
#         }},
#         "upcoming_events": {{
#             "international_conferences": [
#                 {{"name": "Conference", "dates": "Dates"}}
#             ],
#             "national_conferences": [
#                 {{"name": "Conference", "dates": "Dates"}}
#             ],
#             "faculty_development_programs": [
#                 {{"name": "FDP", "dates": "Dates"}}
#             ],
#             "training_events": [
#                 {{"name": "Training", "dates": "Dates"}}
#             ]
#         }}
#     }}"""
        
#         # Rest of your method remains the same... 
#             payload = {
#                 "model": "qwen/qwen3-vl-30b-a3b-thinking",
#                 "messages": [{"role": "user", "content": prompt}],
#                 "temperature": 0.1,
#                 "max_tokens": 3000
#             }
            
#             try:
#                 st.write("Debug - Sending request to OpenRouter...")
#                 response = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload, timeout=60)
                
#                 st.write(f"Debug - Status Code: {response.status_code}")
#                 st.write(f"Debug - Response Headers: {dict(response.headers)}")
                
#                 if response.status_code == 200:
#                     result = response.json()
#                     content = result["choices"][0]["message"]["content"]
#                     st.write("Debug - Raw Response received, length:", len(content))
                    
#                     json_start = content.find('{')
#                     json_end = content.rfind('}') + 1
#                     if json_start != -1 and json_end != 0:
#                         try:
#                             data = json.loads(content[json_start:json_end])
#                             st.write("Debug - Successfully parsed JSON")
#                             return data
#                         except json.JSONDecodeError as e:
#                             st.write(f"Debug - JSON Parse Error: {e}")
#                             st.write("Debug - Content that failed:", content[:500])
#                     else:
#                         st.write("Debug - No JSON found in response")
#                         st.write("Debug - Response content:", content[:500])
#                 else:
#                     st.write(f"Debug - Error Response: {response.text}")
                    
#                 return self.create_error_response(university_name)
#             except Exception as e:
#                 st.write(f"Debug - Exception: {str(e)}")
#                 import traceback
#                 st.write(f"Debug - Traceback: {traceback.format_exc()}")
#                 return self.create_error_response(university_name)
        
#         def create_error_response(self, university_name: str) -> Dict[str, Any]:
#             return {
#                 "university_name": university_name,
#                 "location": {"city": "Unknown", "state": "Unknown", "country": "Unknown"},
#                 "country": "Unknown",
#                 "last_updated": datetime.now().strftime('%Y-%m-%d'),
#                 "academic_info": {
#                     "nirf_rank": "Not available",
#                     "nirf_rank_numeric": 0,
#                     "courses": {"ug": [], "pg": [], "phd": []},
#                     "entrance_exams": [],
#                     "official_website": "#",
#                     "fees_link": "#",
#                     "placements": {"year": "N/A", "highest_package": "N/A", "average_package": "N/A", "top_recruiters": [], "companies_visited": 0}
#                 },
#                 "research_info": {
#                     "publications": {"last_year_2025": 0, "total": 0},
#                     "patents": {"filed_total": 0, "granted_total": 0},
#                     "funded_projects": {"count": 0, "total_value_crores": 0},
#                     "centralized_facilities": []
        
        
#     def create_comparison_charts(self, uni_name: str, uni_data: Dict):
#         # Get SASTRA data from master JSON
#         sastra_data = self.master_data.get("SASTRA University", {}).get("data", {})
        
#         if not sastra_data:
#             return None
        
#         # Extract values
#         req_nirf = uni_data.get('academic_info', {}).get('nirf_rank_numeric', 0)
#         sastra_nirf = sastra_data.get('academic_info', {}).get('nirf_rank_numeric', 51)
        
#         req_pubs = uni_data.get('research_info', {}).get('publications', {}).get('total', 0)
#         sastra_pubs = sastra_data.get('research_info', {}).get('publications', {}).get('total', 9558)
        
#         req_patents_filed = uni_data.get('research_info', {}).get('patents', {}).get('filed_total', 0)
#         req_patents_granted = uni_data.get('research_info', {}).get('patents', {}).get('granted_total', 0)
#         sastra_patents_filed = sastra_data.get('research_info', {}).get('patents', {}).get('filed_total', 52)
#         sastra_patents_granted = sastra_data.get('research_info', {}).get('patents', {}).get('granted_total', 7)
        
#         req_funding = uni_data.get('research_info', {}).get('funded_projects', {}).get('total_value_crores', 0)
#         sastra_funding = sastra_data.get('research_info', {}).get('funded_projects', {}).get('total_value_crores', 92.84)
        
#         # Create subplots
#         fig = make_subplots(
#             rows=2, cols=2,
#             subplot_titles=('NIRF Rank Comparison', 'Research Publications', 
#                           'Patents Comparison', 'Funded Projects (₹ Crores)'),
#             specs=[[{'type': 'bar'}, {'type': 'bar'}],
#                    [{'type': 'bar'}, {'type': 'bar'}]]
#         )
        
#         # NIRF Rank
#         fig.add_trace(
#             go.Bar(x=[uni_name[:15], 'SASTRA'], y=[req_nirf, sastra_nirf],
#                    marker_color=['#3498db', '#e74c3c'],
#                    text=[req_nirf, sastra_nirf], textposition='outside'),
#             row=1, col=1
#         )
        
#         # Publications
#         fig.add_trace(
#             go.Bar(x=[uni_name[:15], 'SASTRA'], y=[req_pubs, sastra_pubs],
#                    marker_color=['#3498db', '#e74c3c'],
#                    text=[f'{req_pubs:,}', f'{sastra_pubs:,}'], textposition='outside'),
#             row=1, col=2
#         )
        
#         # Patents
#         fig.add_trace(
#             go.Bar(x=[uni_name[:15], 'SASTRA'], y=[req_patents_filed, sastra_patents_filed],
#                    name='Filed', marker_color='#f39c12'),
#             row=2, col=1
#         )
#         fig.add_trace(
#             go.Bar(x=[uni_name[:15], 'SASTRA'], y=[req_patents_granted, sastra_patents_granted],
#                    name='Granted', marker_color='#27ae60'),
#             row=2, col=1
#         )
        
#         # Funding
#         fig.add_trace(
#             go.Bar(x=[uni_name[:15], 'SASTRA'], y=[req_funding, sastra_funding],
#                    marker_color=['#3498db', '#e74c3c'],
#                    text=[f'₹{req_funding}Cr', f'₹{sastra_funding}Cr'], textposition='outside'),
#             row=2, col=2
#         )
        
#         fig.update_layout(height=700, showlegend=True, title_text="Comparison with SASTRA University")
#         fig.update_xaxes(tickangle=45)
        
#         return fig

# # Initialize system
# @st.cache_resource
# def init_system():
#     return UniversityInfoSystem()

# def main():
#     # Initialize session state for reset functionality
#     if 'show_results' not in st.session_state:
#         st.session_state.show_results = False
#     if 'uni_name' not in st.session_state:
#         st.session_state.uni_name = None
#     if 'uni_data' not in st.session_state:
#         st.session_state.uni_data = None
    
#     # Header
#     st.markdown('<h1 class="main-header">🎓 Global University Comparison</h1>', unsafe_allow_html=True)
    
#     # Initialize system
#     uni_system = init_system()
    
#     # Search section with Reset button
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         university_name = st.text_input("Enter University Name", placeholder="e.g., IIT Madras, Stanford, Oxford", key="uni_input")
        
#         # Buttons side by side
#         btn_col1, btn_col2 = st.columns(2)
#         with btn_col1:
#             search_button = st.button("🔍 Search & Compare", use_container_width=True)
#         with btn_col2:
#             reset_button = st.button("🔄 Reset", use_container_width=True)
    
#     # Handle reset
#     if reset_button:
#         st.session_state.show_results = False
#         st.session_state.uni_name = None
#         st.session_state.uni_data = None
#         st.rerun()
    
#     # # Handle search
#     # if search_button and university_name:
#     #     with st.spinner('Searching university information...'):
#     #         # Search in cache
#     #         best_match, similarity = uni_system.search_university(university_name)
            
#     #         if best_match:
#     #             uni_name = list(best_match.keys())[0]
#     #             uni_data = best_match[uni_name]["data"]
#     #             # st.success(f"✅ Found in cache (Similarity: {similarity:.2%})")
#     #         else:
#     #             # Fetch from internet
#     #             uni_data = uni_system.fetch_university_details(university_name)
#     #             uni_name = university_name
#     #             if "error" not in uni_data:
#     #                 uni_system.save_to_master_json(uni_name, uni_data)
#     #                 st.success("✅ University details at your fingertips")
#     #             else:
#     #                 st.error("❌ Could not fetch university information")
#     #                 return
            
#     #         # Store in session state
#     #         st.session_state.show_results = True
#     #         st.session_state.uni_name = uni_name
#     #         st.session_state.uni_data = uni_data
#     #         st.rerun()

#     if search_button and university_name:
#         with st.spinner('Searching university information...'):
#             # Search in cache
#             best_match, similarity = uni_system.search_university(university_name)
            
#             if best_match:
#                 uni_name = list(best_match.keys())[0]
#                 uni_data = best_match[uni_name]["data"]
#                 st.write("✅ Found in cache")
#                 st.write("Debug - Data keys:", uni_data.keys())  # DEBUG
#             else:
#                 # Fetch from internet
#                 st.write("Debug - Fetching from API...")  # DEBUG
#                 uni_data = uni_system.fetch_university_details(university_name)
#                 uni_name = university_name
                
#                 st.write("Debug - API Response received")  # DEBUG
#                 st.write("Debug - Data keys:", uni_data.keys())  # DEBUG
                
#                 if "error" not in uni_data:
#                     uni_system.save_to_master_json(uni_name, uni_data)
#                     st.success("✅ University details at your fingertips")
#                 else:
#                     st.error("❌ Could not fetch university information")
#                     st.write("Debug - Error data:", uni_data)  # DEBUG
#                     return
            
#             # Store in session state
#             st.session_state.show_results = True
#             st.session_state.uni_name = uni_name
#             st.session_state.uni_data = uni_data
#             st.rerun()
        
#     # Display results if available
#     if st.session_state.show_results and st.session_state.uni_data:
#         uni_name = st.session_state.uni_name
#         uni_data = st.session_state.uni_data

#         # DEBUG - show what we have
#         st.write("Debug - Displaying results for:", uni_name)
#         st.write("Debug - Full data:", uni_data)
#         st.write("---")
#         # Location Badge
#         location = uni_data.get('location', {})
#         st.markdown(f"""
#         <div class="location-badge">
#             📍 {location.get('city', 'Unknown')}, {location.get('state', 'Unknown')}, {location.get('country', 'Unknown')}
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Create tabs for different sections
#         tab1, tab2, tab3, tab4, tab5 = st.tabs(["📚 Academic", "🔬 Research", "🎪 Sports & Cultural", "📅 Events", "📊 Comparison Graphs"])
        
#         # Tab 1: Academic
#         with tab1:
#             st.markdown('<h2 class="sub-header">Academic Information</h2>', unsafe_allow_html=True)
            
#             acad = uni_data.get('academic_info', {})
            
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#                 st.metric("NIRF Rank", acad.get('nirf_rank', 'N/A'))
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col2:
#                 st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#                 st.metric("Placement Year", acad.get('placements', {}).get('year', 'N/A'))
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col3:
#                 st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#                 st.metric("Companies Visited", acad.get('placements', {}).get('companies_visited', 'N/A'))
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 st.markdown("**🎓 UG Courses**")
#                 for course in acad.get('courses', {}).get('ug', [])[:8]:
#                     st.markdown(f"- {course}")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col2:
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 st.markdown("**📖 PG Courses**")
#                 for course in acad.get('courses', {}).get('pg', [])[:8]:
#                     st.markdown(f"- {course}")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 st.markdown("**🔬 PhD Specializations**")
#                 for spec in acad.get('courses', {}).get('phd', [])[:8]:
#                     st.markdown(f"- {spec}")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col2:
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 st.markdown("**📝 Entrance Exams**")
#                 for exam in acad.get('entrance_exams', [])[:8]:
#                     st.markdown(f"- {exam}")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             st.markdown('<div class="info-card">', unsafe_allow_html=True)
#             st.markdown("**💼 Placement Details**")
#             placements = acad.get('placements', {})
#             st.markdown(f"- **Highest Package:** {placements.get('highest_package', 'N/A')}")
#             st.markdown(f"- **Average Package:** {placements.get('average_package', 'N/A')}")
#             st.markdown("**Top Recruiters:**")
#             for recruiter in placements.get('top_recruiters', [])[:8]:
#                 st.markdown(f"  - {recruiter}")
#             st.markdown('</div>', unsafe_allow_html=True)
            
#             st.markdown(f"**🌐 Website:** [{acad.get('official_website', 'N/A')}]({acad.get('official_website', '#')})")
#             st.markdown(f"**💰 Fees Link:** [{acad.get('fees_link', 'N/A')}]({acad.get('fees_link', '#')})")
        
#         # Tab 2: Research
#         with tab2:
#             st.markdown('<h2 class="sub-header">Research Information</h2>', unsafe_allow_html=True)
            
#             research = uni_data.get('research_info', {})
            
#             col1, col2, col3, col4 = st.columns(4)
#             with col1:
#                 st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#                 st.metric("Publications (2025)", research.get('publications', {}).get('last_year_2025', 0))
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col2:
#                 st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#                 st.metric("Total Publications", f"{research.get('publications', {}).get('total', 0):,}")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col3:
#                 st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#                 patents = research.get('patents', {})
#                 st.metric("Patents Filed", patents.get('filed_total', 0))
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col4:
#                 st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#                 patents = research.get('patents', {})
#                 st.metric("Patents Granted", patents.get('granted_total', 0))
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 funded = research.get('funded_projects', {})
#                 st.markdown("**💰 Funded Projects**")
#                 st.markdown(f"- **Number of Projects:** {funded.get('count', 0)}")
#                 st.markdown(f"- **Total Value:** ₹{funded.get('total_value_crores', 0)} Crores")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col2:
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 st.markdown("**🏗️ Centralized Facilities**")
#                 for facility in research.get('centralized_facilities', [])[:7]:
#                     st.markdown(f"- {facility}")
#                 st.markdown('</div>', unsafe_allow_html=True)
        
#         # Tab 3: Sports & Cultural
#         with tab3:
#             st.markdown('<h2 class="sub-header">Sports & Cultural Activities</h2>', unsafe_allow_html=True)
            
#             sports = uni_data.get('sports_cultural', {})
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 st.markdown("**🎭 Cultural Events**")
#                 for event in sports.get('cultural_events', []):
#                     if isinstance(event, dict):
#                         st.markdown(f"- **{event.get('event_name', 'Unknown')}**")
#                         if event.get('dates'):
#                             st.markdown(f"  📅 {event['dates']}")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col2:
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 st.markdown("**⚽ Sports Events**")
#                 for event in sports.get('sports_events', []):
#                     if isinstance(event, dict):
#                         st.markdown(f"- **{event.get('event_name', 'Unknown')}**")
#                         if event.get('dates'):
#                             st.markdown(f"  📅 {event['dates']}")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             st.markdown('<div class="info-card">', unsafe_allow_html=True)
#             st.markdown("**🎯 Extra Curricular Activities**")
#             for activity in sports.get('extra_curricular', [])[:8]:
#                 st.markdown(f"- {activity}")
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         # Tab 4: Events
#         with tab4:
#             st.markdown('<h2 class="sub-header">Upcoming Events</h2>', unsafe_allow_html=True)
            
#             events = uni_data.get('upcoming_events', {})
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 st.markdown("**🌎 International Conferences**")
#                 for conf in events.get('international_conferences', []):
#                     if isinstance(conf, dict):
#                         st.markdown(f"- **{conf.get('name', 'Unknown')}**")
#                         if conf.get('dates'):
#                             st.markdown(f"  📅 {conf['dates']}")
#                 st.markdown('</div>', unsafe_allow_html=True)
                
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 st.markdown("**🇮🇳 National Conferences**")
#                 for conf in events.get('national_conferences', []):
#                     if isinstance(conf, dict):
#                         st.markdown(f"- **{conf.get('name', 'Unknown')}**")
#                         if conf.get('dates'):
#                             st.markdown(f"  📅 {conf['dates']}")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col2:
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 st.markdown("**👨‍🏫 Faculty Development Programs**")
#                 for fdp in events.get('faculty_development_programs', []):
#                     if isinstance(fdp, dict):
#                         st.markdown(f"- **{fdp.get('name', 'Unknown')}**")
#                         if fdp.get('dates'):
#                             st.markdown(f"  📅 {fdp['dates']}")
#                 st.markdown('</div>', unsafe_allow_html=True)
                
#                 st.markdown('<div class="info-card">', unsafe_allow_html=True)
#                 st.markdown("**🎓 Training Events**")
#                 for training in events.get('training_events', []):
#                     if isinstance(training, dict):
#                         st.markdown(f"- **{training.get('name', 'Unknown')}**")
#                         if training.get('dates'):
#                             st.markdown(f"  📅 {training['dates']}")
#                 st.markdown('</div>', unsafe_allow_html=True)
        
#         # Tab 5: Comparison Graphs
#         with tab5:
#             st.markdown('<h2 class="sub-header">Comparison with SASTRA University</h2>', unsafe_allow_html=True)
            
#             fig = uni_system.create_comparison_charts(uni_name, uni_data)
#             if fig:
#                 st.plotly_chart(fig, use_container_width=True)
#             else:
#                 st.info("SASTRA University data not found in cache")

# if __name__ == "__main__":

#     main()


import streamlit as st
import requests
import json
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# API Key directly in script
API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Configuration - Using GitHub raw URL
MASTER_JSON_URL = "https://raw.githubusercontent.com/tamil-azhagan/universities_ai_tool/main/universities_master.json"
# Local backup path (optional)
LOCAL_JSON_PATH = "universities_master.json"

# Page configuration
st.set_page_config(
    page_title="Global University Comparison",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2C3E50;
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3498db;
    }
    .info-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid #3498db;
    }
    .location-badge {
        background-color: #e3f2fd;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 30px;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #2E4A9A;
    }
    .reset-button>button {
        background-color: #dc3545;
    }
    .reset-button>button:hover {
        background-color: #c82333;
    }
</style>
""", unsafe_allow_html=True)

class UniversityInfoSystem:
    def __init__(self):
        self.current_year = datetime.now().year
        self.last_year = self.current_year - 1
        self.master_data = self.load_master_json()
    
    def levenshtein_distance(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]
    
    def similarity_score(self, s1: str, s2: str) -> float:
        if not s1 and not s2:
            return 1.0
        if not s1 or not s2:
            return 0.0
        distance = self.levenshtein_distance(s1.lower(), s2.lower())
        max_len = max(len(s1), len(s2))
        similarity = 1 - (distance / max_len)
        return similarity
    
    def search_university(self, query: str) -> Tuple[Optional[Dict], float]:
        query = query.lower().strip()
        best_match = None
        best_score = 0.0
        threshold = 0.7
        
        for uni_name, uni_data in self.master_data.items():
            name_score = self.similarity_score(query, uni_name)
            aliases = [
                uni_name.replace("University", "").strip(),
                uni_name.replace("Institute", "").strip(),
                uni_name.replace("IIT", "Indian Institute of Technology"),
                uni_name.replace("NIT", "National Institute of Technology"),
            ]
            alias_scores = [self.similarity_score(query, alias) for alias in aliases if alias]
            max_score = max([name_score] + alias_scores)
            
            if max_score > best_score and max_score >= threshold:
                best_score = max_score
                best_match = {uni_name: uni_data}
        
        return best_match, best_score
    
    def load_master_json(self) -> Dict:
        # Try to load from GitHub first
        try:
            response = requests.get(MASTER_JSON_URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Save a local backup
                with open(LOCAL_JSON_PATH, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                return data
        except:
            pass
        
        # Fallback to local file if GitHub fails
        if os.path.exists(LOCAL_JSON_PATH):
            try:
                with open(LOCAL_JSON_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_to_master_json(self, university_name: str, data: Dict):
        clean_name = university_name.strip()
        self.master_data[clean_name] = {
            "data": data,
            "last_accessed": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "search_count": self.master_data.get(clean_name, {}).get("search_count", 0) + 1
        }
        # Save locally (you'll need to manually upload to GitHub)
        with open(LOCAL_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.master_data, f, indent=4, ensure_ascii=False)
    
    def fetch_university_details(self, university_name: str) -> Dict[str, Any]:
        prompt = f"""You are a university research assistant with REAL-TIME INTERNET ACCESS. 
Search for latest information about "{university_name}".

CURRENT YEAR: 2026

Return ONLY valid JSON in this exact structure (include 7-8 items per list where applicable):

{{
    "university_name": "{university_name}",
    "location": {{
        "city": "City name",
        "state": "State name", 
        "country": "Country"
    }},
    "country": "India/Other",
    "last_updated": "{datetime.now().strftime('%Y-%m-%d')}",
    "academic_info": {{
        "nirf_rank": "Rank or Not Applicable",
        "nirf_rank_numeric": 0,
        "courses": {{
            "ug": ["8 main UG courses"],
            "pg": ["8 main PG courses"],
            "phd": ["8 main PhD areas"]
        }},
        "entrance_exams": ["8 main entrance exams"],
        "official_website": "URL",
        "fees_link": "URL",
        "placements": {{
            "year": "2025",
            "highest_package": "Amount",
            "average_package": "Amount",
            "top_recruiters": ["8 top companies"],
            "companies_visited": 0
        }}
    }},
    "research_info": {{
        "publications": {{
            "last_year_2025": 0,
            "total": 0
        }},
        "patents": {{
            "filed_total": 0,
            "granted_total": 0
        }},
        "funded_projects": {{
            "count": 0,
            "total_value_crores": 0
        }},
        "centralized_facilities": ["7 main facilities"]
    }},
    "sports_cultural": {{
        "cultural_events": [
            {{"event_name": "Event", "dates": "Dates"}}
        ],
        "sports_events": [
            {{"event_name": "Event", "dates": "Dates"}}
        ],
        "extra_curricular": ["8 main activities"]
    }},
    "upcoming_events": {{
        "international_conferences": [
            {{"name": "Conference", "dates": "Dates"}}
        ],
        "national_conferences": [
            {{"name": "Conference", "dates": "Dates"}}
        ],
        "faculty_development_programs": [
            {{"name": "FDP", "dates": "Dates"}}
        ],
        "training_events": [
            {{"name": "Training", "dates": "Dates"}}
        ]
    }}
}}"""
        
        payload = {
            "model": "qwen/qwen3-vl-30b-a3b-thinking",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 3000
        }
        
        try:
            st.write("Debug - Sending request to OpenRouter...")
            response = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload, timeout=60)
            
            st.write(f"Debug - Status Code: {response.status_code}")
            st.write(f"Debug - Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                st.write("Debug - Raw Response received, length:", len(content))
                
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    try:
                        data = json.loads(content[json_start:json_end])
                        st.write("Debug - Successfully parsed JSON")
                        return data
                    except json.JSONDecodeError as e:
                        st.write(f"Debug - JSON Parse Error: {e}")
                        st.write("Debug - Content that failed:", content[:500])
                else:
                    st.write("Debug - No JSON found in response")
                    st.write("Debug - Response content:", content[:500])
            else:
                st.write(f"Debug - Error Response: {response.text}")
                
            return self.create_error_response(university_name)
        except Exception as e:
            st.write(f"Debug - Exception: {str(e)}")
            import traceback
            st.write(f"Debug - Traceback: {traceback.format_exc()}")
            return self.create_error_response(university_name)
    
    def create_error_response(self, university_name: str) -> Dict[str, Any]:
        return {
            "university_name": university_name,
            "location": {"city": "Unknown", "state": "Unknown", "country": "Unknown"},
            "country": "Unknown",
            "last_updated": datetime.now().strftime('%Y-%m-%d'),
            "academic_info": {
                "nirf_rank": "Not available",
                "nirf_rank_numeric": 0,
                "courses": {"ug": [], "pg": [], "phd": []},
                "entrance_exams": [],
                "official_website": "#",
                "fees_link": "#",
                "placements": {"year": "N/A", "highest_package": "N/A", "average_package": "N/A", "top_recruiters": [], "companies_visited": 0}
            },
            "research_info": {
                "publications": {"last_year_2025": 0, "total": 0},
                "patents": {"filed_total": 0, "granted_total": 0},
                "funded_projects": {"count": 0, "total_value_crores": 0},
                "centralized_facilities": []
            },
            "sports_cultural": {"cultural_events": [], "sports_events": [], "extra_curricular": []},
            "upcoming_events": {
                "international_conferences": [],
                "national_conferences": [],
                "faculty_development_programs": [],
                "training_events": []
            }
        }
    
    def create_comparison_charts(self, uni_name: str, uni_data: Dict):
        # Get SASTRA data from master JSON
        sastra_data = self.master_data.get("SASTRA University", {}).get("data", {})
        
        if not sastra_data:
            return None
        
        # Extract values
        req_nirf = uni_data.get('academic_info', {}).get('nirf_rank_numeric', 0)
        sastra_nirf = sastra_data.get('academic_info', {}).get('nirf_rank_numeric', 51)
        
        req_pubs = uni_data.get('research_info', {}).get('publications', {}).get('total', 0)
        sastra_pubs = sastra_data.get('research_info', {}).get('publications', {}).get('total', 9558)
        
        req_patents_filed = uni_data.get('research_info', {}).get('patents', {}).get('filed_total', 0)
        req_patents_granted = uni_data.get('research_info', {}).get('patents', {}).get('granted_total', 0)
        sastra_patents_filed = sastra_data.get('research_info', {}).get('patents', {}).get('filed_total', 52)
        sastra_patents_granted = sastra_data.get('research_info', {}).get('patents', {}).get('granted_total', 7)
        
        req_funding = uni_data.get('research_info', {}).get('funded_projects', {}).get('total_value_crores', 0)
        sastra_funding = sastra_data.get('research_info', {}).get('funded_projects', {}).get('total_value_crores', 92.84)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('NIRF Rank Comparison', 'Research Publications', 
                          'Patents Comparison', 'Funded Projects (₹ Crores)'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # NIRF Rank
        fig.add_trace(
            go.Bar(x=[uni_name[:15], 'SASTRA'], y=[req_nirf, sastra_nirf],
                   marker_color=['#3498db', '#e74c3c'],
                   text=[req_nirf, sastra_nirf], textposition='outside'),
            row=1, col=1
        )
        
        # Publications
        fig.add_trace(
            go.Bar(x=[uni_name[:15], 'SASTRA'], y=[req_pubs, sastra_pubs],
                   marker_color=['#3498db', '#e74c3c'],
                   text=[f'{req_pubs:,}', f'{sastra_pubs:,}'], textposition='outside'),
            row=1, col=2
        )
        
        # Patents
        fig.add_trace(
            go.Bar(x=[uni_name[:15], 'SASTRA'], y=[req_patents_filed, sastra_patents_filed],
                   name='Filed', marker_color='#f39c12'),
            row=2, col=1
        )
        fig.add_trace(
            go.Bar(x=[uni_name[:15], 'SASTRA'], y=[req_patents_granted, sastra_patents_granted],
                   name='Granted', marker_color='#27ae60'),
            row=2, col=1
        )
        
        # Funding
        fig.add_trace(
            go.Bar(x=[uni_name[:15], 'SASTRA'], y=[req_funding, sastra_funding],
                   marker_color=['#3498db', '#e74c3c'],
                   text=[f'₹{req_funding}Cr', f'₹{sastra_funding}Cr'], textposition='outside'),
            row=2, col=2
        )
        
        fig.update_layout(height=700, showlegend=True, title_text="Comparison with SASTRA University")
        fig.update_xaxes(tickangle=45)
        
        return fig

# Initialize system
@st.cache_resource
def init_system():
    return UniversityInfoSystem()

def main():
    # Initialize session state for reset functionality
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'uni_name' not in st.session_state:
        st.session_state.uni_name = None
    if 'uni_data' not in st.session_state:
        st.session_state.uni_data = None
    
    # Header
    st.markdown('<h1 class="main-header">🎓 Global University Comparison</h1>', unsafe_allow_html=True)
    
    # Initialize system
    uni_system = init_system()
    
    # Search section with Reset button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        university_name = st.text_input("Enter University Name", placeholder="e.g., IIT Madras, Stanford, Oxford", key="uni_input")
        
        # Buttons side by side
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            search_button = st.button("🔍 Search & Compare", use_container_width=True)
        with btn_col2:
            reset_button = st.button("🔄 Reset", use_container_width=True)
    
    # Handle reset
    if reset_button:
        st.session_state.show_results = False
        st.session_state.uni_name = None
        st.session_state.uni_data = None
        st.rerun()
    
    # Handle search
    if search_button and university_name:
        with st.spinner('Searching university information...'):
            # Search in cache
            best_match, similarity = uni_system.search_university(university_name)
            
            if best_match:
                uni_name = list(best_match.keys())[0]
                uni_data = best_match[uni_name]["data"]
                st.write("✅ Found in cache")
                st.write("Debug - Data keys:", uni_data.keys())
            else:
                # Fetch from internet
                st.write("Debug - Fetching from API...")
                uni_data = uni_system.fetch_university_details(university_name)
                uni_name = university_name
                
                st.write("Debug - API Response received")
                st.write("Debug - Data keys:", uni_data.keys())
                
                if "error" not in uni_data:
                    uni_system.save_to_master_json(uni_name, uni_data)
                    st.success("✅ University details at your fingertips")
                else:
                    st.error("❌ Could not fetch university information")
                    st.write("Debug - Error data:", uni_data)
                    return
            
            # Store in session state
            st.session_state.show_results = True
            st.session_state.uni_name = uni_name
            st.session_state.uni_data = uni_data
            st.rerun()
        
    # Display results if available
    if st.session_state.show_results and st.session_state.uni_data:
        uni_name = st.session_state.uni_name
        uni_data = st.session_state.uni_data

        # DEBUG - show what we have
        st.write("Debug - Displaying results for:", uni_name)
        st.write("Debug - Full data:", uni_data)
        st.write("---")
        
        # Location Badge
        location = uni_data.get('location', {})
        st.markdown(f"""
        <div class="location-badge">
            📍 {location.get('city', 'Unknown')}, {location.get('state', 'Unknown')}, {location.get('country', 'Unknown')}
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📚 Academic", "🔬 Research", "🎪 Sports & Cultural", "📅 Events", "📊 Comparison Graphs"])
        
        # Tab 1: Academic
        with tab1:
            st.markdown('<h2 class="sub-header">Academic Information</h2>', unsafe_allow_html=True)
            
            acad = uni_data.get('academic_info', {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("NIRF Rank", acad.get('nirf_rank', 'N/A'))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Placement Year", acad.get('placements', {}).get('year', 'N/A'))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Companies Visited", acad.get('placements', {}).get('companies_visited', 'N/A'))
                st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("**🎓 UG Courses**")
                for course in acad.get('courses', {}).get('ug', [])[:8]:
                    st.markdown(f"- {course}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("**📖 PG Courses**")
                for course in acad.get('courses', {}).get('pg', [])[:8]:
                    st.markdown(f"- {course}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("**🔬 PhD Specializations**")
                for spec in acad.get('courses', {}).get('phd', [])[:8]:
                    st.markdown(f"- {spec}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("**📝 Entrance Exams**")
                for exam in acad.get('entrance_exams', [])[:8]:
                    st.markdown(f"- {exam}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("**💼 Placement Details**")
            placements = acad.get('placements', {})
            st.markdown(f"- **Highest Package:** {placements.get('highest_package', 'N/A')}")
            st.markdown(f"- **Average Package:** {placements.get('average_package', 'N/A')}")
            st.markdown("**Top Recruiters:**")
            for recruiter in placements.get('top_recruiters', [])[:8]:
                st.markdown(f"  - {recruiter}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown(f"**🌐 Website:** [{acad.get('official_website', 'N/A')}]({acad.get('official_website', '#')})")
            st.markdown(f"**💰 Fees Link:** [{acad.get('fees_link', 'N/A')}]({acad.get('fees_link', '#')})")
        
        # Tab 2: Research
        with tab2:
            st.markdown('<h2 class="sub-header">Research Information</h2>', unsafe_allow_html=True)
            
            research = uni_data.get('research_info', {})
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Publications (2025)", research.get('publications', {}).get('last_year_2025', 0))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Total Publications", f"{research.get('publications', {}).get('total', 0):,}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                patents = research.get('patents', {})
                st.metric("Patents Filed", patents.get('filed_total', 0))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                patents = research.get('patents', {})
                st.metric("Patents Granted", patents.get('granted_total', 0))
                st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                funded = research.get('funded_projects', {})
                st.markdown("**💰 Funded Projects**")
                st.markdown(f"- **Number of Projects:** {funded.get('count', 0)}")
                st.markdown(f"- **Total Value:** ₹{funded.get('total_value_crores', 0)} Crores")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("**🏗️ Centralized Facilities**")
                for facility in research.get('centralized_facilities', [])[:7]:
                    st.markdown(f"- {facility}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Tab 3: Sports & Cultural
        with tab3:
            st.markdown('<h2 class="sub-header">Sports & Cultural Activities</h2>', unsafe_allow_html=True)
            
            sports = uni_data.get('sports_cultural', {})
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("**🎭 Cultural Events**")
                for event in sports.get('cultural_events', []):
                    if isinstance(event, dict):
                        st.markdown(f"- **{event.get('event_name', 'Unknown')}**")
                        if event.get('dates'):
                            st.markdown(f"  📅 {event['dates']}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("**⚽ Sports Events**")
                for event in sports.get('sports_events', []):
                    if isinstance(event, dict):
                        st.markdown(f"- **{event.get('event_name', 'Unknown')}**")
                        if event.get('dates'):
                            st.markdown(f"  📅 {event['dates']}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("**🎯 Extra Curricular Activities**")
            for activity in sports.get('extra_curricular', [])[:8]:
                st.markdown(f"- {activity}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tab 4: Events
        with tab4:
            st.markdown('<h2 class="sub-header">Upcoming Events</h2>', unsafe_allow_html=True)
            
            events = uni_data.get('upcoming_events', {})
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("**🌎 International Conferences**")
                for conf in events.get('international_conferences', []):
                    if isinstance(conf, dict):
                        st.markdown(f"- **{conf.get('name', 'Unknown')}**")
                        if conf.get('dates'):
                            st.markdown(f"  📅 {conf['dates']}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("**🇮🇳 National Conferences**")
                for conf in events.get('national_conferences', []):
                    if isinstance(conf, dict):
                        st.markdown(f"- **{conf.get('name', 'Unknown')}**")
                        if conf.get('dates'):
                            st.markdown(f"  📅 {conf['dates']}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("**👨‍🏫 Faculty Development Programs**")
                for fdp in events.get('faculty_development_programs', []):
                    if isinstance(fdp, dict):
                        st.markdown(f"- **{fdp.get('name', 'Unknown')}**")
                        if fdp.get('dates'):
                            st.markdown(f"  📅 {fdp['dates']}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("**🎓 Training Events**")
                for training in events.get('training_events', []):
                    if isinstance(training, dict):
                        st.markdown(f"- **{training.get('name', 'Unknown')}**")
                        if training.get('dates'):
                            st.markdown(f"  📅 {training['dates']}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Tab 5: Comparison Graphs
        with tab5:
            st.markdown('<h2 class="sub-header">Comparison with SASTRA University</h2>', unsafe_allow_html=True)
            
            fig = uni_system.create_comparison_charts(uni_name, uni_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("SASTRA University data not found in cache")

if __name__ == "__main__":
    main()









