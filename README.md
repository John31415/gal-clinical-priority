# gal-clinical-priority

LLM-based simulation for clinical case prioritization under limited resources, inspired by Hospital Gustavo Aldereguía Lima, Cienfuegos, Cuba.

## Overview

This project simulates the prioritization of clinical cases under constrained hospital resources. Patients are modeled with clinical attributes, the hospital is modeled with limited capacity and consumable resources, and the system evaluates different admission policies through simulation.

The project combines:

* discrete-event simulation,
* stochastic health evolution,
* heuristic and metaheuristic prioritization policies,
* synthetic dataset generation,
* and LLM-assisted clinical text generation and extraction.

## Repository Structure

All source code lives inside `src/`.

```text
src/
├── algorithms/              # Simulated Annealing implementation
├── dataset_generation/      # Synthetic patient dataset generation pipeline
├── distributions/           # Probability distributions: normal, gamma, uniform, exponential, etc.
├── domain/                  # Core domain entities: patient, hospital, resource, requirements
├── dynamics/                # Health evolution and resource consumption dynamics
├── experiments/             # Experiment runners and comparisons
├── generators/              # Scenario generation and patient loading from JSON
├── llm/                     # Cloudflare Workers AI integration and prompts
├── metrics/                 # Evaluation metrics and solution scoring
├── policies/                # Admission and prioritization policies
├── simulation/              # Discrete-event simulation engine
├── utils/                   # Shared helpers and utilities
└── main.py                  # Main entry point
```

At the same level as `src/`, the repository also contains:

```text
README.md
docs/
dataset/
```

* `docs/` contains the technical report.
* `dataset/` contains the generated patient dataset and other data artifacts.

## Requirements

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

It is strongly recommended to do this inside a virtual environment.

## Creating and Activating a Virtual Environment

From the project root:

```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your shell should show `(venv)` or a similar prefix.

## Running the Project

Run the main experiment from the project root with:

```bash
python3 -m src.main
```

This command executes a full simulation experiment using the currently configured scenario and policies.

Example:

```bash
(venv) john314@DESKTOP-8EJNRPS:~/Documents/gal-clinical-priority$ python3 -m src.main
```

Depending on the current configuration, this will run an experiment with a randomized or predefined scenario and print the results for each policy.

## Generating the Patient Dataset

The patient dataset is generated through the script:

```text
src/dataset_generation/patient_dataset_generator.py
```

Inside that file, there is a line commented out at the bottom:

```python
# dataset_patient_generator()
```

To generate the dataset, uncomment that line and run the module directly:

```bash
python3 -m src.dataset_generation.patient_dataset_generator
```

This will create the synthetic patient dataset in the configured JSON output file.

### What the generator does

The dataset generation pipeline works in three stages:

1. A basic synthetic patient is generated using controlled randomness.
2. A diagnosis narrative is produced by the LLM from the basic patient data.
3. The narrative is parsed again by the LLM to extract structured patient attributes.

The final output is a JSON dataset containing patients with:

* identifier,
* age,
* clinical diagnosis text,
* health level,
* deterioration rate,
* improvement rate,
* and drug information.

## LLM Configuration

This project uses Cloudflare Workers AI. To run the LLM functions, you need to configure your Cloudflare API credentials.

### 1. Get Your Credentials

#### Cloudflare Account ID (`CF_ID`)

1. Log in to your [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Select your account or account home.
3. On the right-hand sidebar (or near the bottom of the page), look for the **Account ID** section.
4. Copy the string of characters.

#### Cloudflare API Token (`CF_TOKEN`)

1. In the top-right corner of the Cloudflare Dashboard, click your **User Profile icon** and select **My Profile**.
2. Go to **API Tokens** from the left menu.
3. Click **Create Token**.
4. Scroll down to **Custom Token** and click **Get Started**.
5. Set up the token with the following settings:

   * **Token name:** `Workers AI Access` (or any preferred name)
   * **Permissions:** Select `Account` | `Workers AI` | `Edit`
6. Click **Continue to summary**, then click **Create Token**.
7. Copy the generated token immediately (it will not be shown again).

### 2. Set Environment Variables

Export the credentials in your shell before running the project:

```bash
export CF_ID="your_cloudflare_account_id"
export CF_TOKEN="your_cloudflare_api_token"
```

You can also store them in a `.env` file if your local setup supports it.

### 3. Model Used

The current LLM configuration uses Cloudflare Workers AI with the model:

```text
@cf/meta/llama-3.1-8b-instruct
```

This model is used for:

* expanding basic patient information into a clinical narrative,
* extracting structured attributes from the narrative,
* and supporting the generation pipeline used to build the dataset.

## Main Components

### `domain`

Contains the core entities of the problem, such as patients, hospitals, and resources.

### `dynamics`

Implements the evolution of health status and the progressive consumption of resources.

### `simulation`

Provides the event-driven simulation engine, including arrival handling, queue management, admission, and patient evolution.

### `policies`

Defines the prioritization strategies used to reorder patients before admission.

### `algorithms`

Contains optimization algorithms such as Simulated Annealing.

### `metrics`

Computes the final evaluation metrics, including lives saved and total suffering.

### `generators`

Builds scenarios and loads patients from generated JSON datasets.

### `dataset_generation`

Creates the synthetic clinical dataset using randomness and LLM-based expansion.

### `llm`

Wraps the Cloudflare Workers AI integration, prompts, and parsing logic.

### `distributions`

Provides probability distributions used by the simulator and dataset generators.

### `experiments`

Contains experiment runners and comparison scripts.

### `utils`

Shared helper functions and reusable utilities.

## Expected Output

The system evaluates multiple policies over the same scenario and reports:

* number of patients,
* lives saved,
* deaths,
* minimum health sum,
* simulation time,
* and execution time.

For a given scenario, the best policy is selected according to the project’s objective criteria.
