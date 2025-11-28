📊 Content Intelligence Analyzer
A comprehensive Streamlit-based tool for analyzing content across the marketing funnel, comparing with competitors, and optimizing for different buyer personas.
🌟 Features
1. Own Content Analysis

Multi-format Input: URL, PDF, Word documents, or direct text
Automatic Content Extraction: Extract full content from web pages
Funnel Stage Detection: Automatically identify if content is Awareness, Consideration, or Decision stage
Entity Analysis: Count and analyze URLs, statistics, emails, and other entities
Heading Alignment Check: Verify content structure and heading effectiveness
Keyword Optimization: Analyze keyword density and get optimization suggestions
Save & Retrieve: Save analyses for future reference

2. Competitor Analysis

Competitive Intelligence: Analyze competitor content from any source
Gap Identification: Find opportunities where competitors are weak
Strength Analysis: Understand what competitors do well
Side-by-side Comparison: Compare your content against competitors
Historical Tracking: Save competitor analyses to track changes over time

3. Persona-Based Analysis

Persona Management: Create and manage multiple buyer personas
Excel/CSV Import: Bulk import personas from spreadsheets
Content Mapping: Map content assets to specific personas
Funnel Gap Analysis: Identify missing content for each persona at each funnel stage
Pain Point Coverage: See which persona pain points are addressed
Goal Alignment: Check if content aligns with persona goals
Priority Recommendations: Get actionable recommendations for content creation

🚀 Installation
Prerequisites

Python 3.8 or higher
pip package manager

Setup Instructions

Clone or download the repository

bash   # If using git
   git clone <your-repo-url>
   cd content-intelligence-analyzer

Install dependencies

bash   pip install -r requirements.txt

Run the application

bash   streamlit run content_analyzer.py

Access the application

The app will automatically open in your browser
Default URL: http://localhost:8501



📖 Usage Guide
Getting Started

Configure API Keys (Optional)

Click on the sidebar to expand API Configuration
Enter your API keys for OpenAI, Gemini, or Claude
Click "Save API Keys" to store them securely
Note: Basic analysis works without API keys



Tab 1: Own Content Analysis

Input Your Content

Choose input method: URL, PDF, Word Doc, or Direct Text
For URL: Enter the URL and click "Extract Content"
For files: Upload and click the extract button
For direct text: Paste content directly


Add Target Keywords

Enter target keywords in the right panel
One keyword per line
These will be analyzed for optimization


Analyze Content

Click "Analyze Content" button
View results including:

Funnel Stage: Which stage of the funnel (Awareness/Consideration/Decision)
Content Metrics: Word count, sentences, URLs, statistics
Heading Analysis: Structure and alignment
Keyword Optimization: Density and suggestions




Save Analysis

Click "Save Analysis" to store results
Access saved analyses at the bottom of the tab



Tab 2: Competitor Analysis

Add Competitor Content

Enter competitor name
Choose input method and extract content
Add relevant keywords for analysis


Analyze Competitor

Click "Analyze Competitor Content"
View insights on:

Competitor strengths
Opportunities for you
Funnel stage positioning
Content quality metrics




Save for Reference

Save competitor analyses
Track changes over time
Build competitive intelligence



Tab 3: Persona-Based Analysis
Creating Personas

Manual Entry

Fill in persona details:

Persona Name (e.g., "Marketing Manager Mary")
Role/Title
Description
Pain Points (one per line)
Goals (one per line)


Click "Add Persona"


Excel/CSV Import

Prepare a file with columns:

Persona Name
Role/Title
Description
Pain Points (comma-separated)
Goals (comma-separated)


Upload and click "Import Personas"



Analyzing Content by Persona

Select Persona

Choose from your created personas


Add Content Assets

Select asset type (Blog Post, Case Study, etc.)
Input content via URL, file, or direct text
Click "Extract Content"


Analyze for Persona

Click "Analyze for Persona"
View:

Persona relevance score
Addressed pain points and goals
Missing elements
Funnel stage


Save the analysis



Viewing Opportunities & Focus

Gap Analysis

See content distribution across personas and funnel stages
Identify missing content types


Priority Recommendations

Get actionable recommendations
Focus on high-priority gaps
Plan content creation strategy



📊 Funnel Stages Explained
🌟 Awareness Stage

Purpose: Problem recognition and education
Content Types: Blog posts, social media, infographics, videos, podcasts
Intent Signals: Educational, informational, thought leadership
Keywords: "what is", "how to", "guide", "introduction", "basics"

🔍 Consideration Stage

Purpose: Solution evaluation and comparison
Content Types: Whitepapers, ebooks, webinars, comparison guides
Intent Signals: Evaluative, comparative, solution-focused
Keywords: "vs", "comparison", "best", "top", "review", "alternative"

✅ Decision Stage

Purpose: Purchase decision and validation
Content Types: Case studies, testimonials, product demos, pricing pages
Intent Signals: Transactional, proof-seeking, validation
Keywords: "pricing", "buy", "demo", "trial", "case study", "ROI"

💾 Data Storage
All your data is stored locally in the analyzer_data folder:

analyses.json - Your content analyses
competitor_analyses.json - Competitor analyses
personas.json - Your personas
persona_analyses.json - Persona-based analyses
api_keys.json - API keys (encrypted)

Important: This data persists between sessions, so you won't lose your work!
🔧 Advanced Features
Keyword Optimization Tips

Ideal Density: 1-3% for each keyword
Natural Usage: Don't force keywords
Header Placement: Include keywords in H1, H2, H3
First 100 Words: Use main keyword early
Semantic Variations: Use related terms

Content Improvement Suggestions
The analyzer provides specific suggestions for:

Word count optimization
Heading structure improvement
Keyword placement
Entity enhancement (statistics, links)
Funnel stage alignment

Competitive Intelligence

Track competitor content strategy
Identify gaps in competitor coverage
Learn from their strengths
Find differentiation opportunities

🚀 Deployment to Streamlit Cloud

Push to GitHub

bash   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo>
   git push -u origin main

Deploy on Streamlit Cloud

Go to https://streamlit.io/cloud
Sign in with GitHub
Click "New app"
Select your repository
Main file: content_analyzer.py
Click "Deploy"


Configure Secrets (Optional)

In Streamlit Cloud dashboard, go to App Settings
Add secrets for API keys if needed



📝 Best Practices
Content Analysis

Regular Audits: Analyze your content monthly
Keyword Research: Keep target keywords updated
Competitor Tracking: Monitor competitors quarterly
Persona Updates: Refresh personas as market changes

Persona Management

Start with 3-5 personas
Use real data from customer research
Update pain points based on feedback
Map all content to personas

Gap Analysis

Prioritize decision stage content first
Create awareness content for top-of-funnel
Balance across personas
Track progress monthly

🐛 Troubleshooting
Content Extraction Issues

Problem: Can't extract from URL
Solution: Check if the URL is accessible and not behind a login

File Upload Errors

Problem: PDF/DOCX won't upload
Solution: Ensure file size is under 200MB and format is correct

Analysis Not Working

Problem: Analysis button does nothing
Solution: Ensure content is at least 100 words long

Saved Data Missing

Problem: Previous analyses disappeared
Solution: Check if analyzer_data folder exists and has correct permissions

📧 Support
For issues, questions, or feature requests:

Check this README first
Review the troubleshooting section
Check Streamlit documentation
Open an issue in the repository

🔮 Future Enhancements
Coming soon:

AI-powered content generation suggestions
Automated competitor monitoring
Content calendar integration
Multi-language support
Advanced SEO scoring
Content performance tracking
Team collaboration features

📄 License
This project is open source and available under the MIT License.
🙏 Acknowledgments
Built with:

Streamlit - The app framework
BeautifulSoup - Web scraping
PyPDF2 - PDF processing
python-docx - DOCX processing
Pandas - Data analysis


Made with ❤️ for Content Marketers
Happy Analyzing! 🚀
