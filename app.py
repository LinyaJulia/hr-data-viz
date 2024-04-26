import streamlit as st
import altair as alt
from helpers import getData, style

def main():
    st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
    style.local_css("helpers/style.css")

    # I want to put a drop down where you can choose a view type
    view = st.selectbox(
        "Select a view:",
        ("Project View", "Department View"),
        index=0
    )
    st.divider()

    if(view == "Project View"):
        
        st.title("Cost per Project for March")

        costPerProject = getData.CostPerProject()

        tableContainer = st.container(border=True)
        tableContainer.subheader(costPerProject.getTitle())
        costPerProjectChart = alt.Chart(costPerProject.getDataframe()).mark_bar().encode(
            x=alt.X(costPerProject.getX(), sort=None, title=costPerProject.getXTitle()),
            y=alt.Y(costPerProject.getY(), title=costPerProject.getYTitle())
        )
        tableContainer.altair_chart(costPerProjectChart, use_container_width=True)

        tableContainer = st.container(border=True)
        tableContainer.subheader(costPerProject.getTitle())
        tableContainer.dataframe(costPerProject.getDataframe(), hide_index=True, use_container_width=True)

    if(view == "Department View"):
        st.title("Cost per Project per Team for March")

        costPerProjectPerTeam = getData.CostPerProjectPerTeam()

        team = st.selectbox(
            "Select a team:",
            costPerProjectPerTeam.getTeams(),
            index=0
        )

        CostPerProjectPerTeamContainer = st.container(border=True)
        CostPerProjectPerTeamContainer.subheader("Cost per Project for " + team)
        costPerProjectChartPerTeam = alt.Chart(costPerProjectPerTeam.getDataframe(team)).mark_bar().encode(
            x=alt.X(costPerProjectPerTeam.getX(), sort=None, title=costPerProjectPerTeam.getXTitle()),
            y=alt.Y(costPerProjectPerTeam.getY(), title=costPerProjectPerTeam.getYTitle())
        )

        CostPerProjectPerTeamContainer.altair_chart(costPerProjectChartPerTeam, use_container_width=True)

        CostPerProjectPerTeamTableContainer = st.container(border=True)
        CostPerProjectPerTeamTableContainer.subheader("Project Table")
        CostPerProjectPerTeamTableContainer.dataframe(costPerProjectPerTeam.getDataframe(team), hide_index=True, use_container_width=True)



if __name__ == '__main__':
    main()