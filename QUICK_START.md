# 🚀 Quick Setup Guide

## Step-by-Step Installation

### 1. Install Python (if not already installed)
- Download Python 3.8+ from https://python.org
- During installation, check "Add Python to PATH"
- Verify installation:
  ```bash
  python --version
  ```

### 2. Download the Application
- Download all project files to a folder
- Required files:
  - content_analyzer.py
  - analysis_modules.py
  - requirements.txt

### 3. Install Dependencies
Open terminal/command prompt in the project folder:

**Windows:**
```bash
cd path\to\content-intelligence-analyzer
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
cd path/to/content-intelligence-analyzer
pip3 install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run content_analyzer.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 🎯 First Time Usage

### Step 1: Configure API Keys (Optional)
1. Open the sidebar (click arrow on left)
2. Expand "API Keys Setup"
3. Enter your API keys:
   - OpenAI: For GPT-powered analysis
   - Gemini: For Google AI analysis
   - Claude: For Anthropic AI analysis
4. Click "Save API Keys"

**Note**: The tool works without API keys for basic analysis!

### Step 2: Analyze Your First Content

#### Option A: Analyze from URL
1. Go to "Own Content Analysis" tab
2. Select "URL" as input method
3. Enter your article/page URL
4. Click "Extract Content from URL"
5. Add target keywords (optional)
6. Click "Analyze Content"

#### Option B: Analyze from File
1. Go to "Own Content Analysis" tab
2. Select "PDF Upload" or "Word Document Upload"
3. Upload your file
4. Click extract button
5. Add target keywords (optional)
6. Click "Analyze Content"

### Step 3: Create Your First Persona
1. Go to "Persona-Based Analysis" tab
2. Click "Create Personas" sub-tab
3. Fill in the form:
   - Persona Name: "Marketing Manager Mary"
   - Role/Title: "Marketing Manager"
   - Description: "Mid-size B2B company"
   - Pain Points: "Limited budget", "Need to prove ROI"
   - Goals: "Increase qualified leads", "Improve conversion rate"
4. Click "Add Persona"

### Step 4: Analyze Content by Persona
1. Stay in "Persona-Based Analysis" tab
2. Click "Analyze Content by Persona" sub-tab
3. Select your persona from dropdown
4. Choose asset type (e.g., "Blog Post")
5. Input content (URL, file, or text)
6. Click "Analyze for Persona"
7. Save the analysis

### Step 5: View Opportunities
1. Click "Opportunities & Focus" sub-tab
2. Review gap analysis
3. See priority recommendations
4. Plan your content strategy

## 📊 Understanding the Results

### Funnel Stage Icons
- 🌟 **Awareness** - Educational content
- 🔍 **Consideration** - Comparison content
- ✅ **Decision** - Conversion content

### Relevance Scores
- **80-100%**: Excellent persona fit
- **60-79%**: Good persona fit
- **40-59%**: Moderate fit, needs improvement
- **0-39%**: Poor fit, major revisions needed

### Keyword Density
- **1-3%**: Optimal (Green)
- **<1%**: Too low (Yellow)
- **>3%**: Too high - keyword stuffing (Red)

## 🔧 Common Tasks

### Save an Analysis
- Look for the "💾 Save Analysis" button
- Click to save
- Access saved analyses at bottom of each tab

### Import Personas from Excel
1. Create Excel file with columns:
   - Persona Name
   - Role/Title
   - Description
   - Pain Points (comma-separated)
   - Goals (comma-separated)
2. Go to "Create Personas" tab
3. Select "Upload Excel/CSV"
4. Upload file
5. Click "Import Personas"

### View Saved Data
- All data saved in `analyzer_data` folder
- Files are in JSON format
- Persists between sessions

### Compare with Competitor
1. Analyze your content first (save it)
2. Go to "Competitor Analysis" tab
3. Analyze competitor content
4. Compare metrics side-by-side

## 🆘 Getting Help

### Can't Extract URL?
- Make sure URL is publicly accessible
- Check internet connection
- Try a different URL

### File Won't Upload?
- Check file size (max 200MB)
- Verify file format (.pdf or .docx)
- Try saving file in a different format

### Analysis Takes Too Long?
- Large files may take 30-60 seconds
- If over 2 minutes, refresh and try again
- Break large documents into smaller sections

### Saved Data Not Showing?
- Check if `analyzer_data` folder exists
- Verify folder has write permissions
- Try restarting the application

## 💡 Tips for Best Results

### Content Analysis
✅ **DO:**
- Analyze complete articles (not snippets)
- Use 3-5 target keywords
- Review suggestions carefully
- Save analyses for comparison

❌ **DON'T:**
- Analyze very short content (<100 words)
- Use too many keywords (>10)
- Ignore heading structure
- Skip saving important analyses

### Persona Creation
✅ **DO:**
- Base personas on real customer data
- Include 3-5 pain points
- Include 3-5 goals
- Use descriptive names

❌ **DON'T:**
- Create too many personas (>7)
- Use generic descriptions
- Skip pain points or goals
- Forget to save personas

### Gap Analysis
✅ **DO:**
- Map all content to personas
- Check all funnel stages
- Review quarterly
- Act on recommendations

❌ **DON'T:**
- Analyze content without personas
- Ignore missing stages
- Create only one content type
- Skip competitor analysis

## 🎓 Next Steps

### Week 1: Foundation
- [ ] Set up the tool
- [ ] Analyze 3-5 existing content pieces
- [ ] Create 3 buyer personas
- [ ] Identify top 3 content gaps

### Week 2: Competitor Intelligence
- [ ] Analyze 5 competitor articles
- [ ] Document their content strategy
- [ ] Identify differentiation opportunities
- [ ] Plan competitive content

### Week 3: Persona Mapping
- [ ] Map all content to personas
- [ ] Complete gap analysis
- [ ] Create content plan
- [ ] Prioritize creation

### Week 4: Optimization
- [ ] Implement keyword suggestions
- [ ] Improve heading structure
- [ ] Create gap-filling content
- [ ] Re-analyze and measure

## 📚 Additional Resources

### Learn More About:
- **Funnel Stages**: See main README.md
- **Keyword Research**: Google Keyword Planner, Ahrefs
- **Persona Development**: HubSpot Persona Generator
- **Content Strategy**: Content Marketing Institute

### Video Tutorials (Coming Soon)
- Setting up the tool
- Analyzing your first content
- Creating effective personas
- Using gap analysis

## 🎉 You're Ready!

Start analyzing your content and building a data-driven content strategy!

Questions? Check the main README.md or open an issue.

Happy analyzing! 🚀
