import datetime

import pandas as pd
import requests
import streamlit as st
from services.blob_service import BlobStorageService
from services.credit_card_service import CreditCardValidator
from services.data_base import DatabaseService
from streamlit_lottie import st_lottie

# Global services initialization
CREDIT_CARD_VALIDATOR = CreditCardValidator()
BLOB_STORAGE_SERVICE = BlobStorageService()
DATABASE_SERVICE = DatabaseService()


def load_lottie(url: str):
    """Loads animation from Lottie Files."""
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def render_sidebar():
    """
    Renders the application sidebar with navigation and developer information.

    Returns:
        str: Selected page in the menu
    """
    menu_options = {
        "Home": "🏠",
        "Card Analysis": "💳",
        "Database Query": "🔍",
        "Documentation": "📚",
        "About": "ℹ️",
    }

    selected_page = st.sidebar.radio(
        "Menu",
        list(menu_options.keys()),
        format_func=lambda x: f"{x} {menu_options[x]}",
    )

    return selected_page


def process_card_analysis(uploaded_file):
    """
    Processes the uploaded credit card image.

    Args:
        uploaded_file (UploadedFile): Uploaded image file

    Returns:
        tuple: Card information and validation result, or None
    """
    try:
        st.image(uploaded_file, caption="Card Image", use_column_width=True)

        with st.spinner("Processing..."):
            file_name = uploaded_file.name
            file = uploaded_file.getvalue()
            blob_url = BLOB_STORAGE_SERVICE.upload_blob(file, file_name)

            if not blob_url:
                st.error("Error uploading image to Blob Storage.")
                return None

            card_info = CREDIT_CARD_VALIDATOR.detect_credit_card_info_from_url(
                blob_url)
            if not card_info:
                st.error("Unable to analyze card.")
                return None

            validation_result = CREDIT_CARD_VALIDATOR.validate_card_info(
                card_info)
            return card_info, validation_result

    except Exception as e:
        st.error(f"Error during card analysis: {e}")
        return None


def database_query_page():
    """
    Database query page that automatically displays all data
    and allows custom queries with ready-made examples.
    """
    st.title("🔍 Database Query")

    # Automatically display all data when loading the page
    st.subheader("📊 All Records in `credit_cards` Table")
    try:
        all_data = DATABASE_SERVICE.get_all_cards()
        if all_data:
            df_all = pd.DataFrame(all_data)
            st.dataframe(df_all, use_container_width=True)

            # Button to export all data as CSV
            csv_all = df_all.to_csv(index=False)
            st.download_button(
                label="💾 Download All Data (CSV)",
                data=csv_all,
                file_name="all_credit_cards_data.csv",
                mime="text/csv",
            )
        else:
            st.info("⚠️ No data found in `credit_cards` table.")
    except Exception as e:
        st.error(f"Error loading all data: {e}")

    # Allow custom queries
    st.markdown("---")
    st.subheader("🔎 Custom Queries")
    st.markdown(
        """
        **Query Examples:**
        - All records: `SELECT * FROM credit_cards`
        - Cards by id: `SELECT * FROM credit_cards WHERE id = 1`
        - Cards by name: `SELECT * FROM credit_cards WHERE card_name = "GABRIEL LIMA"`
        - Cards issued by bank: `SELECT * FROM credit_cards WHERE bank_name = 'Bank X'`
        """
    )

    # SQL query text box
    query = st.text_area(
        "Enter your SQL query:",
        placeholder="Example: SELECT * FROM credit_cards WHERE bank_name = 'Bank X'",
        height=150,
    )

    if st.button("Execute Query"):
        try:
            # Execute custom query
            results = DATABASE_SERVICE.execute_custom_query(query)

            if results:
                # Convert results to DataFrame
                df_results = pd.DataFrame(results)
                st.dataframe(df_results, use_container_width=True)

                # Button to export results as CSV
                csv_results = df_results.to_csv(index=False)
                st.download_button(
                    label="💾 Download Results (CSV)",
                    data=csv_results,
                    file_name="query_results.csv",
                    mime="text/csv",
                )
            else:
                st.info("🔍 No results found for the query.")
        except ValueError as ve:
            st.error(f"❌ Validation error: {ve}")
        except Exception as e:
            st.error(f"❌ Error executing query: {e}")


def home_page():
    """
    Renders the home page with project description.
    """
    st.title("🌟 Simplifying Card Validation in E-commerce")
    # Load animation
    lottie_translate = load_lottie(
        "https://lottie.host/c6d163ab-0ab8-49aa-8c50-332eb30e3774/kktucbjshh.json"
    )
    st_lottie(lottie_translate, height=300)
    st.markdown(
        """
      Have you ever wondered how some e-commerce platforms use advanced technologies
      to facilitate purchases and prevent fraud? Remember that magical moment when,
      instead of typing all your card details while finishing a purchase, you can
      simply send a photo?
      #### 💡 Our Proposal
      This project demonstrates exactly how that magic happens! Using Azure's
      Artificial Intelligence, we've implemented a card validation system that
      makes this process not only possible but extremely simple.
      #### 🚀 How It Works
      1. Upload the card image
      2. AI analyzes the data instantly
      3. Receive validation in seconds
      4. Data is stored for future analysis
      #### 🎯 Benefits
      - Automatic information detection without typing
      - Intuitive and friendly interface
      - Storage for future analysis
      - Easy queries with CSV export
      #### 🔍 Exploring the Project
      This is a demonstration project that uses cutting-edge Azure technologies
      to show how to implement card validation efficiently. Although it's a
      POC (Proof of Concept), it already includes the main elements needed
      for a complete system:
      - Accurate card data extraction
      - Real-time validation
      - Structured storage
      - Data analysis interface
      #### 🎯 Objective
      To demonstrate in practice how modern technologies can be applied to
      create solutions that significantly improve user experience in
      financial transactions.
    """
    )


def documentation_page():
    """
    Renders the documentation page.
    """
    st.title("📚 Documentation")
    st.markdown(
        """
      # Credit Card Analyzer Documentation

      ## Overview

      This application uses the Azure Document Intelligence API to extract credit card information from images. The extracted data is then validated and persisted in a SQLite database.

      ## Main Features

      * **Image Upload:** Allows users to upload a credit card image.
      * **Image Analysis:** Uses Azure Document Intelligence API to detect and extract information such as card number, expiration date, cardholder name, and bank name.
      * **Card Validation:** Performs basic validation of the card number and expiration date.
      * **Data Storage:** Stores card information (including validation result) in a SQLite database.
      * **Data Query:** Allows querying stored data using SQL queries.
      * **Data Export:** Allows exporting query results to a CSV file.

      ## Architecture

      The application follows a three-tier architecture:

      1. **Frontend (Streamlit):** User interface for user interaction.
      2. **Backend (Python):** Business logic, including interaction with Azure services and database.
      3. **Azure Services:** Azure Document Intelligence and Azure Blob Storage.

      ## Technologies Used

      * **Streamlit:** Python framework for creating web applications.
      * **Python:** Programming language.
      * **Azure Document Intelligence:** Azure service for document information extraction.
      * **Azure Blob Storage:** Azure service for storing binary data objects.
      * **SQLite:** Relational database management system.
    """
    )


def about_page():
    """
    Renders the about page.
    """
    st.title("ℹ️ About")
    st.markdown(
        """
      ### 🎯 Credit Card Analyzer Project

      This project is a Proof of Concept (POC) developed as part of the
      [Bootcamp Microsoft Certification Challenge #1 - AI 102](https://www.dio.me/bootcamp/microsoft-ai-102). The goal is to demonstrate the practical
      application of modern development concepts and integration with Azure
      cloud services.

      #### 🛠️ Technologies Used
      - **Frontend**: Streamlit
      - **Backend**: Python
      - **Cloud**: Azure Services
      - **Database**: SQLite
      - **Version Control**: Git

      #### 🌟 Features
      - Intuitive interface
      - Image processing and validation
      - Database storage
      - Data analysis and export
      - Azure services integration (Document Intelligence and Blob Storage)

      #### 📝 Note
      This is an educational and demonstration project and should not be used
      in a production environment without proper adaptations and security measures.
    """
    )


def card_analysis_page():
    """
    Page for credit card analysis.
    """
    st.title("💳 Card Analysis")
    uploaded_file = st.file_uploader(
        "Upload card image", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file and st.button("💳 Analyze Card"):
        result = process_card_analysis(uploaded_file)
        if result:
            card_info, validation_result = result

            st.write("Card Information:")
            st.write(card_info)

            if validation_result["is_valid"]:
                st.success("✅ Valid Card")
                existing_card = DATABASE_SERVICE.get_card_by_number(
                    card_info["card_number"]
                )

                if existing_card:
                    st.info(
                        f"Card already exists in database. ID: {existing_card['id']}"
                    )
                else:
                    card_info["is_valid"] = validation_result["is_valid"]
                    card_info["processed_at"] = datetime.datetime.now().isoformat()
                    DATABASE_SERVICE.insert_card(card_info)
                    st.success("Card inserted into database!")
            else:
                st.error("❌ Invalid Card")


def main():
    """
    Entry point for the Credit Card Analyzer application.
    """
    st.set_page_config(page_title="Credit Card Analyzer",
                       page_icon="💳", layout="wide")

    # Page mapping
    page_handlers = {
        "Home": home_page,
        "Card Analysis": card_analysis_page,
        "Database Query": database_query_page,
        "Documentation": documentation_page,
        "About": about_page,
    }

    # Render selected page
    selected_page = render_sidebar()
    handler = page_handlers.get(selected_page)

    if handler:
        handler()


if __name__ == "__main__":
    main()
