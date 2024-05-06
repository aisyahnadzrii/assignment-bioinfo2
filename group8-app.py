import streamlit as st
import requests
import networkx as nx

# UniProtKB protein data retrieval function
def get_protein_data(uniprot_id):
  url = f"https://www.ebi.ac.uk/proteins/api/proteins/{uniprot_id}"
  response = requests.get(url)
  try:
    return response.json()["results"][0]
  except (requests.exceptions.RequestException, KeyError):
    return None  # Or provide a custom error message

# Protein-Protein Interaction network generation from STRING
def get_ppi_network(uniprot_id):
  url = f"https://string-db.org/api/interactions/{uniprot_id}"
  response = requests.get(url)
  data = response.json()
  
  # Create network object
  G = nx.Graph()
  
  # Add nodes (proteins)
  for interaction in data["interactions"]:
    protein1 = interaction["protein1"]["identifier"]
    protein2 = interaction["protein2"]["identifier"]
    G.add_edge(protein1, protein2)
  
  return G

# Streamlit App
st.title("Protein Data Explorer")

# Input field for UniProt ID
uniprot_id = st.text_input("Enter UniProt ID:")

if st.button("Get Protein Data"):
  if not uniprot_id:
    st.error("Please enter a UniProt ID.")
  else:
    # Retrieve protein data
    protein_data = get_protein_data(uniprot_id)
    
    # Handle case where no data is found
    if protein_data is None:
      st.error("Protein data not found for the given ID.")
    else:
      # Display protein characteristics
      st.header("Protein Characteristics")
      try:
        st.write(f"**Entry Name:** {protein_data['entry_name']}")
      except KeyError:
        st.write("Entry Name not found.")
      st.write(f"**Protein Name:** {protein_data['protein_name']['full']}")
      st.write(f"**Length:** {protein_data['length']}")
      st.write(f"**Molecular Weight:** {protein_data['molecular_weight']}")
      
      # Get and display PPI network
      ppi_network = get_ppi_network(uniprot_id)
      st.header("Protein-Protein Interaction Network")
      nx.draw(ppi_network, with_labels=True, node_color='lightblue', edge_color='gray')
      st.pyplot()
