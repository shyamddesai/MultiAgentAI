# NewsBridge AI

NewsBridge AI is an innovative multi-agent AI system designed to streamline market research in the energy sector. Developed for an oil and gas company, this AI-powered tool provides real-time analysis and summaries of financial news relevant to commodities trading, with a specific focus on oil and gas products such as Brent and WTI.

## Key Features
- **Automated News Collection**: Automatically scrapes thousands of news articles from open-source sources using RSS feeds and customized scraping algorithms.
- **Highlight Extraction & Summarization**: Distills large datasets into key insights, using NLP techniques to summarize relevant data concisely.
- **Sentiment Analysis**: Employs NLP models to assess the tone of news articles, offering sentiment-aware insights into the energy market's current trends.
- **Relevancy Ranking**: Prioritizes news articles based on importance, relevancy, and trader-defined keywords, allowing quick access to essential information.
- **Market Insights**: Provides trend analysis and actionable advice on commodities like Brent and WTI, tailored for the energy sector.

## Technical Stack
- **Framework**: Built with crewAI and LangChain tools for orchestrating multi-agent AI processes.
- **NLP Tools**: Utilizes BERT, OpenAI, RAKE, and spaCy for language processing, summarization, and sentiment analysis.
- **Backend**: ASGI-based architecture with multithreading support to manage high-volume real-time data processing.
- **Deployment**: Hosted on Render for reliable, scalable production deployment.

## Project Highlights
- **End-to-End Automation**: Automates news gathering, preprocessing, and summarization, giving traders real-time insights on commodities such as Naphtha and Brent WTI.
- **Real-World Impact**: Recognized by senior executives and SMEs, with a successful pilot deployment that significantly reduced research time and improved decision-making speed.

---

## Installation and Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/shyamddesai/NewsBridgeAI
   cd NewsBridgeAI
   ```

2. **Install Dependencies**:
   - Ensure Python is installed.
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure API Keys**:
   - Add your OpenAI API key to the `.env` file to enable NLP and language processing functionalities.

4. **Run the Application**:
   - Start the multi-agent processing:
     ```bash
     python MultiAgent.py
     ```

5. **Launch the Frontend**:
   - Open a new terminal and run the frontend:
     ```bash
     cd Frontend
     python app.py
     ```

## Usage
- **Custom Keywords**: Configure keywords and commodities in `crew/config.py` to tailor the news focus on specific trends or entities in the energy sector.
- **Run Multi-Agent Processing**: Start `MultiAgent.py` to activate agents that automatically gather, process, and analyze news.
- **Access Insights**: View sentiment analysis, relevancy-ranked articles, and summary reports in the `reports` directory for actionable insights.

---

## Team Members
- Shyam Desai
- Laith Al Homoud
- Zuotong Zhang
- Kaushik Krishna Mohan
- Ali Makki
