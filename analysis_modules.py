import streamlit as st
import requests
from bs4 import BeautifulSoup
import PyPDF2
import docx
import io
import re
from datetime import datetime
import pandas as pd
from collections import Counter
import json

# Funnel stage definitions
FUNNEL_STAGES = {
    'awareness': {
        'emoji': '🌟',
        'title': 'Awareness',
        'description': 'Top of funnel - Problem recognition and education',
        'content_types': ['blog_post', 'social_media', 'infographic', 'video', 'podcast'],
        'intent_signals': ['educational', 'informational', 'thought_leadership'],
        'keywords': ['what is', 'how to', 'guide', 'introduction', 'beginner', 'basics', 'overview', 'understanding']
    },
    'consideration': {
        'emoji': '🔍',
        'title': 'Consideration',
        'description': 'Middle of funnel - Solution evaluation and comparison',
        'content_types': ['whitepaper', 'ebook', 'webinar', 'comparison_guide', 'how_to'],
        'intent_signals': ['evaluative', 'comparative', 'solution_focused'],
        'keywords': ['vs', 'comparison', 'best', 'top', 'review', 'evaluate', 'choose', 'alternative', 'solution']
    },
    'decision': {
        'emoji': '✅',
        'title': 'Decision',
        'description': 'Bottom of funnel - Purchase decision and validation',
        'content_types': ['case_study', 'testimonial', 'product_demo', 'pricing', 'roi_calculator'],
        'intent_signals': ['transactional', 'proof_seeking', 'validation'],
        'keywords': ['pricing', 'buy', 'purchase', 'demo', 'trial', 'case study', 'testimonial', 'roi', 'results']
    }
}

def extract_content_from_url(url):
    """Extract text content from a URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Extract headings
        headings = []
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for heading in soup.find_all(tag):
                headings.append({
                    'level': tag,
                    'text': heading.get_text().strip()
                })
        
        return {
            'success': True,
            'content': text,
            'headings': headings,
            'url': url
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def extract_content_from_pdf(pdf_file):
    """Extract text content from a PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        return {
            'success': True,
            'content': text,
            'headings': [],
            'source': 'PDF Upload'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def extract_content_from_docx(docx_file):
    """Extract text content from a DOCX file"""
    try:
        doc = docx.Document(docx_file)
        text = ""
        headings = []
        
        for para in doc.paragraphs:
            text += para.text + "\n"
            if para.style.name.startswith('Heading'):
                headings.append({
                    'level': para.style.name,
                    'text': para.text
                })
        
        return {
            'success': True,
            'content': text,
            'headings': headings,
            'source': 'DOCX Upload'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def analyze_funnel_stage(content):
    """Determine the funnel stage of the content"""
    content_lower = content.lower()
    scores = {}
    
    for stage, config in FUNNEL_STAGES.items():
        score = 0
        # Check for keyword matches
        for keyword in config['keywords']:
            if keyword in content_lower:
                score += content_lower.count(keyword)
        scores[stage] = score
    
    # Determine primary stage
    primary_stage = max(scores, key=scores.get)
    confidence = scores[primary_stage] / (sum(scores.values()) + 1)
    
    return {
        'primary_stage': primary_stage,
        'confidence': confidence,
        'scores': scores,
        'stage_info': FUNNEL_STAGES[primary_stage]
    }

def extract_entities(content):
    """Extract and count different entities from content"""
    # Extract URLs
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
    
    # Extract emails
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
    
    # Extract numbers/statistics
    numbers = re.findall(r'\b\d+%|\b\d+\.\d+%|\$\d+|\d+x\b', content)
    
    # Word count and sentence count
    words = content.split()
    sentences = re.split(r'[.!?]+', content)
    
    # Extract potential company names (capitalized words)
    potential_companies = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
    
    return {
        'total_words': len(words),
        'total_sentences': len([s for s in sentences if s.strip()]),
        'urls_count': len(urls),
        'emails_count': len(emails),
        'statistics_count': len(numbers),
        'urls': urls[:10],  # Limit to 10
        'statistics': numbers[:20],  # Limit to 20
        'avg_words_per_sentence': len(words) / max(len([s for s in sentences if s.strip()]), 1)
    }

def analyze_heading_alignment(content, headings):
    """Analyze if content is aligned with headings"""
    if not headings:
        return {
            'aligned': False,
            'message': 'No headings found in the content',
            'suggestions': ['Add clear H1, H2, H3 headings to structure your content']
        }
    
    analysis = []
    suggestions = []
    
    for heading in headings:
        heading_text = heading['text'].lower()
        # Simple alignment check - look for keywords from heading in surrounding content
        alignment_score = sum(1 for word in heading_text.split() if word in content.lower())
        
        analysis.append({
            'heading': heading['text'],
            'level': heading['level'],
            'alignment_score': alignment_score
        })
    
    # Generate suggestions
    if len(headings) < 3:
        suggestions.append("Add more headings to improve content structure (aim for 3-5 main sections)")
    
    avg_alignment = sum(h['alignment_score'] for h in analysis) / len(analysis)
    if avg_alignment < 3:
        suggestions.append("Ensure heading keywords appear in the content below each heading")
    
    return {
        'aligned': avg_alignment >= 3,
        'heading_analysis': analysis,
        'suggestions': suggestions if suggestions else ['Content structure looks good!']
    }

def analyze_keyword_optimization(content, target_keywords):
    """Analyze content for keyword optimization"""
    if not target_keywords:
        return {
            'optimized': False,
            'message': 'No target keywords provided'
        }
    
    content_lower = content.lower()
    keyword_analysis = []
    
    for keyword in target_keywords:
        keyword_lower = keyword.lower()
        count = content_lower.count(keyword_lower)
        
        # Calculate keyword density
        total_words = len(content.split())
        density = (count / total_words) * 100 if total_words > 0 else 0
        
        # Determine if optimization is good (1-3% density is generally good)
        status = 'good' if 1 <= density <= 3 else ('low' if density < 1 else 'high')
        
        keyword_analysis.append({
            'keyword': keyword,
            'count': count,
            'density': round(density, 2),
            'status': status
        })
    
    # Generate optimization suggestions
    suggestions = []
    for kw in keyword_analysis:
        if kw['status'] == 'low':
            suggestions.append(f"Increase usage of '{kw['keyword']}' (current: {kw['count']} times, {kw['density']}%)")
        elif kw['status'] == 'high':
            suggestions.append(f"Reduce usage of '{kw['keyword']}' to avoid keyword stuffing (current: {kw['count']} times, {kw['density']}%)")
    
    if not suggestions:
        suggestions.append("Keyword optimization looks good! Maintain natural usage.")
    
    # Add general SEO suggestions
    suggestions.extend([
        "Include target keywords in the first 100 words",
        "Use keywords in headings (H1, H2, H3)",
        "Add keywords to meta title and description",
        "Use semantic variations of your keywords"
    ])
    
    return {
        'optimized': all(kw['status'] == 'good' for kw in keyword_analysis),
        'keyword_analysis': keyword_analysis,
        'suggestions': suggestions
    }

def call_ai_api(content, prompt, api_provider='openai'):
    """Call AI API for advanced analysis"""
    api_keys = st.session_state.api_keys
    
    if api_provider == 'openai' and api_keys.get('openai'):
        try:
            import openai
            openai.api_key = api_keys['openai']
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a content marketing expert analyzing content for funnel stages, optimization, and improvements."},
                    {"role": "user", "content": f"{prompt}\n\nContent:\n{content[:4000]}"}
                ],
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"API Error: {str(e)}"
    
    # Fallback analysis if no API key
    return "Advanced AI analysis requires API key configuration. Basic analysis completed."

def render_own_content_tab():
    """Render the Own Content Analysis tab"""
    st.markdown('<h2 class="sub-header">🎯 Your Content Analysis</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    Analyze your own content to understand its funnel stage, optimization level, and improvement opportunities.
    Upload content via URL, PDF, or Word document.
    """)
    
    # Content input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📥 Input Content")
        
        input_method = st.radio(
            "Choose input method:",
            ["URL", "PDF Upload", "Word Document Upload", "Direct Text"],
            horizontal=True
        )
        
        content = None
        headings = []
        source = ""
        
        if input_method == "URL":
            url = st.text_input("Enter URL:", placeholder="https://example.com/article")
            if st.button("🔍 Extract Content from URL"):
                with st.spinner("Extracting content..."):
                    result = extract_content_from_url(url)
                    if result['success']:
                        content = result['content']
                        headings = result['headings']
                        source = result['url']
                        st.success("✅ Content extracted successfully!")
                    else:
                        st.error(f"❌ Error: {result['error']}")
        
        elif input_method == "PDF Upload":
            pdf_file = st.file_uploader("Upload PDF file", type=['pdf'])
            if pdf_file and st.button("📄 Extract Content from PDF"):
                with st.spinner("Extracting content..."):
                    result = extract_content_from_pdf(pdf_file)
                    if result['success']:
                        content = result['content']
                        headings = result['headings']
                        source = result['source']
                        st.success("✅ Content extracted successfully!")
                    else:
                        st.error(f"❌ Error: {result['error']}")
        
        elif input_method == "Word Document Upload":
            docx_file = st.file_uploader("Upload Word document", type=['docx'])
            if docx_file and st.button("📝 Extract Content from Document"):
                with st.spinner("Extracting content..."):
                    result = extract_content_from_docx(docx_file)
                    if result['success']:
                        content = result['content']
                        headings = result['headings']
                        source = result['source']
                        st.success("✅ Content extracted successfully!")
                    else:
                        st.error(f"❌ Error: {result['error']}")
        
        else:  # Direct Text
            content = st.text_area("Paste your content here:", height=300)
            source = "Direct Text Input"
            if content:
                st.info("✅ Content ready for analysis")
    
    with col2:
        st.subheader("🎯 Target Keywords")
        keywords_input = st.text_area(
            "Enter target keywords (one per line):",
            height=200,
            placeholder="content marketing\nSEO optimization\ndigital strategy"
        )
        target_keywords = [kw.strip() for kw in keywords_input.split('\n') if kw.strip()]
        
        if target_keywords:
            st.info(f"📊 {len(target_keywords)} keywords added")
    
    # Analysis section
    if content and len(content) > 100:
        st.markdown("---")
        st.subheader("🔬 Content Analysis")
        
        if st.button("🚀 Analyze Content", type="primary"):
            with st.spinner("Analyzing content..."):
                # Perform all analyses
                funnel_analysis = analyze_funnel_stage(content)
                entity_analysis = extract_entities(content)
                heading_analysis = analyze_heading_alignment(content, headings)
                keyword_analysis = analyze_keyword_optimization(content, target_keywords)
                
                # Store results
                analysis_result = {
                    'timestamp': datetime.now().isoformat(),
                    'source': source,
                    'content_preview': content[:500],
                    'funnel_analysis': funnel_analysis,
                    'entity_analysis': entity_analysis,
                    'heading_analysis': heading_analysis,
                    'keyword_analysis': keyword_analysis,
                    'target_keywords': target_keywords
                }
                
                # Display results
                st.markdown("### 📊 Analysis Results")
                
                # Funnel Stage
                stage = funnel_analysis['primary_stage']
                stage_info = funnel_analysis['stage_info']
                
                st.markdown(f"""
                <div class="funnel-{stage}">
                    <h3>{stage_info['emoji']} {stage_info['title']} Stage</h3>
                    <p><strong>Confidence:</strong> {funnel_analysis['confidence']:.1%}</p>
                    <p>{stage_info['description']}</p>
                    <p><strong>Typical Content Types:</strong> {', '.join(stage_info['content_types'])}</p>
                    <p><strong>Intent Signals:</strong> {', '.join(stage_info['intent_signals'])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Entity Analysis
                st.markdown("### 📈 Content Metrics")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Words", f"{entity_analysis['total_words']:,}")
                col2.metric("Sentences", entity_analysis['total_sentences'])
                col3.metric("URLs Found", entity_analysis['urls_count'])
                col4.metric("Statistics", entity_analysis['statistics_count'])
                
                # Heading Analysis
                st.markdown("### 📑 Heading Structure Analysis")
                if heading_analysis['aligned']:
                    st.markdown('<div class="strength-box">✅ Content structure is well-aligned with headings</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="improvement-box">⚠️ Content structure needs improvement</div>', unsafe_allow_html=True)
                
                if headings:
                    with st.expander("View Heading Analysis"):
                        for h in heading_analysis['heading_analysis']:
                            st.write(f"**{h['level'].upper()}:** {h['heading']} (Alignment Score: {h['alignment_score']})")
                
                st.markdown("**Suggestions:**")
                for suggestion in heading_analysis['suggestions']:
                    st.write(f"• {suggestion}")
                
                # Keyword Optimization
                if target_keywords:
                    st.markdown("### 🎯 Keyword Optimization Analysis")
                    
                    if keyword_analysis['optimized']:
                        st.markdown('<div class="strength-box">✅ Keywords are well-optimized</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="improvement-box">⚠️ Keyword optimization needs attention</div>', unsafe_allow_html=True)
                    
                    # Keyword table
                    kw_df = pd.DataFrame(keyword_analysis['keyword_analysis'])
                    st.dataframe(kw_df, use_container_width=True)
                    
                    st.markdown("**Optimization Suggestions:**")
                    for suggestion in keyword_analysis['suggestions']:
                        st.write(f"• {suggestion}")
                
                # Save analysis
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button("💾 Save Analysis"):
                        st.session_state.saved_analyses.append(analysis_result)
                        from content_analyzer import save_data
                        if save_data('analyses', st.session_state.saved_analyses):
                            st.success("✅ Analysis saved!")
    
    # View saved analyses
    if st.session_state.saved_analyses:
        st.markdown("---")
        st.subheader("📚 Saved Analyses")
        
        for idx, analysis in enumerate(reversed(st.session_state.saved_analyses)):
            with st.expander(f"Analysis {len(st.session_state.saved_analyses) - idx}: {analysis['source']} - {analysis['timestamp'][:10]}"):
                st.write(f"**Source:** {analysis['source']}")
                st.write(f"**Date:** {analysis['timestamp']}")
                st.write(f"**Funnel Stage:** {analysis['funnel_analysis']['stage_info']['emoji']} {analysis['funnel_analysis']['stage_info']['title']}")
                st.write(f"**Content Preview:** {analysis['content_preview']}...")

def render_competitor_tab():
    """Render the Competitor Analysis tab"""
    st.markdown('<h2 class="sub-header">🔍 Competitor Content Analysis</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    Analyze competitor content to identify gaps, opportunities, and optimization strategies.
    Compare their content against your own to gain competitive insights.
    """)
    
    # Similar structure to own content but with competitor focus
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📥 Competitor Content Input")
        
        comp_input_method = st.radio(
            "Choose input method:",
            ["URL", "PDF Upload", "Word Document Upload", "Direct Text"],
            horizontal=True,
            key="comp_input"
        )
        
        competitor_name = st.text_input("Competitor Name:", placeholder="e.g., Competitor Inc.")
        
        content = None
        headings = []
        source = ""
        
        if comp_input_method == "URL":
            url = st.text_input("Enter Competitor URL:", placeholder="https://competitor.com/article", key="comp_url")
            if st.button("🔍 Extract Competitor Content"):
                with st.spinner("Extracting content..."):
                    result = extract_content_from_url(url)
                    if result['success']:
                        content = result['content']
                        headings = result['headings']
                        source = result['url']
                        st.success("✅ Content extracted successfully!")
                    else:
                        st.error(f"❌ Error: {result['error']}")
        
        elif comp_input_method == "PDF Upload":
            pdf_file = st.file_uploader("Upload Competitor PDF", type=['pdf'], key="comp_pdf")
            if pdf_file and st.button("📄 Extract Competitor PDF Content"):
                with st.spinner("Extracting content..."):
                    result = extract_content_from_pdf(pdf_file)
                    if result['success']:
                        content = result['content']
                        headings = result['headings']
                        source = "Competitor PDF"
                        st.success("✅ Content extracted successfully!")
                    else:
                        st.error(f"❌ Error: {result['error']}")
        
        elif comp_input_method == "Word Document Upload":
            docx_file = st.file_uploader("Upload Competitor Document", type=['docx'], key="comp_docx")
            if docx_file and st.button("📝 Extract Competitor Document Content"):
                with st.spinner("Extracting content..."):
                    result = extract_content_from_docx(docx_file)
                    if result['success']:
                        content = result['content']
                        headings = result['headings']
                        source = "Competitor Document"
                        st.success("✅ Content extracted successfully!")
                    else:
                        st.error(f"❌ Error: {result['error']}")
        
        else:
            content = st.text_area("Paste competitor content:", height=300, key="comp_text")
            source = "Competitor Direct Input"
    
    with col2:
        st.subheader("🎯 Analysis Keywords")
        comp_keywords_input = st.text_area(
            "Keywords to analyze:",
            height=200,
            key="comp_keywords",
            placeholder="keyword 1\nkeyword 2\nkeyword 3"
        )
        comp_keywords = [kw.strip() for kw in comp_keywords_input.split('\n') if kw.strip()]
    
    # Competitor Analysis
    if content and competitor_name and len(content) > 100:
        st.markdown("---")
        
        if st.button("🚀 Analyze Competitor Content", type="primary", key="analyze_comp"):
            with st.spinner("Analyzing competitor content..."):
                funnel_analysis = analyze_funnel_stage(content)
                entity_analysis = extract_entities(content)
                heading_analysis = analyze_heading_alignment(content, headings)
                keyword_analysis = analyze_keyword_optimization(content, comp_keywords)
                
                comp_analysis = {
                    'timestamp': datetime.now().isoformat(),
                    'competitor_name': competitor_name,
                    'source': source,
                    'content_preview': content[:500],
                    'funnel_analysis': funnel_analysis,
                    'entity_analysis': entity_analysis,
                    'heading_analysis': heading_analysis,
                    'keyword_analysis': keyword_analysis
                }
                
                st.markdown(f"### 📊 Analysis: {competitor_name}")
                
                # Funnel Stage
                stage = funnel_analysis['primary_stage']
                stage_info = funnel_analysis['stage_info']
                
                st.markdown(f"""
                <div class="funnel-{stage}">
                    <h4>{stage_info['emoji']} {stage_info['title']} Stage Content</h4>
                    <p>{stage_info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Comparative Insights
                st.markdown("### 💡 Competitive Insights")
                
                insights_col1, insights_col2 = st.columns(2)
                
                with insights_col1:
                    st.markdown("#### 💪 Competitor Strengths")
                    strengths = []
                    
                    if entity_analysis['total_words'] > 1500:
                        strengths.append(f"✅ Comprehensive content ({entity_analysis['total_words']:,} words)")
                    if entity_analysis['statistics_count'] > 5:
                        strengths.append(f"✅ Data-driven ({entity_analysis['statistics_count']} statistics)")
                    if len(headings) >= 5:
                        strengths.append(f"✅ Well-structured ({len(headings)} headings)")
                    
                    if strengths:
                        for strength in strengths:
                            st.write(strength)
                    else:
                        st.write("Basic content structure")
                
                with insights_col2:
                    st.markdown("#### 🎯 Opportunities for You")
                    opportunities = []
                    
                    if entity_analysis['total_words'] < 1000:
                        opportunities.append("📝 Create more comprehensive content")
                    if entity_analysis['statistics_count'] < 3:
                        opportunities.append("📊 Add more data and statistics")
                    if len(headings) < 3:
                        opportunities.append("📑 Improve content structure")
                    
                    if opportunities:
                        for opp in opportunities:
                            st.write(opp)
                    else:
                        st.write("Competitor has strong content - focus on differentiation")
                
                # Save analysis
                if st.button("💾 Save Competitor Analysis"):
                    st.session_state.competitor_analyses.append(comp_analysis)
                    from content_analyzer import save_data
                    if save_data('competitor_analyses', st.session_state.competitor_analyses):
                        st.success("✅ Competitor analysis saved!")
    
    # View saved competitor analyses
    if st.session_state.competitor_analyses:
        st.markdown("---")
        st.subheader("📚 Saved Competitor Analyses")
        
        for idx, analysis in enumerate(reversed(st.session_state.competitor_analyses)):
            with st.expander(f"{analysis['competitor_name']} - {analysis['timestamp'][:10]}"):
                st.write(f"**Competitor:** {analysis['competitor_name']}")
                st.write(f"**Source:** {analysis['source']}")
                st.write(f"**Funnel Stage:** {analysis['funnel_analysis']['stage_info']['title']}")

def render_persona_tab():
    """Render the Persona-Based Analysis tab"""
    st.markdown('<h2 class="sub-header">👥 Persona-Based Content Analysis</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    Create buyer personas and analyze your content library to identify gaps and opportunities for each persona.
    """)
    
    # Sub-tabs for persona management
    persona_subtab1, persona_subtab2, persona_subtab3 = st.tabs([
        "🆕 Create Personas",
        "📊 Analyze Content by Persona",
        "🎯 Opportunities & Focus"
    ])
    
    with persona_subtab1:
        st.subheader("Create or Import Personas")
        
        persona_input_method = st.radio(
            "How would you like to add personas?",
            ["Manual Entry", "Upload Excel/CSV"],
            horizontal=True
        )
        
        if persona_input_method == "Manual Entry":
            with st.form("persona_form"):
                st.markdown("#### Add New Persona")
                
                persona_name = st.text_input("Persona Name*", placeholder="e.g., Marketing Manager Mary")
                role_title = st.text_input("Role/Title*", placeholder="e.g., Marketing Manager")
                description = st.text_area("Description", placeholder="Brief description of this persona")
                pain_points = st.text_area("Pain Points (one per line)", placeholder="Challenge 1\nChallenge 2\nChallenge 3")
                goals = st.text_area("Goals (one per line)", placeholder="Goal 1\nGoal 2\nGoal 3")
                
                submitted = st.form_submit_button("➕ Add Persona")
                
                if submitted and persona_name and role_title:
                    new_persona = {
                        'id': len(st.session_state.personas) + 1,
                        'name': persona_name,
                        'role': role_title,
                        'description': description,
                        'pain_points': [p.strip() for p in pain_points.split('\n') if p.strip()],
                        'goals': [g.strip() for g in goals.split('\n') if g.strip()],
                        'created_at': datetime.now().isoformat()
                    }
                    
                    st.session_state.personas.append(new_persona)
                    from content_analyzer import save_data
                    save_data('personas', st.session_state.personas)
                    st.success(f"✅ Persona '{persona_name}' added successfully!")
                    st.rerun()
        
        else:
            st.markdown("#### Upload Persona Data")
            uploaded_file = st.file_uploader(
                "Upload Excel or CSV file",
                type=['xlsx', 'xls', 'csv'],
                help="File should have columns: Persona Name, Role/Title, Description, Pain Points, Goals"
            )
            
            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.write("Preview:")
                    st.dataframe(df.head())
                    
                    if st.button("📥 Import Personas"):
                        for _, row in df.iterrows():
                            new_persona = {
                                'id': len(st.session_state.personas) + 1,
                                'name': row.get('Persona Name', ''),
                                'role': row.get('Role/Title', ''),
                                'description': row.get('Description', ''),
                                'pain_points': str(row.get('Pain Points', '')).split(',') if pd.notna(row.get('Pain Points')) else [],
                                'goals': str(row.get('Goals', '')).split(',') if pd.notna(row.get('Goals')) else [],
                                'created_at': datetime.now().isoformat()
                            }
                            st.session_state.personas.append(new_persona)
                        
                        from content_analyzer import save_data
                        save_data('personas', st.session_state.personas)
                        st.success(f"✅ {len(df)} personas imported successfully!")
                        st.rerun()
                
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        # Display existing personas
        if st.session_state.personas:
            st.markdown("---")
            st.subheader("📋 Your Personas")
            
            for persona in st.session_state.personas:
                with st.expander(f"👤 {persona['name']} - {persona['role']}"):
                    st.write(f"**Description:** {persona['description']}")
                    st.write(f"**Pain Points:**")
                    for pp in persona['pain_points']:
                        st.write(f"  • {pp}")
                    st.write(f"**Goals:**")
                    for goal in persona['goals']:
                        st.write(f"  • {goal}")
                    
                    if st.button(f"🗑️ Delete", key=f"del_{persona['id']}"):
                        st.session_state.personas = [p for p in st.session_state.personas if p['id'] != persona['id']]
                        from content_analyzer import save_data
                        save_data('personas', st.session_state.personas)
                        st.rerun()
    
    with persona_subtab2:
        st.subheader("Analyze Content for Personas")
        
        if not st.session_state.personas:
            st.warning("⚠️ Please create personas first in the 'Create Personas' tab")
        else:
            selected_persona = st.selectbox(
                "Select Persona:",
                options=st.session_state.personas,
                format_func=lambda p: f"{p['name']} ({p['role']})"
            )
            
            st.markdown(f"### Analyzing for: {selected_persona['name']}")
            
            # Content assets input
            st.subheader("📎 Add Content Assets")
            
            asset_type = st.selectbox(
                "Asset Type:",
                ["Blog Post", "Case Study", "Solution Page", "Webinar", "One-Pager", "White Paper", "Other"]
            )
            
            asset_input = st.radio(
                "Input Method:",
                ["URL", "File Upload", "Direct Text"],
                horizontal=True,
                key="persona_asset_input"
            )
            
            content = None
            asset_url = ""
            
            if asset_input == "URL":
                asset_url = st.text_input("Asset URL:", key="persona_url")
                if st.button("Extract Content", key="persona_extract"):
                    result = extract_content_from_url(asset_url)
                    if result['success']:
                        content = result['content']
                        st.success("✅ Content extracted!")
            
            elif asset_input == "File Upload":
                uploaded = st.file_uploader("Upload file", type=['pdf', 'docx'], key="persona_file")
                if uploaded:
                    if uploaded.name.endswith('.pdf'):
                        result = extract_content_from_pdf(uploaded)
                    else:
                        result = extract_content_from_docx(uploaded)
                    
                    if result['success']:
                        content = result['content']
                        st.success("✅ Content extracted!")
            
            else:
                content = st.text_area("Paste content:", height=200, key="persona_content")
            
            if content and st.button("🔬 Analyze for Persona", key="analyze_persona"):
                with st.spinner("Analyzing content for persona fit..."):
                    funnel_analysis = analyze_funnel_stage(content)
                    entity_analysis = extract_entities(content)
                    
                    # Persona-specific analysis
                    persona_relevance_score = 0
                    relevant_pain_points = []
                    relevant_goals = []
                    
                    content_lower = content.lower()
                    
                    # Check for pain points
                    for pain_point in selected_persona['pain_points']:
                        if any(word.lower() in content_lower for word in pain_point.split()):
                            persona_relevance_score += 1
                            relevant_pain_points.append(pain_point)
                    
                    # Check for goals
                    for goal in selected_persona['goals']:
                        if any(word.lower() in content_lower for word in goal.split()):
                            persona_relevance_score += 1
                            relevant_goals.append(goal)
                    
                    persona_analysis = {
                        'timestamp': datetime.now().isoformat(),
                        'persona': selected_persona,
                        'asset_type': asset_type,
                        'asset_url': asset_url,
                        'content_preview': content[:500],
                        'funnel_stage': funnel_analysis['primary_stage'],
                        'persona_relevance_score': persona_relevance_score,
                        'relevant_pain_points': relevant_pain_points,
                        'relevant_goals': relevant_goals,
                        'entity_analysis': entity_analysis
                    }
                    
                    st.markdown("### 📊 Persona Analysis Results")
                    
                    # Relevance score
                    relevance_pct = (persona_relevance_score / (len(selected_persona['pain_points']) + len(selected_persona['goals']))) * 100 if (len(selected_persona['pain_points']) + len(selected_persona['goals'])) > 0 else 0
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Persona Relevance", f"{relevance_pct:.0f}%")
                    col2.metric("Funnel Stage", funnel_analysis['stage_info']['emoji'] + " " + funnel_analysis['stage_info']['title'])
                    col3.metric("Content Type", asset_type)
                    
                    # Relevant pain points and goals
                    st.markdown("#### ✅ Addressed in Content")
                    pcol1, pcol2 = st.columns(2)
                    
                    with pcol1:
                        st.write("**Pain Points:**")
                        if relevant_pain_points:
                            for pp in relevant_pain_points:
                                st.write(f"✅ {pp}")
                        else:
                            st.write("❌ None addressed")
                    
                    with pcol2:
                        st.write("**Goals:**")
                        if relevant_goals:
                            for goal in relevant_goals:
                                st.write(f"✅ {goal}")
                        else:
                            st.write("❌ None addressed")
                    
                    # Missing elements
                    st.markdown("#### ⚠️ Missing from Content")
                    missing_pain = [pp for pp in selected_persona['pain_points'] if pp not in relevant_pain_points]
                    missing_goals = [g for g in selected_persona['goals'] if g not in relevant_goals]
                    
                    if missing_pain:
                        st.write("**Pain Points to Address:**")
                        for pp in missing_pain:
                            st.write(f"• {pp}")
                    
                    if missing_goals:
                        st.write("**Goals to Highlight:**")
                        for goal in missing_goals:
                            st.write(f"• {goal}")
                    
                    # Save analysis
                    if st.button("💾 Save Persona Analysis"):
                        st.session_state.persona_analyses.append(persona_analysis)
                        from content_analyzer import save_data
                        save_data('persona_analyses', st.session_state.persona_analyses)
                        st.success("✅ Analysis saved!")
    
    with persona_subtab3:
        st.subheader("🎯 Opportunities & Focus Areas")
        
        if not st.session_state.persona_analyses:
            st.warning("⚠️ No persona analyses yet. Analyze some content in the previous tab!")
        else:
            st.markdown("### 📈 Content Gap Analysis")
            
            # Create summary by persona and funnel stage
            persona_content_map = {}
            
            for analysis in st.session_state.persona_analyses:
                persona_name = analysis['persona']['name']
                funnel_stage = analysis['funnel_stage']
                asset_type = analysis['asset_type']
                
                if persona_name not in persona_content_map:
                    persona_content_map[persona_name] = {
                        'awareness': [],
                        'consideration': [],
                        'decision': []
                    }
                
                persona_content_map[persona_name][funnel_stage].append(asset_type)
            
            # Display gap analysis
            for persona_name, stages in persona_content_map.items():
                st.markdown(f"#### 👤 {persona_name}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("##### 🌟 Awareness")
                    awareness_count = len(stages['awareness'])
                    if awareness_count > 0:
                        st.success(f"✅ {awareness_count} assets")
                        for asset in stages['awareness']:
                            st.write(f"  • {asset}")
                    else:
                        st.error("❌ No content")
                        st.write("**Create:** Blog posts, Educational content")
                
                with col2:
                    st.markdown("##### 🔍 Consideration")
                    consideration_count = len(stages['consideration'])
                    if consideration_count > 0:
                        st.success(f"✅ {consideration_count} assets")
                        for asset in stages['consideration']:
                            st.write(f"  • {asset}")
                    else:
                        st.error("❌ No content")
                        st.write("**Create:** Webinars, Comparison guides")
                
                with col3:
                    st.markdown("##### ✅ Decision")
                    decision_count = len(stages['decision'])
                    if decision_count > 0:
                        st.success(f"✅ {decision_count} assets")
                        for asset in stages['decision']:
                            st.write(f"  • {asset}")
                    else:
                        st.error("❌ No content")
                        st.write("**Create:** Case studies, ROI calculators")
                
                st.markdown("---")
            
            # Overall recommendations
            st.markdown("### 💡 Priority Recommendations")
            
            recommendations = []
            
            for persona_name, stages in persona_content_map.items():
                if len(stages['awareness']) == 0:
                    recommendations.append({
                        'priority': 'High',
                        'persona': persona_name,
                        'action': f"Create Awareness stage content (blog posts, educational resources)"
                    })
                
                if len(stages['decision']) == 0:
                    recommendations.append({
                        'priority': 'High',
                        'persona': persona_name,
                        'action': f"Create Decision stage content (case studies, testimonials)"
                    })
                
                if len(stages['consideration']) == 0:
                    recommendations.append({
                        'priority': 'Medium',
                        'persona': persona_name,
                        'action': f"Create Consideration stage content (webinars, comparison guides)"
                    })
            
            if recommendations:
                rec_df = pd.DataFrame(recommendations)
                st.dataframe(rec_df, use_container_width=True)
            else:
                st.success("✅ Great job! You have content across all funnel stages for all personas.")
