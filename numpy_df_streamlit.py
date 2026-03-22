# numpy_random.py
import numpy as np
import pandas as pd
import streamlit as st
st.write()
num_rows = st.slider("Number of rows", 1, 10000, 500)
data = []
for i in range(num_rows):
    data.append(
        {
            "Preview": f"https://picsum.photos/400/200?lock={i}",
            "Views": np.random.randint(0, 1000),
            "Active": np.random.choice([True, False]),
            "Category": np.random.choice(["🤖 LLM", "📊 Data", "⚙️ Tool"]),
            "Progress": np.random.randint(1, 100),
        }
    )
### continuation of numpy_random.py



data = pd.DataFrame(data)

st.subheader("Top 10 Views")
st.line_chart(data["Views"].head(10))

config = {
    "Preview": st.column_config.ImageColumn(),
    "Progress": st.column_config.ProgressColumn(),
}

if st.toggle("Enable editing"):
    edited_data = st.data_editor(data, column_config=config, use_container_width=True)
else:
    st.dataframe(data, column_config=config, use_container_width=True)
