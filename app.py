import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Set up the web page title
st.title("Phasor Addition Simulator")
st.markdown("Adjust the sliders to see the individual waves (black) and the resultant wave (red).")

# Interactive Sliders
M = st.slider("Number of waves (M)", min_value=1, max_value=15, value=6, step=1)
p_deg = st.slider("Phase difference in degrees (Δϕ)", min_value=0.0, max_value=180.0, value=22.5, step=1.0)

# Convert phase difference to radians
p = np.radians(p_deg)

# Initialize starting coordinates at origin (0,0)
x_coords = [0]
y_coords = [0]

# Calculate the tip coordinates of each vector tip-to-tail
for n in range(M):
    dx = np.cos(n * p)
    dy = np.sin(n * p)
    x_coords.append(x_coords[-1] + dx)
    y_coords.append(y_coords[-1] + dy)

# Create the figure
fig = go.Figure()

# Draw the individual wave vectors (Black arrows)
for i in range(M):
    fig.add_annotation(
        x=x_coords[i+1], y=y_coords[i+1],
        ax=x_coords[i], ay=y_coords[i],
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="black"
    )

# Draw the resultant sum vector (Red arrow)
fig.add_annotation(
    x=x_coords[-1], y=y_coords[-1],
    ax=x_coords[0], ay=y_coords[0],
    xref="x", yref="y", axref="x", ayref="y",
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="red"
)

# Calculate dynamic layout boundaries so the arrows always fit
max_val = max(max(np.abs(x_coords)), max(np.abs(y_coords))) + 1

fig.update_layout(
    xaxis=dict(range=[-max_val, max_val], showgrid=True, zeroline=True),
    yaxis=dict(range=[-max_val, max_val], showgrid=True, zeroline=True, scaleanchor="x", scaleratio=1), # scaleanchor ensures perfectly square proportions
    width=600, height=600,
    plot_bgcolor="white"
)

# Display the plot in the app
st.plotly_chart(fig)