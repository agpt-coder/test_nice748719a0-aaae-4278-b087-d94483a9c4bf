---
date: 2024-04-22T22:24:33.033807
author: AutoGPT <info@agpt.co>
---

# test_nice

a project that allows users to write B2B and B2C cold emails utilizing AI. In the program use LiteLLM so I can call multiple models like gpt-4-turbo and another model for checking output of gpt-4-turbo

**Features**

- **AI Writing Interface** This feature allows users to input their requirements for cold emails and utilizes models like gpt-4-turbo to generate drafts.

- **Model Selection Option** Users can choose between different AI models, such as gpt-4-turbo or others, to see which best fits their needs.

- **Quality Check Module** A secondary AI model checks the output of the primary AI writing tool to ensure accuracy and adherence to best practices in email marketing.

- **Template Library** Provides a variety of pre-designed templates for different B2B and B2C scenarios.

- **Editing and Customization Tools** These tools allow users to fine-tune AI-generated drafts before finalizing them.

- **Performance Analytics** Tracks and reports on the effectiveness of the sent emails, analyzing metrics like open rates and conversion rates.


## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'test_nice'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
