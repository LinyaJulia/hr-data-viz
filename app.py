import streamlit as st
import altair as alt
from helpers import getData, ui

def main():

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
        visualWidth = int((ui.getScreenWidth()*0.85))

        tableContainer = st.container(border=True)
        tableContainer.subheader("Cost per Project")
        tableContainer.write(alt.Chart(costPerProject.getDataframe()).mark_bar().encode(
            x=alt.X(costPerProject.getX(), sort=None, title="Project"),
            y=alt.Y(costPerProject.getY(), title="Cost"),
        ).properties(
            width=visualWidth,
            height=500
        ))
        
        tableContainer = st.container(border=True)
        tableContainer.subheader("Project Table")
        tableContainer.dataframe(costPerProject.getDataframe(), width=visualWidth, hide_index=True)

    if(view == "Department View"):
        st.title("Cost per Project per Team for March")

        costPerProjectPerTeam = getData.CostPerProjectPerTeam()
        visualWidth = int((ui.getScreenWidth()*0.85))

        team = st.selectbox(
            "Select a team:",
            costPerProjectPerTeam.getTeams(),
            index=0
        )

        CostPerProjectPerTeamContainer = st.container(border=True)
        CostPerProjectPerTeamContainer.subheader("Cost per Project for " + team)
        CostPerProjectPerTeamContainer.write(alt.Chart(costPerProjectPerTeam.getDataframe(team)).mark_bar().encode(
            x=alt.X(costPerProjectPerTeam.getX(), sort=None, title="Project"),
            y=alt.Y(costPerProjectPerTeam.getY(), title="Cost"),
        ).properties(
            width=(visualWidth),
            height=500
        ))

        CostPerProjectPerTeamTableContainer = st.container(border=True)
        CostPerProjectPerTeamTableContainer.subheader("Project Table")
        CostPerProjectPerTeamTableContainer.dataframe(costPerProjectPerTeam.getDataframe(team), width=visualWidth, hide_index=True)






        return None


if __name__ == '__main__':
    main()