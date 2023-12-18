---
page_type: sample
languages: 
- python
products: 
- azure
- azure-sdks
- azure-functions
description: "Azure Function App integrating OpenAI libraries, designed to automate tasks and offer AI-driven solutions"
title: Using Azure Open AI for automations with Azure Functions
author: gavin-aguiar
urlFragment: azure-functions-python-use-open-ai
---

# Using Azure Open AI for automations with Azure Functions

ai-personal-assistant is an Azure Function App integrating OpenAI libraries, designed to automate tasks and offer AI-driven solutions. This project harnesses the power of AI to streamline processes and enhance functionality in various applications.

## Documentation

The "ai-personal-assistant" project is an innovative solution that combines Azure Function Apps with OpenAI's advanced capabilities and Azure Cosmos DB's MongoDB API. This infrastructure is uniquely designed to develop a chatbot that utilizes emails from Outlook as its data source. The project is focused on creating a personalized, intelligent chatbot that can interact seamlessly, drawing its knowledge base directly from the user's email interactions.

## Getting Started

### Prerequisites

- Azure Python Function app.
- Azure OpenAI account
- Azure Cosmos DB for MongoDB - vCore Config
- Python 3.9 or higher.
- Outlook Desktop App
- (For local development) Azure Storage emulator such as [Azurite](https://learn.microsoft.com/azure/storage/common/storage-use-azurite) running in the background

### Installation

1. Clone the repository:

    ``` bash
    git clone [repository-url]
    ```

1. Navigate to the project directory:

    ```bash
    cd functions_with_openai
    ```

1. Install the required dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

1. Add the following environment variables in local.settings.json
or as app settings in Azure Function App
    - OPENAI_API_KEY -  The API key for your Azure OpenAI resource; For Open AI refer [platform API Key](https://platform.openai.com/api-keys).
    - OPENAI_API_TYPE - set this to `azure` for azure API
    - OPENAI_API_BASE - The base URL for your Azure OpenAI resource.  You can find this in the Azure portal under your Azure OpenAI resource for Azure Open AI.
    - OPENAI_API_VERSION - The API version you want to use: set this to `2022-12-01` for the released version. Refer [this doc](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#embeddings) for latest released version for embeddings.
    - OPENAI_DEPLOYMENT_NAME - set this to deployment name for Azure Open AI and model name (`text-embedding-ada-002`) for Open AI API.
    - CosmosConnectionString - Connection String of Cosmos Database for Mongo DB (vCore)
    - DB_NAME - Database Name in Mongo DB
    - COLLECTION_NAME - Collection Name in the Mongo DB.

### Deployment

To run the function app locally
Run the following command

```bash
func host start
```

To deploy the FunctionApp to Azure:

Ensure you are logged into Azure CLI.
Run the following command:

``` bash
func azure functionapp publish [Your FunctionApp Name]
``````

## Resources

- [OpenAI Documentation](https://openai.com/api/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/)
- [Azure Cosmos DB for MongoDB](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/introduction)
