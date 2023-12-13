
# ai-personal-assistant

ai-personal-assistant is an Azure FunctionApp integrating OpenAI libraries, designed to automate tasks and offer AI-driven solutions. This project harnesses the power of AI to streamline processes and enhance functionality in various applications.

## Documentation

The "ai-personal-assistant" project is an innovative solution that combines Azure Function Apps with OpenAI's advanced capabilities and Azure Cosmos DB's MongoDB API. This infrastructure is uniquely designed to develop a chatbot that utilizes emails from Outlook as its data source. The project is focused on creating a personalized, intelligent chatbot that can interact seamlessly, drawing its knowledge base directly from the user's email interactions.

## Getting Started

### Prerequisites

- Azure Python Function app.
- Azure OpenAI account
- Azure Cosmos DB for MongoDB
- Python 3.9 or higher.

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
    - OPENAI_API_KEY
    - OPENAI_API_TYPE
    - OPENAI_API_BASE
    - OPENAI_API_VERSION
    - CosmosConnectionString

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
