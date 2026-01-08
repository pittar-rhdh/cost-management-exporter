# Red Hat Cost Management Exporter

A simple FastAPI web application that retrieves and displays OpenShift cost information from the Red Hat Cost Management API.

## Features

*   **Secure Authentication**: Uses Red Hat Service Account (Client Credentials Grant) for authentication.
*   **Cost Visualization**: Aggregates and displays OpenShift costs by cluster for the current month.
*   **User-Friendly Interface**: Provides a web-based login form to enter credentials securely.
*   **Zero Configuration**: No complex environment setup required; just plug in your credentials and go.

## Prerequisites

*   Python 3.12+
*   A Red Hat Service Account with access to Cost Management.
    *   Create one at [console.redhat.com](https://console.redhat.com/iam/service-accounts).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/cost-management-exporter.git
    cd cost-management-exporter
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the application:**
    ```bash
    python main.py
    ```

2.  **Access the web interface:**
    Open your browser and navigate to `http://localhost:8000`.

3.  **Login:**
    Enter your Red Hat Service Account **Client ID** and **Client Secret** in the login form.

4.  **View Costs:**
    The application will authenticate and display a detailed table of your OpenShift cluster costs for the current month.

## Project Structure

*   `main.py`: The entry point for the FastAPI application.
*   `services/`: Contains business logic.
    *   `auth.py`: Handles authentication with Red Hat SSO.
    *   `cost_api.py`: Client for the Red Hat Cost Management API.
*   `templates/`: HTML templates for the UI.
    *   `index.html`: The main dashboard and login page.
*   `tests/`: Unit tests for the application.

## Testing

Run the unit tests to verify the application logic:

```bash
python -m unittest discover tests
```

## Contributing

1.  Create a feature branch (`git checkout -b feature/amazing-feature`).
2.  Commit your changes (`git commit -m 'Add amazing feature'`).
3.  Push to the branch (`git push origin feature/amazing-feature`).
4.  Open a Pull Request.
