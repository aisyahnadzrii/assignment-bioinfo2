import streamlit as st
import requests
import networkx as nx
import matplotlib.pyplot as plt

# Function to retrieve protein data from UniProt
def get_protein_data(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.txt"
    response = requests.get(url)
    protein_data = {"ID": uniprot_id}  # Initialize with the UniProt ID
    for line in response.iter_lines():
        line = line.decode("utf-8")
        if line.startswith("ID"):
            fields = line.split()
            if len(fields) >= 2:
                protein_data["Name"] = ' '.join(fields[1:])
            else:
                protein_data["Name"] = "Not available"
        elif line.startswith("SQ"):
            weight_line = next(response.iter_lines()).decode("utf-8")
            weight = weight_line.split()[-1]
            protein_data["Weight"] = weight
        elif line.startswith("DE   RecName: Full="):
            function = line.split("Full=")[1].split(";")[0]
            protein_data["Function"] = function
        elif line.startswith("DR   SUPFAM"):
            structure = line.split(";")[1]
            protein_data["Structure"] = structure
        elif line.startswith("FT   MOD_RES"):
            length = int(line.split()[2])
            protein_data["Length"] = length
        elif line.startswith("CC   -!- SUBCELLULAR LOCATION:"):
            subcellular_location = line.split("CC   -!- SUBCELLULAR LOCATION:")[1].strip()
            protein_data["Subcellular Location"] = subcellular_location
        elif line.startswith("FT   MOD_RES"):
            ptms = line.split(";")[1:]
            protein_data["PTMs"] = [ptm.strip() for ptm in ptms]
        elif line.startswith("DR   Reactome"):
            pathway = line.split(";")[1]
            protein_data["Pathway"] = pathway
        elif line.startswith("DR   MIM"):
            disease = line.split(";")[1]
            protein_data["Disease"] = disease
    return protein_data

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
