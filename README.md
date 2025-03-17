# DuckBot V1: Your Personalized AI Assistant

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)

## Overview

DuckBot V1 is a user-friendly desktop application that leverages the power of various Artificial Intelligence models, including Google Gemini, OpenAI's models (like `gpt-3.5-turbo-instruct`), and the potential for integration with local models like LLaMA and Hugging Face Transformers. Built with a graphical user interface (GUI) using PySide6, DuckBot V1 provides a centralized and enhanced way to interact with AI, offering features and flexibility beyond simply using the standard Gemini API or web interface.

**This project aims to provide a more personalized and integrated AI experience by:**

* Offering a dedicated desktop interface for AI interactions.
* Enabling the use of multiple AI models within a single application.
* Allowing for the extension of AI capabilities through custom modules.
* Integrating AI with local system functionalities.

## Key Differences and Advantages Over Regular Gemini

While Google Gemini is a powerful and versatile Large Language Model, DuckBot V1 offers several distinct advantages and features that go beyond the standard Gemini API or web interface:

**1. Unified Interface for Multiple AI Models:**

* **DuckBot V1:** Provides a single GUI to interact with Google Gemini, OpenAI models, and potentially locally run models like LLaMA and those from Hugging Face. You can easily switch between different AI "participants" using a dropdown menu.
* **Regular Gemini:** Typically accessed through its specific API or Google's Bard interface, without native integration with other AI models.

**2. Extensibility Through Custom Modules:**

* **DuckBot V1:** Features a modular design that allows you to load custom AI functions from the `modules` directory. This means you can extend the application's capabilities with specialized AI tasks or integrations tailored to your needs.
* **Regular Gemini:** Offers a fixed set of functionalities through its API, with limited options for user-defined extensions within the standard usage.

**3. Integration with Local System Functionality:**

* **DuckBot V1:** Includes the ability to execute local system commands directly from the chat interface (e.g., opening notepad, listing files). This bridges the gap between AI interaction and your local operating system.
* **Regular Gemini:** Operates primarily within its own context and does not have direct access to your local file system or the ability to execute system commands.

**4. Enhanced User Experience with a Dedicated GUI:**

* **DuckBot V1:** Offers a user-friendly graphical interface with features like:
    * Clear chat history display.
    * Separate output display for AI "thought process" or system command results.
    * Easy selection of different AI models.
    * Buttons for clearing history and copying output.
    * Persistence of the last selected AI model.
* **Regular Gemini:** Primarily interacted with through code via its API or a web-based interface like Bard, which may not offer the same level of customization or integration with local workflows.

**5. Potential for Local AI Model Usage:**

* **DuckBot V1:** Is designed to potentially integrate with locally run AI models (like LLaMA or those loaded via Hugging Face Transformers) if you have the necessary hardware and setup. This allows for AI processing without relying solely on external APIs.
* **Regular Gemini:** Primarily functions as a cloud-based service. Running a full instance of Gemini locally is not typically feasible for most users.

**6. Customization and Personalization:**

* **DuckBot V1:** Being an open-source project, you have the freedom to modify and customize the application to fit your specific requirements and preferences.
* **Regular Gemini:** Offers limited customization options beyond the parameters available in its API.

**In essence, DuckBot V1 acts as a powerful and flexible client that brings together various AI capabilities into a single, user-controlled application, offering a more integrated and personalized experience compared to interacting with Gemini in isolation.**

## Uses of DuckBot V1

DuckBot V1 can be used for a wide range of tasks, including:

* **General Question Answering:** Leveraging the knowledge of Gemini and other integrated models.
* **Creative Writing and Content Generation:** Utilizing the text generation capabilities of the AI participants.
* **Code Generation and Assistance:** Depending on the capabilities of the selected AI model.
* **Brainstorming and Idea Generation:** Interacting with AI to explore different perspectives.
* **Task Automation (Basic):** Using system commands to perform simple local tasks.
* **Learning and Research:** Quickly accessing information and explanations from various AI sources.
* **Experimenting with Different AI Models:** Comparing the responses and capabilities of Gemini, OpenAI, and local models.
* **Building Custom AI Workflows:** By creating and loading specialized AI functions through modules.

## Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone [repository URL]
    cd DuckBot V1
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Keys:**
    * Create a `.env` file in the root directory of the project.
    * Add your API keys for Google Gemini and OpenAI (if you intend to use those features):
        ```dotenv
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
        LLAMA_API_KEY="YOUR_LLAMA_API_KEY" # Optional
        ```
        **Important:** Replace `"YOUR_GEMINI_API_KEY"` and `"YOUR_OPENAI_API_KEY"` with your actual API keys.

4.  **Run the Application:**
    ```bash
    python run_all_windows.py
    ```

## Contributing

Contributions to DuckBot V1 are welcome! If you have ideas for new features, bug fixes, or improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgements

* Google for the Gemini API.
* OpenAI for their language models.
* The developers of PySide6 for the GUI framework.
* The Hugging Face team for the `transformers` library.
* The `python-dotenv` library for managing environment variables.
