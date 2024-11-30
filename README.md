# 💳 Credit Card Analyzer

An innovative solution for credit card analysis and validation using Azure AI

## Contents

- [Overview](#overview)
- [Technologies](#technologies)
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [Features](#features)
- [Future Development](#future-development)

## Overview

Credit Card Analyzer is a modern web application that streamlines credit card validation for e-commerce platforms. Using Azure's advanced AI capabilities, the system extracts and validates credit card information from images, providing a seamless and efficient experience.

## Technologies

### Core Stack

- Python 3.12+
- Streamlit 1.39.0+
- Azure Document Intelligence
- Azure Blob Storage
- SQLite

### Key Libraries

- `azure-ai-documentintelligence`: Document analysis
- `azure-storage-blob`: Image storage
- `pandas`: Data manipulation
- `python-dotenv`: Environment variable management

## Requirements

- Python 3.12 or higher
- Azure account with access to:
  - Azure Document Intelligence
  - Azure Blob Storage
- Docker (optional)

## Setup and Installation

### Local Development

1. Clone repository:
```bash
git clone https://github.com/gabriela-bezerra/Credit-Card-Analyzer.git
```

2. Navigate to repository:
```bash
cd Credit-Card-Analyzer
```

3. Install Poetry (if needed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

4. Setup virtual environment:
```bash
poetry install --without dev
```

5. Activate virtual environment:
```bash
poetry shell
```

6. Configure environment:
```bash
cp .env.example .env
```

7. Update `.env` with credentials:
```
AZURE_DOC_INT_ENDPOINT=your_doc_intelligence_endpoint
AZURE_DOC_INT_KEY=your_doc_intelligence_key
AZURE_STORAGE_CONNECTION=your_storage_connection_string
CONTAINER_NAME=your_container_name
DATABASE_PATH=../data/credit_cards.db
```

8. Navigate to project directory:
```bash
cd desafios_de_projeto/desafio_2/src
```

9. Launch application:
```bash
streamlit run app.py
```

10. Visit: http://localhost:8501

### Docker Deployment

1. Navigate to Dockerfile directory:
```bash
cd desafios_de_projeto/desafio_2
```

2. Build and run:
```bash
docker-compose up --build
```

3. Visit: http://localhost:8501

4. Stop service:
```bash
docker-compose down
```

## Features

### Card Analysis
- Card image upload
- Automated data extraction
- Card validation
- Database storage

### Data Management
- Custom filtering
- CSV export
- Detailed visualization

### User Experience
- Responsive design
- Visual feedback
- Streamlined navigation

## Future Development

- GDPR-compliant data protection implementation
- Enhanced validation (expiration date verification, etc.)
- Multilingual support
- Advanced analytics dashboard
- REST API for integrations