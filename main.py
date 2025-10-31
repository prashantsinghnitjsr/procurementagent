"""
Pharma Procurement Research Agent - Streamlit UI
Mimics Risk AI Agent styling
"""

import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Pharma Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to mimic the Risk AI Agent styling
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #f5f7fa;
    }
    
    /* Header styling */
    .main-header {
        background-color: white;
        padding: 1.5rem 2rem;
        border-bottom: 1px solid #e5e7eb;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 1.875rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
    }
    
    .main-subtitle {
        font-size: 0.875rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
    
    /* Section headers */
    .section-header {
        background-color: #eff6ff;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #3b82f6;
    }
    
    .section-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1e40af;
        margin: 0;
    }
    
    .section-description {
        font-size: 0.875rem;
        color: #1e40af;
        margin-top: 0.5rem;
        line-height: 1.5;
    }
    
    /* Risk card styling */
    .risk-card {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .risk-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .risk-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1f2937;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .risk-icon {
        color: #a855f7;
        font-size: 1.5rem;
    }
    
    .risk-badge-high {
        background-color: #fef2f2;
        color: #991b1b;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .risk-badge-medium {
        background-color: #fffbeb;
        color: #92400e;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .risk-badge-low {
        background-color: #f0fdf4;
        color: #166534;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .risk-meta {
        font-size: 0.75rem;
        color: #6b7280;
        margin-bottom: 1rem;
    }
    
    .risk-content {
        color: #374151;
        line-height: 1.6;
        font-size: 0.875rem;
    }
    
    .key-insights {
        margin-top: 1rem;
        font-weight: 600;
        color: #1f2937;
        font-size: 0.875rem;
    }
    
    .insight-list {
        margin-top: 0.5rem;
        padding-left: 1.5rem;
        color: #374151;
        font-size: 0.875rem;
    }
    
    .data-sources {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }
    
    .data-source-label {
        font-weight: 600;
        color: #6b7280;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .data-source-tag {
        display: inline-block;
        background-color: #f3f4f6;
        color: #4b5563;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        margin-top: 0.5rem;
    }
    
    /* Status indicator */
    .status-online {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background-color: #d1fae5;
        color: #065f46;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
    }
    
    /* Loading spinner */
    .loading-text {
        color: #6b7280;
        font-size: 0.875rem;
        font-style: italic;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 0.375rem;
        font-weight: 500;
        font-size: 0.875rem;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
    }
    
    /* Selectbox styling */
    .stSelectbox {
        margin-bottom: 1rem;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 0.375rem;
        border: 1px solid #d1d5db;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.375rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini API
GEMINI_API_KEY = "AIzaSyCjr4ICLBSfmgc3MQB7KhfbA9WByzPNvVU"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize session state
if 'research_data' not in st.session_state:
    st.session_state.research_data = {}
if 'research_complete' not in st.session_state:
    st.session_state.research_complete = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

def get_search_strategy(material_type: str) -> dict:
    """Define research strategy based on material type"""
    strategies = {
        "API": {
            "priority_sources": [
                "PubChem", "Google Patents", "PharmaCompass", 
                "DrugBank", "Volza", "FDA Drug Master Files", "ChemSpider"
            ],
            "focus_areas": [
                "Synthesis routes and manufacturing process",
                "Patent landscape and IP considerations",
                "GMP-certified manufacturers",
                "Regulatory status (DMF, CEP)",
                "Price premiums for pharma-grade quality"
            ]
        },
        "KSM": {
            "priority_sources": [
                "Google Patents", "PubChem", "Volza", 
                "ChemAnalyst", "ICIS", "Supplier directories"
            ],
            "focus_areas": [
                "Upstream raw material dependencies",
                "Chinese/Indian manufacturing dominance",
                "Patent considerations for synthesis routes",
                "Scale-up challenges",
                "Backward integration opportunities"
            ]
        },
        "Excipient": {
            "priority_sources": [
                "PharmaCompass", "USP/EP/JP Pharmacopeia", "Volza",
                "IPEC", "PubChem", "Manufacturer websites"
            ],
            "focus_areas": [
                "Pharmacopeial compliance (USP/EP/JP)",
                "Functional categories and applications",
                "Allergen and safety considerations",
                "Supply chain diversity",
                "Commodity vs specialty pricing"
            ]
        },
        "Solvent": {
            "priority_sources": [
                "ICH Q3C guidelines", "PubChem", "ICIS/ChemAnalyst",
                "Volza", "Green chemistry databases", "Distributor catalogs"
            ],
            "focus_areas": [
                "ICH classification (Class 1/2/3)",
                "Residual solvent limits",
                "Green chemistry alternatives",
                "Bulk commodity pricing",
                "Regional availability and logistics"
            ]
        }
    }
    return strategies.get(material_type, strategies["API"])

def research_step(step_number: int, material_type: str, material_name: str, previous_context: str = "") -> str:
    """Execute a research step"""
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    strategy = get_search_strategy(material_type)
    
    prompts = {
        1: f"""Research {material_type}: {material_name}

RELIABLE SOURCES ONLY:
{', '.join(strategy['priority_sources'])}

Provide:
1. MATERIAL DEFINITION & PROPERTIES (Chemical name, CAS, formula, properties)
2. FORMATION PROCESS & SYNTHESIS (Synthesis routes, starting materials, yields)

Be specific, cite sources.""",
        
        2: f"""Analyze SUPPLY CHAIN for {material_type}: {material_name}

Context: {previous_context[:1500]}

Provide:
1. RAW MATERIAL SOURCING (Starting materials, geographic sources)
2. MANUFACTURING LANDSCAPE (Major countries, manufacturers, concentration)
3. SUPPLY CHAIN RISKS (Dependencies, geographic risks, regulatory barriers)
4. DISTRIBUTION CHANNELS (Lead times, MOQs)""",
        
        3: f"""Build SHOULD-COST MODEL for {material_type}: {material_name}

Context: {previous_context[:1500]}

Provide:
1. RAW MATERIAL COSTS (Each material + quantity per kg)
2. MANUFACTURING COSTS (Labor, energy, equipment by region)
3. OVERHEAD & QUALITY COSTS (GMP premium, QC, regulatory)
4. TOTAL COST BUILDUP (Raw + Manufacturing + Overhead + Margin)
5. REGIONAL COST VARIATIONS""",
        
        4: f"""Research MARKET PRICING for {material_type}: {material_name}

Should-cost: {previous_context[:1500]}

Sources: PharmaCompass, Volza, Supplier catalogs

Provide:
1. MARKET PRICE RANGE (Spot, bulk, contract prices)
2. VOLZA TRADE DATA (Import prices, trends, volume tiers)
3. PRICE vs SHOULD-COST COMPARISON
4. QUALITY PREMIUMS
5. PRICING RED FLAGS""",
        
        5: f"""Identify HSN/HS CODES for {material_type}: {material_name}

Context: {previous_context[:1000]}

Provide:
1. PRIMARY HSN/HS CODES (6-digit HS, 8-digit HSN, 10-digit HTS)
2. ALTERNATIVE/RELATED CODES
3. TRADE CLASSIFICATION NOTES (Tariffs, restrictions)
4. CODES TO MONITOR (Related materials)
5. TRADE DATA SEARCH STRATEGY""",
        
        6: f"""Analyze TRADE PATTERNS for {material_type}: {material_name}

HSN context: {previous_context[:1000]}

Sources: Volza, UN Comtrade

Provide:
1. TOP EXPORTING COUNTRIES (Rank, market share, prices)
2. TOP IMPORTING COUNTRIES
3. TRADE FLOWS & PATTERNS
4. MARKET CONCENTRATION ANALYSIS
5. PROCUREMENT INSIGHTS""",
        
        7: f"""Identify SUPPLIERS for {material_type}: {material_name}

Trade context: {previous_context[:1500]}

Sources: PharmaCompass, FDA DMF, EMA, Volza

Provide:
1. TIER 1 SUPPLIERS (Name, location, credentials, capacity)
2. TIER 2 SUPPLIERS (Alternatives)
3. TIER 3 SUPPLIERS (Emerging)
4. SUPPLIER EVALUATION CRITERIA
5. RED FLAGS & DUE DILIGENCE
6. PROCUREMENT RECOMMENDATIONS

List 5-10 actual suppliers."""
    }
    
    response = model.generate_content(prompts.get(step_number, ""))
    return response.text

def create_risk_card(title: str, content: str, risk_level: str = "HIGH", sources: list = None, icon: str = "🔍"):
    """Create a styled risk card matching the image"""
    
    # Determine badge color
    badge_class = {
        "HIGH": "risk-badge-high",
        "MEDIUM": "risk-badge-medium",
        "LOW": "risk-badge-low"
    }.get(risk_level, "risk-badge-high")
    
    # Parse content for key insights
    parts = content.split("Key Insights:")
    analysis = parts[0] if len(parts) > 0 else content
    insights = parts[1] if len(parts) > 1 else ""
    
    # Format sources
    source_tags = ""
    if sources:
        for source in sources:
            source_tags += f'<span class="data-source-tag">{source}</span> '
    
    card_html = f"""
    <div class="risk-card">
        <div class="risk-card-header">
            <div class="risk-title">
                <span class="risk-icon">{icon}</span>
                <span>{title}</span>
            </div>
            <span class="{badge_class}">{risk_level}</span>
        </div>
        
        <div class="risk-meta">
            {len(sources) if sources else 1} source(s) • Multiple insights
        </div>
        
        <div class="risk-content">
            <strong>Analysis:</strong><br>
            {analysis}
        </div>
        
        {f'<div class="key-insights"><strong>Key Insights:</strong><div class="insight-list">{insights}</div></div>' if insights else ''}
        
        <div class="data-sources">
            <div class="data-source-label">Data Sources:</div>
            {source_tags if source_tags else '<span class="data-source-tag">AI Research</span>'}
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 class="main-title">Pharma Research Agent</h1>
                <p class="main-subtitle">AI-powered procurement intelligence</p>
            </div>
            <div class="status-online">
                <span class="status-dot"></span>
                Backend Online
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        material_type = st.selectbox(
            "Select Material Type",
            ["API", "KSM", "Excipient", "Solvent"],
            key="material_type"
        )
    
    with col2:
        material_name = st.text_input(
            "Material Name",
            placeholder="e.g., Ibuprofen, Paracetamol",
            key="material_name"
        )
    
    with col3:
        st.write("")  # Spacer
        st.write("")  # Spacer
        start_research = st.button("🔬 Start Research", use_container_width=True)
    
    # Research execution
    if start_research and material_name:
        st.session_state.research_complete = False
        st.session_state.research_data = {}
        st.session_state.current_step = 0
        
        # Progress container
        progress_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = [
                ("Material Overview", "🔍"),
                ("Supply Chain Analysis", "🌐"),
                ("Should-Cost Model", "💰"),
                ("Market Pricing", "📊"),
                ("HSN Codes", "📋"),
                ("Trade Analysis", "🌍"),
                ("Supplier Identification", "🏭")
            ]
            
            for i, (step_name, icon) in enumerate(steps, 1):
                status_text.markdown(f'<p class="loading-text">{icon} Step {i}/7: {step_name}...</p>', unsafe_allow_html=True)
                progress_bar.progress(i / 7)
                
                # Execute research
                previous_context = ""
                if i > 1:
                    previous_context = st.session_state.research_data.get(f'step_{i-1}', '')
                
                result = research_step(i, material_type, material_name, previous_context)
                st.session_state.research_data[f'step_{i}'] = result
                
                time.sleep(1)  # Rate limiting
            
            status_text.markdown('<p class="loading-text">✅ Research completed!</p>', unsafe_allow_html=True)
            st.session_state.research_complete = True
    
    # Display results
    if st.session_state.research_complete and st.session_state.research_data:
        st.markdown("---")
        
        # Market Intelligence Section (like in the image)
        st.markdown("""
        <div class="section-header">
            <h2 class="section-title">Market Intelligence</h2>
            <p class="section-description">
                Comprehensive analysis of {material} covering formation, supply chain, pricing, trade patterns, and qualified suppliers.
            </p>
        </div>
        """.format(material=material_name), unsafe_allow_html=True)
        
        # Risk Category Analysis
        st.markdown("<h3 style='color: #1f2937; margin-top: 2rem; margin-bottom: 1rem;'>Research Category Analysis</h3>", unsafe_allow_html=True)
        
        # Create cards for each section
        sections = [
            ("Material Overview & Formation", st.session_state.research_data.get('step_1', ''), "HIGH", ["PubChem", "Google Patents"], "🔬"),
            ("Supply Chain Structure", st.session_state.research_data.get('step_2', ''), "HIGH", ["Volza", "PharmaCompass"], "🌐"),
            ("Should-Cost Model", st.session_state.research_data.get('step_3', ''), "MEDIUM", ["ChemAnalyst", "ICIS"], "💰"),
            ("Market Pricing Analysis", st.session_state.research_data.get('step_4', ''), "HIGH", ["Volza", "PharmaCompass"], "📊"),
            ("HSN/HS Code Intelligence", st.session_state.research_data.get('step_5', ''), "MEDIUM", ["Customs Database", "Volza"], "📋"),
            ("International Trade Patterns", st.session_state.research_data.get('step_6', ''), "HIGH", ["Volza", "UN Comtrade"], "🌍"),
            ("Qualified Suppliers", st.session_state.research_data.get('step_7', ''), "HIGH", ["PharmaCompass", "FDA DMF"], "🏭")
        ]
        
        # Display in two columns
        col1, col2 = st.columns(2)
        
        for idx, (title, content, risk, sources, icon) in enumerate(sections):
            with col1 if idx % 2 == 0 else col2:
                with st.expander(f"{icon} {title}", expanded=(idx < 2)):
                    create_risk_card(title, content, risk, sources, icon)
        
        # Download report button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            # Generate report text
            report = f"""
PHARMA PROCUREMENT RESEARCH REPORT
{'='*80}

Material Type: {material_type}
Material Name: {material_name}
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*80}

"""
            for title, content, _, _, _ in sections:
                report += f"\n{title.upper()}\n{'='*80}\n{content}\n\n"
            
            st.download_button(
                label="📥 Download Full Report",
                data=report,
                file_name=f"pharma_research_{material_type}_{material_name}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )

if __name__ == "__main__":

    main()
