import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("Phasor Addition Simulator")
st.markdown("Adjust the sliders to see the individual waves (black) and the resultant wave (red).")

# Interactive Sliders
# Added a strict upper limit to M to prevent visual clutter and lag
M = st.slider("Number of waves (M)", min_value=1, max_value=20, value=6, step=1)

# Phase difference directly in radians (0 to 2π)
p = st.slider("Phase difference in radians (Δϕ)", min_value=0.0, max_value=float(2 * np.pi), value=float(np.pi/8), step=0.05)

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
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3, arrowcolor="red"
)

# Fix the axis limits strictly based on M to prevent bounding box jitter
# This keeps the UI incredibly smooth and stops "weird messes" during recalculation
axis_limit = M * 1.05 

fig.update_layout(
    xaxis=dict(range=[-axis_limit, axis_limit], showgrid=True, zeroline=True),
    yaxis=dict(range=[-axis_limit, axis_limit], showgrid=True, zeroline=True, scaleanchor="x", scaleratio=1),
    width=600, height=600,
    plot_bgcolor="white",
    uirevision="constant", # This tells Plotly not to reset the zoom/pan/layout on every update
    margin=dict(l=20, r=20, t=20, b=20) # Reduces whitespace for a cleaner Notion embed
)

# use_container_width makes it auto-fit the Notion block nicely
st.plotly_chart(fig, use_container_width=True)