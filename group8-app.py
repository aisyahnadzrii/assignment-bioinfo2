import streamlit as st
from Bio.SeqIO import parse
from Bio.SeqUtils import molecular_weight
import matplotlib.pyplot as plt
import networkx as nx
import requests
from io import StringIO
import logging

# Function to fetch protein data from Uniprot
def fetch_protein_data(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Error fetching protein data. Please check the Uniprot ID.")
    fasta_data = response.text
    try:
        records = parse(StringIO(fasta_data), "fasta")
        record = next(records)  # Get the first record
        length = len(record.seq)
        weight = molecular_weight(record.seq)
        return {'length': length, 'weight': weight}
    except StopIteration:
        raise ValueError("No protein sequence found in the provided data.")
    except (ValueError, SeqIO.ParserError) as e:
        logging.error(f"Error parsing protein data: {e}")
        raise ValueError("Error parsing protein data. Please check the Uniprot ID.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise ValueError("An unexpected error occurred.")

# Function to retrieve protein-protein interaction network from STRING DB
def fetch_ppi_network(uniprot_id):
    # Placeholder function - replace with actual implementation
    # Here, let's assume we have a dummy network for demonstration
    G = nx.Graph()
    G.add_node(uniprot_id)
    G.add_nodes_from(["Interactor1", "Interactor2", "Interactor3"])
    G.add_edges_from([(uniprot_id, "Interactor1"), (uniprot_id, "Interactor2"), (uniprot_id, "Interactor3")])
    return G

# Function for sequence alignment using Biopython
def perform_sequence_alignment(sequence1, sequence2):
    # Placeholder function - replace with actual implementation
    # Here, let's assume we are performing a simple local alignment
    # This is just a demonstration, you should replace this with proper sequence alignment code
    alignment_score = len(sequence1) + len(sequence2)  # Dummy score
    return alignment_score

# Streamlit app
def main():
    st.title("Protein Data Analysis App")

    # Sidebar for user input
    option = st.sidebar.selectbox("Select Input Type", ("Uniprot ID", "Protein Sequence"))

    if option == "Uniprot ID":
        uniprot_id = st.sidebar.text_input("Enter Uniprot ID")
        if st.sidebar.button("Fetch Data"):
            protein_data = fetch_protein_data(uniprot_id)
            display_protein_info(protein_data)

            # Fetch PPI network
            ppi_network = fetch_ppi_network(uniprot_id)
            display_ppi_network(ppi_network)

    elif option == "Protein Sequence":
        protein_sequence = st.sidebar.text_area("Enter Protein Sequence")
        if st.sidebar.button("Analyze Sequence"):
            display_analysis_results(protein_sequence)

def display_protein_info(protein_data):
    # Display protein characteristics
    st.write("Protein Characteristics:")
    st.write("Length:", protein_data['length'])
    st.write("Weight:", protein_data['weight'])

def display_ppi_network(ppi_network):
    # Visualize PPI network
    st.write("Protein-Protein Interaction Network:")
    pos = nx.spring_layout(ppi_network)
    nx.draw(ppi_network, pos, with_labels=True)
    plt.title("Protein-Protein Interaction Network")
    st.pyplot()

def display_analysis_results(protein_sequence):
    # Perform sequence analysis
    st.write("Performing Sequence Analysis:")
    # Perform sequence alignment (dummy example)
    alignment_score = perform_sequence_alignment(protein_sequence, protein_sequence[::-1])
    st.write("Sequence Alignment Score:", alignment_score)

if __name__ == "__main__":
    main()
