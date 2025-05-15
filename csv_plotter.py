import streamlit as st
import pandas as pd

@st.cache_data
def load_csv(file_obj):
    return pd.read_csv(file_obj)

st.title("CSV Quick Plotter")

uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if 'df' not in st.session_state:
    st.session_state.df = None
if 'data_source_name' not in st.session_state:
    st.session_state.data_source_name = None

if uploaded_file is not None:
    if st.session_state.data_source_name != uploaded_file.name:
        st.session_state.df = load_csv(uploaded_file)
        st.session_state.data_source_name = uploaded_file.name
    df = st.session_state.df

    # tab1, tab2 = st.tabs(['Chart', 'Dataframe'])
    # tab1.bar_chart(st.session_state.df, height=250, x="Name", y="Salary")
    # tab2.dataframe(st.session_state.df, height=250, use_container_width=True)

    st.sidebar.success(f"{uploaded_file.name} uploaded successfully.")
else:
    df = st.session_state.df

if df is not None:
    st.header("Data Preview")
    st.dataframe(df)
    st.header("Create a Plot")
    columns = df.columns.to_list()
    numeric_columns = df.select_dtypes(include=['number']).columns.to_list()

    if not numeric_columns:
        st.warning("No numeric columns in this data for plotting the y-axis")
    else:
        col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Select x-axis:", columns)
    with col2:
        y_axis = st.selectbox("Select y-axis:", numeric_columns)

    plot_type = st.radio("Select plot type:", ("Bar Chart", "Line Chart"), horizontal=True)

    if x_axis and y_axis:
        st.subheader(f"{plot_type} of {x_axis} and {y_axis}")
        if plot_type == 'Bar Chart':
            if df[x_axis].dtype == 'object' and df[x_axis].nunique() < 20:
                st.bar_chart(df.groupby(x_axis)[y_axis].mean())
                st.caption(f"Show mean of {y_axis} for each {x_axis}")
            else:
                st.bar_chart(df.set_index(x_axis)[y_axis])
        elif plot_type == "Line Chart":
            chart_data = df.sort_values(by=x_axis)
            st.line_chart(chart_data.set_index(x_axis)[y_axis])

        with st.expander("View data summary"):
            st.write("**Shape**", df.shape)
            st.write("**Columns**", df.columns.tolist())
            st.write("**Data Types**")
            st.dataframe(df.describe(include='all'))

else:
    st.info("Upload a CSV file to get started")