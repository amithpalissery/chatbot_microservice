# README: Kubernetes-Native Chatbot Microservice 

This repository contains a full-stack chatbot application built with three microservices, all designed to run on a Kubernetes cluster. The application leverages best practices in cloud-native development, including microservices architecture, containerization, and automated deployment with Helm.

-----

### Application Architecture and Workflow

The application is composed of three services that work together to provide a seamless chatbot experience:

  * **`frontend`**: A web-based user interface that handles user input and displays chatbot responses.
  * **`ai-service`**: The core of the application. It receives user queries from the frontend, communicates with the `chat-history-service` to retrieve past context, and uses an external Gemini API to generate a response.
  * **`chat-history-service`**: A simple database service that stores and retrieves a user's conversation history to provide context to the AI.

The flow of communication is **bidirectional**: `Frontend <-> AI Service <-> Chat History Service`.

-----

### Cloud-Native Best Practices

This project incorporates several best practices for building robust and scalable applications in a Kubernetes environment:

1.  **Microservices Architecture**: The application is broken down into small, independent services. This makes development, deployment, and scaling of each component easier and more efficient.
2.  **Containerization**: Each service is packaged in its own Docker container, ensuring a consistent and portable environment across development and production.
3.  **Infrastructure as Code (IaC)**: The entire application is deployed using a single **Helm chart**. This allows you to define, install, and upgrade all Kubernetes resources (Deployments, Services, etc.) in a predictable and repeatable way.
4.  **Automatic Scaling**: The `ai-service` uses a **Horizontal Pod Autoscaler (HPA)** to automatically scale the number of pods based on CPU utilization. This ensures the application can handle fluctuating user loads efficiently.
5.  **Secure Communication**: **Network Policies** are implemented to act as a firewall for the pods. These policies restrict traffic to only what is necessary for the application to function, preventing unauthorized access and securing the inter-service communication.
6.  **Centralized Logging**: All services use standard output for logging. Kubernetes automatically collects these logs, making it easy to monitor and debug the application from a central location using `kubectl logs`.

-----

### Deployment

To deploy the application to your Kubernetes cluster, follow these steps:

1.  **Configure Your Cluster**: Ensure you have a running Kubernetes cluster and your `kubectl` context is set correctly. The cluster must have an Ingress Controller (like NGINX Ingress) and a CNI plugin that supports Network Policies (like Weave Net).
2.  **Install Helm**: Follow the official Helm documentation to install Helm on your machine.
3.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```
4.  **Update Dependencies**: The `ai-service` uses a Gemini API key. Ensure this key is configured as a Kubernetes secret named `gemini-api-key`.
    ```bash
    kubectl create secret generic gemini-api-key --from-literal=API_KEY='your_api_key_here'
    ```
5.  **Deploy the Application**: Use the `helm upgrade --install` command to deploy the application. This command will create or update all the necessary Kubernetes resources, including the Deployments, Services, HPA, and Network Policies.
    ```bash
    helm upgrade --install chatbot-release ./chatbot-microservice-chart
    ```
6.  **Access the Application**: Once the pods are running, find the external IP address of your Ingress Controller to access the frontend.

-----

### Troubleshooting Common Issues

  * **`504 Gateway Timeout`**: This is usually a Network Policy issue. The Ingress Controller is unable to reach the frontend service. The fix is to ensure your `frontend-network-policy.yaml` correctly identifies the namespace of your Ingress Controller (often `default` or `ingress-nginx`).
  * **No Response from AI Service**: This typically indicates that the AI service's outbound traffic is being blocked. Check the logs for DNS lookup failures or connection timeouts. The fix is to ensure your `ai-service-network-policy.yaml` has the correct `egress` rules to allow traffic to CoreDNS and the external internet.
  * **`500 Internal Server Error`**: This is an application-level error. Use `kubectl logs` to check the `ai-service` logs for detailed error messages, such as authentication failures with the Gemini API or a problem communicating with the chat history service.
