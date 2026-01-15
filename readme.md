# Find Nearest Tracked City - Streamlit App

A web application to find the nearest tracked city from a predefined list of US cities.

## Features

- Enter any US city name to find the nearest tracked city
- Optional state selection for more accurate geocoding
- Option to prioritize same-state matches or search all states
- Displays top 5 nearest tracked cities with distances
- Shows 130+ tracked cities across all US states

## Local Development

### Prerequisites
- Python 3.9+
- pip

### Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

5. Open your browser to `http://localhost:8501`

## Azure Deployment

### Option 1: Deploy via Azure Portal

1. **Create an Azure App Service:**
   - Go to Azure Portal → Create a resource → Web App
   - Choose:
     - Runtime stack: Python 3.10 or 3.11
     - Operating System: Linux
     - Region: Choose your preferred region

2. **Configure Deployment:**
   - Go to your App Service → Deployment Center
   - Choose your source (GitHub, Local Git, or ZIP deploy)
   - Connect your repository or upload files

3. **Configure Startup Command:**
   - Go to Configuration → General settings
   - Set Startup Command to:
   ```
   python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0
   ```

4. **Set Environment Variable (Optional):**
   - Go to Configuration → Application settings
   - Add: `WEBSITES_PORT` = `8000`

### Option 2: Deploy via Azure CLI

1. **Login to Azure:**
```bash
az login
```

2. **Create a resource group (if needed):**
```bash
az group create --name myResourceGroup --location eastus
```

3. **Create an App Service plan:**
```bash
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux
```

4. **Create the web app:**
```bash
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name my-nearest-city-app --runtime "PYTHON:3.10"
```

5. **Configure startup command:**
```bash
az webapp config set --resource-group myResourceGroup --name my-nearest-city-app --startup-file "python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0"
```

6. **Deploy the code:**
```bash
# From the project directory
zip -r deploy.zip .
az webapp deploy --resource-group myResourceGroup --name my-nearest-city-app --src-path deploy.zip
```

### Option 3: Deploy via VS Code

1. Install the Azure App Service extension
2. Right-click on the project folder
3. Select "Deploy to Web App..."
4. Follow the prompts to create or select an App Service
5. After deployment, configure the startup command in Azure Portal

## Project Structure

```
nearest_city_app/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── startup.sh          # Startup script for Azure
└── README.md           # This file
```

## Configuration

The app uses the Nominatim geocoding service (OpenStreetMap) which is free but has usage limits. For production use with high traffic, consider:

1. Adding caching for geocoded results
2. Using a commercial geocoding API (Google Maps, Azure Maps, etc.)
3. Implementing rate limiting

## Tracked Cities

The app includes 130+ tracked cities across all US states. The full list can be viewed in the app's sidebar.

## Troubleshooting

### App not loading on Azure
- Check that the startup command is correct
- Verify WEBSITES_PORT is set to 8000
- Check the App Service logs for errors

### Geocoding errors
- The Nominatim service may have rate limits
- Try adding a state to improve accuracy
- Check for typos in the city name

## License

MIT License