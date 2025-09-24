# News Article to Graph Database Processor

A Python prototype that transforms news articles into knowledge graphs by extracting entities and relationships using NLP, then storing them in a Neo4j graph database.

## 🚀 Features

- **Web Scraping**: Automatically extracts text from news article URLs using `newspaper3k`
- **NLP Entity Extraction**: Identifies named entities (people, organizations, locations, etc.) using spaCy
- **Relationship Mining**: Extracts subject-predicate-object relationships from article text
- **Graph Database Storage**: Stores extracted knowledge in Neo4j with proper relationships
- **Interactive CLI**: User-friendly command-line interface for processing articles

## 📋 Prerequisites

Before running this project, ensure you have:

- **Python 3.8+** installed
- **Neo4j Desktop** or **Neo4j Community** running locally
- **spaCy English model** installed

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/news-article-graph-prototype.git
cd news-article-graph-prototype
Install required packages

bash
pip install newspaper3k spacy py2neo python-dotenv
Download spaCy English model

bash
python -m spacy download en_core_web_sm
Set up environment variables
Create a .env file in the project root:

env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
🎯 Usage
Start Neo4j and ensure it's running on bolt://localhost:7687

Run the script:

bash
python news_article_to_graph.py
Enter a news article URL when prompted:

text
Enter article URL (or 'q' to quit): https://www.bbc.com/news/business-68466735
View results in Neo4j Browser (http://localhost:7474):

cypher
MATCH (n) RETURN n LIMIT 50
📊 Example Output
After processing a BBC news article, the graph database will contain:

Article Node: Contains title, URL, authors, and publish date

Entity Nodes: People, organizations, locations mentioned in the article

Relationships: Connections between entities (e.g., "CEO → LEADS → Company")

Sample Cypher Queries
cypher
// Find all articles and their mentioned entities
MATCH (a:Article)-[:MENTIONS]->(e)
RETURN a.name AS Article, e.name AS Entity, labels(e) AS Type

// Find relationships between entities
MATCH (e1)-[r]->(e2)
WHERE e1:Person OR e1:Organization OR e1:Location
RETURN e1.name, type(r), e2.name
🏗️ Project Architecture
text
Input URL → Web Scraping → NLP Processing → Graph Storage → Visualization
    ↓           ↓             ↓               ↓              ↓
 Article   Text Content  Entities & Relationships  Neo4j Database  Neo4j Browser
Key Components
scrape_article(): Extracts article content using newspaper3k

extract_entities_and_relations(): Uses spaCy for NLP processing

store_in_graphdb(): Manages Neo4j database operations

Configuration: Environment-based setup for flexibility

📁 File Structure
text
news-article-graph-prototype/
│
├── news_article_to_graph.py  # Main application script
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
└── README.md                 # This file
🔧 Technical Details
Dependencies
newspaper3k: Article extraction and parsing

spacy: NLP entity recognition and dependency parsing

py2neo: Neo4j database connectivity

python-dotenv: Environment variable management

Entity Types Extracted
PERSON, ORGANIZATION, LOCATION, DATE, MONEY, GPE, etc.

Custom relationship types based on grammatical dependencies

🐛 Troubleshooting
Common Issues
Neo4j Connection Error

Ensure Neo4j is running

Check credentials in .env file

Verify bolt://localhost:7687 is accessible

Module Not Found Errors

bash
pip install --upgrade newspaper3k spacy py2neo python-dotenv
Article Parsing Failures

Try different news sources

Check if URL is accessible without paywalls

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit changes (git commit -m 'Add amazing feature')

Push to branch (git push origin feature/amazing-feature)

Open a Pull Request

📝 License
This project is open source and available under the MIT License.

👨‍💻 Author
Nidhi


NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
