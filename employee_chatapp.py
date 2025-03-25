import streamlit as st
import dotenv
import os
import requests

# Load environment variables
dotenv.load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
APPLICATION_TOKEN = os.getenv("langflow_token")
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = "46c21089-c9cb-4337-a0d8-aa6497766063"
ENDPOINT = "emp_chat"


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def main():
    st.title("Chat With Employees Data")

    message = st.text_area("Message", placeholder="Ask something...")

    if st.button("Submit"):
        if not message.strip():
            st.error("Please enter a message")
            return

        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))


if __name__ == "__main__":
    main()
