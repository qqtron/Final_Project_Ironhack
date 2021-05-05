import streamlit as st
import properties as p


def get_property_zones():
    return list(set(list(p.CorporateProperty.zones()) + list(p.TraditionalProperty.zones()) + list(p.TouristProperty.zones())))


title = st.title('Rental profitability analyzer')

zone = st.sidebar.selectbox(
    "Select a zone", get_property_zones())

bedrooms = st.sidebar.select_slider(
    "Bedrooms", (1, 2, 3, 4))

acquisition_price = st.sidebar.number_input(
    "Acquisition price", 0)

process = st.sidebar.button(
    "Get data")


if process and acquisition_price != 0:
    st.write(p.CorporateProperty(zone, bedrooms, acquisition_price))
    st.write(p.TouristProperty(zone, bedrooms, acquisition_price))
    st.write(p.TraditionalProperty(zone, bedrooms, acquisition_price))


