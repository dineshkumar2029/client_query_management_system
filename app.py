import streamlit as st
from auth import login_user, register_user
from query_operations import (
    insert_query,
    get_all_queries,
    close_query
)
import pandas as pd
import matplotlib.pyplot as plt

#Configuring Page UI
st.set_page_config(
    page_title="Client Query Management System",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SESSION VARIABLES
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""


st.title("Client Query Management System")


# ---------------- LOGOUT ----------------
def logout():

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""


# ---------------- BEFORE LOGIN ----------------
if not st.session_state.logged_in:

    menu = ["Login", "Register"]

    choice = st.sidebar.selectbox("Menu", menu)

    # LOGIN
    if choice == "Login":

        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login_user(username, password)

            if user:

                st.session_state.logged_in = True
                st.session_state.username = user[1]
                st.session_state.role = user[3]

                st.success("Login Successful")
                st.rerun()

            else:
                st.error("Invalid Username or Password")

    # REGISTER
    elif choice == "Register":

        st.subheader("Register")

        new_username = st.text_input("New Username")
        new_password = st.text_input(
            "New Password",
            type="password"
        )

        role = st.selectbox(
            "Select Role",
            ["Client", "Support"]
        )

        if st.button("Register"):

            success = register_user(
                new_username,
                new_password,
                role
            )

            if success:
                st.success("User Registered Successfully")

            else:
                st.error("Registration Failed")


# ---------------- AFTER LOGIN ----------------
else:

    st.sidebar.success(
        f"Logged in as {st.session_state.username}"
    )

    st.sidebar.write(
        f"Role: {st.session_state.role}"
    )

    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    # CLIENT DASHBOARD
    if st.session_state.role == "Client":

        st.header("Client Dashboard")

        st.subheader("Submit a Query")

        mail_id = st.text_input("Email ID")

        mobile_number = st.text_input("Mobile Number")

        query_heading = st.text_input("Query Heading")

        query_description = st.text_area(
            "Query Description"
        )

        if st.button("Submit Query"):
            result = insert_query(
                mail_id,
                mobile_number,
                query_heading,
                query_description
            )

            if result == "Success":

                st.success("Query Submitted Successfully")

            else:

                st.error(result)

    # SUPPORT DASHBOARD
    elif st.session_state.role == "Support":

        st.header("Support Dashboard")

        # GET QUERIES
        queries = get_all_queries()

        if queries:

            # CREATE DATAFRAME
            columns = [
                "Query ID",
                "Email",
                "Mobile",
                "Heading",
                "Description",
                "Status",
                "Created Time",
                "Closed Time"
            ]

            df = pd.DataFrame(
                queries,
                columns=columns
            )

                        # ---------------- ANALYTICS ----------------

            st.subheader("Analytics Dashboard")

            total_queries = len(df)

            open_queries_count = len(
                df[df["Status"] == "Open"]
            )

            closed_queries_count = len(
                df[df["Status"] == "Closed"]
            )

            status_counts = df["Status"].value_counts()

            # LAYOUT COLUMNS
            left_col, right_col = st.columns([1, 2])

            # LEFT SIDE METRICS
            with left_col:

                st.metric(
                    "Total Queries",
                    total_queries
                )

                st.metric(
                    "Open Queries",
                    open_queries_count
                )

                st.metric(
                    "Closed Queries",
                    closed_queries_count
                )

            # RIGHT SIDE PIE CHART
            with right_col:

                fig, ax = plt.subplots(figsize=(4, 4))

                # SHOW COUNTS
                def show_count(pct):

                    total = sum(status_counts)

                    count = int(round(pct * total / 100))

                    return f"{count}"

                ax.pie(
                    status_counts,
                    labels=status_counts.index,
                    autopct=show_count
                )

                ax.axis('equal')

                st.pyplot(fig)
            # ---------------- FILTER ----------------

            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Open", "Closed"]
            )

            if status_filter != "All":

                df = df[df["Status"] == status_filter]

            # ---------------- TABLE ----------------

            st.subheader("All Queries")

            st.dataframe(
                df,
                use_container_width=True
            )

            # ---------------- CLOSE QUERY ----------------

            st.subheader("Close Query")

            open_queries = df[df["Status"] == "Open"]

            if not open_queries.empty:

                query_id = st.selectbox(
                    "Select Query ID",
                    open_queries["Query ID"]
                )

                if st.button("Close Selected Query"):

                    success = close_query(query_id)

                    if success:

                        st.success(
                            f"Query {query_id} Closed Successfully"
                        )

                        st.rerun()

                    else:

                        st.error("Failed to Close Query")

            else:

                st.info("No Open Queries")

        else:

            st.info("No Queries Available")