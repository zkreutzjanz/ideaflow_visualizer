import json

# Load the JSON data
with open('/Users/zach/Documents/Ideaflow/ideaflow_visualizer/personal-2024-9-6.if.json', 'r') as file:
    data = json.load(file)

nodes = []
edges = []

# Process each note
for note_id, note in data['notes'].items():
    node_type = None
    content = []
    linked_note_ids = []

    # Find the first hashtag type and collect content and linkedNoteIds
    for token in note['tokens']:
        for item in token['content']:
            if item['type'] == 'hashtag' and not node_type:
                node_type = item['content'].lstrip('#')  # Remove # from node type
            if 'content' in item:
                sanitized_content = item['content'].lstrip('#').replace("'", "\\'")
                content.append(sanitized_content)  # Remove # from content and sanitize for Neo4j
            if item['type'] == 'spaceship':
                linked_note_ids.append(item['linkedNoteId'])

    # Create a node
    nodes.append({
        'id': note_id,
        'type': node_type,
        'content': ' '.join(content)
    })

    # Create edges
    for linked_note_id in linked_note_ids:
        edges.append({
            'source': note_id,
            'target': linked_note_id
        })

# Generate Cypher queries
cypher_queries = []

# Create nodes
for node in nodes:
    cypher_queries.append(f"CREATE (n:{node['type']} {{id: '{node['id']}', content: '{node['content']}'}});")

# Create edges
for edge in edges:
    cypher_queries.append(f"MATCH (a {{id: '{edge['source']}'}}), (b {{id: '{edge['target']}'}}) CREATE (a)-[:LINKS_TO]->(b);")

# Write Cypher queries to a file
with open('neo4j_import.cypher', 'w') as file:
    file.write('\n'.join(cypher_queries))

print("Cypher queries have been written to neo4j_import.cypher")