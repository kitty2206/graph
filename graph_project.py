"""
News Article to Graph Database Prototype
This script asks for a news article URL, extracts entities and relationships,
and stores them in a Neo4j graph database.
"""

# Import required libraries
from newspaper import Article
import spacy
from py2neo import Graph, Node, Relationship
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize NLP model
print("Loading NLP model...")
nlp = spacy.load("en_core_web_sm")

# Initialize Neo4j connection
graph = Graph(
    os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
    auth=(
        os.getenv('NEO4J_USER', 'neo4j'),
        os.getenv('NEO4J_PASSWORD', 'password')
    )
)

def scrape_article(url):
    """Extract text from a news article URL"""
    print(f"\nScraping article from {url}...")
    article = Article(url)
    article.download()
    article.parse()
    
    return {
        'title': article.title,
        'text': article.text,
        'authors': article.authors,
        'publish_date': article.publish_date,
        'url': url
    }

def extract_entities_and_relations(article_text):
    """Extract entities and their relationships from text"""
    print("Extracting entities and relationships...")
    doc = nlp(article_text)
    
    entities = {}
    relationships = []
    
    # Extract named entities
    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = set()
        entities[ent.label_].add(ent.text)
    
    # Convert sets to lists for JSON serialization
    entities = {k: list(v) for k, v in entities.items()}
    
    # Extract simple subject-predicate relationships
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ("nsubj", "nsubjpass"):
                subject = token.text
                for child in token.children:
                    if child.dep_ in ("attr", "acomp", "dobj"):
                        predicate = child.lemma_.upper()  # Use lemma and uppercase for consistency
                        obj = " ".join([t.text for t in child.subtree if t.dep_ != "det"])
                        relationships.append((subject, predicate, obj))
    
    return {
        'entities': entities,
        'relationships': relationships
    }

def store_in_graphdb(article_data, entity_data):
    """Store article data and entities in Neo4j"""
    print("Storing data in graph database...")
    
    # Clear existing data (for testing)
    graph.delete_all()
    
    # Create article node
    article_node = Node(
        "Article",
        name=article_data['title'],
        url=article_data['url'],
        publish_date=str(article_data['publish_date']),
        authors=', '.join(article_data['authors'])
    )
    graph.create(article_node)
    
    # Create entity nodes and store relationships to article
    entity_nodes = {}
    for entity_type, entity_names in entity_data['entities'].items():
        for entity_name in entity_names:
            if entity_name not in entity_nodes:
                node = Node(entity_type, name=entity_name)
                entity_nodes[entity_name] = node
                graph.create(node)
                # Link entity to article
                rel = Relationship(article_node, "MENTIONS", node)
                graph.create(rel)
    
    # Create relationships between entities
    for rel in entity_data['relationships']:
        subject, predicate, obj = rel
        if subject in entity_nodes and obj in entity_nodes:
            relationship = Relationship(
                entity_nodes[subject], 
                predicate, 
                entity_nodes[obj]
            )
            graph.create(relationship)
    
    print(f"Stored {len(entity_nodes)} entities and {len(entity_data['relationships'])} relationships")

def get_article_url():
    """Prompt user to enter a news article URL"""
    print("\n" + "="*50)
    print("News Article to Graph Database Processor")
    print("="*50 + "\n")
    print("Please enter a news article URL to analyze (e.g., from BBC, CNN, etc.)")
    print("Example: https://www.bbc.com/news/business-68466735")
    
    while True:
        url = input("\nEnter article URL (or 'q' to quit): ").strip()
        if url.lower() == 'q':
            return None
        if url.startswith(('http://', 'https://')):
            return url
        print("Invalid URL. Please include http:// or https://")

def main():
    """Main execution function"""
    while True:
        article_url = get_article_url()
        if not article_url:
            print("\nExiting program...")
            break
            
        try:
            # Step 1: Scrape article
            article_data = scrape_article(article_url)
            
            # Step 2: Extract entities and relationships
            entity_data = extract_entities_and_relations(article_data['text'])
            
            # Step 3: Store in graph database
            store_in_graphdb(article_data, entity_data)
            
            print("\n" + "="*50)
            print("Processing Complete!")
            print("="*50)
            print(f"Article title: {article_data['title']}")
            print(f"Found {sum(len(v) for v in entity_data['entities'].values())} entities")
            print(f"Found {len(entity_data['relationships'])} relationships")
            print("\nYou can now view the graph in Neo4j Browser (http://localhost:7474)")
            print("Try running: MATCH (n) RETURN n LIMIT 50")
            
        except Exception as e:
            print(f"\nError processing article: {e}")
            print("Please try a different URL or check the article is accessible.")

if __name__ == "__main__":
    # Display instructions
    print("""
Requirements:
1. Neo4j running (default: bolt://localhost:7687)
2. .env file with credentials or edit the code
3. Python packages: newspaper3k, spacy, py2neo, python-dotenv

The script will:
1. Ask for a news article URL
2. Extract entities and relationships
3. Store them in Neo4j
""")
    main()