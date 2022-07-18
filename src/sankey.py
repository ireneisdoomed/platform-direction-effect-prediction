from typing import Optional

import click
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo

@click.command()
@click.option('--nodes_path', help='Table with all the nodes to be represented in the diagram in TSV format.')
@click.option('--links_path', help='Table with all the links between nodes to be represented in in the diagram in TSV format.')
@click.option('--values_col', help='Name of the column in the links table to represent the strength of the flow.')
@click.option('--source', default=None, help='Optional flag to indicate a specific dataset to plot the diagram.')
def generate_sankey(nodes_path: str, links_path:str, values_col:str, source:Optional[str]=None):
    nodes = pd.read_csv(nodes_path, sep='\t')
    links = pd.read_csv(links_path, sep='\t')

    if source and source not in nodes.Label.values:
        raise ValueError("The source node is not in the nodes list")

    if source:
        # Filter the data to the data source of interest
        initial_node = nodes.query("Label == @source").Index.values[0]
        nodes_of_interest = [initial_node] + list(links.query("source == @initial_node").target.unique())
        links = links.query("source in @nodes_of_interest")

    node_dict = {y:x for x, y in enumerate(nodes.Index.values)}
    source_node = [node_dict[x] for x in links.source.values]
    target_node = [node_dict[x] for x in links.target.values]
    sankey = go.Figure( 
        data=[go.Sankey( # The plot we are interest
            # This part is for the node information
            node = dict( 
                label = nodes.Label.values
            ),
            # This part is for the link information
            link = dict(
                source = source_node,
                target = target_node,
                value = links[values_col].values
            ))],
    )
    sankey.update_layout(title=f"Direction of effect - {source}", width=1000, height=1000)
    pyo.plot(sankey, filename=f'Direction of effect - {source}', auto_open=True)

    return sankey

if __name__ == '__main__':
    generate_sankey()