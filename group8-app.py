import streamlit as st
import requests
import networkx as nx
import matplotlib.pyplot as plt

# UniProtKB protein data retrieval function
def get_protein_data(uniprot_id):
    url = f"https://www.ebi.ac.uk/proteins/api/proteins/{uniprot_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["results"][0]
    else:
        raise ValueError("Error retrieving protein data. Please check the UniProt ID.")

# Protein-Protein Interaction network generation from STRING
def get_ppi_network(uniprot_id):
    url = f"https://string-db.org/api/interactions/{uniprot_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Create network object
        G = nx.Graph()

        # Add nodes (proteins)
        for interaction in data["interactions"]:
            protein1 = interaction["protein1"]["identifier"]
            protein2 = interaction["protein2"]["identifier"]
            G.add_edge(protein1, protein2)

        return G
    else:
        raise ValueError("Error retrieving PPI network data. Please check the UniProt ID.")

# Streamlit App
st.title("Protein Data Explorer")

# Input field for UniProt ID
uniprot_id = st.text_input("Enter UniProt ID:")

if st.button("Get Protein Data"):
    if not uniprot_id:
        st.error("Please enter a UniProt ID.")
    else:
        try:
            # Retrieve protein data
            protein_data = get_protein_data(uniprot_id)

            # Display protein characteristics
            st.header("Protein Characteristics")
            st.write(f"**Entry Name:** {protein_data['entry_name']}")
            st.write(f"**Protein Name:** {protein_data['protein_name']['full']}")
            st.write(f"**Length:** {protein_data['length']}")
            st.write(f"**Molecular Weight:** {protein_data['molecular_weight']}")

            # Get and display PPI network
            ppi_network = get_ppi_network(uniprot_id)
            st.header("Protein-Protein Interaction Network")
            pos = nx.spring_layout(ppi_network)
            plt.figure(figsize=(8, 6))
            nx.draw(ppi_network, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_size=8)
            plt.title("PPI Network")
            st.pyplot(plt)
            
        except ValueError as e:
            st.error(f"{e}")
