```
---
title: Org Clarifai
emoji: 🏃
colorFrom: yellow
colorTo: red
sdk: streamlit
sdk_version: 1.26.0
app_file: src/streamlit_app.py
pinned: false
---
```
# https-streamlit.io-community-llm-hackathon-2023

## Hackathon

Presenting an interesting concept of agent based streamlit interactions and could have various applications, especially for tasks involving data processing, automation, and collaboration. 

## Goal

Be able to do the following

* Use large language models apis interactivly via clarifai or indirectly via git/yaml api.
* User approve api calls and interactions using rules and manual work. 
* Consume quickly read in git or pastes as inputs and load them as datasets.
* Communicate with other bots via directories and logs and clarifai.
* Convert directories and text to protobufs to yaml to api calls and back.
* Improve itself via improvement process that uses this system.

## Architecture

We are describing a system where each "agent" or component operates within a directory-based environment. Each agent reads and processes instructions from files, interacts with the directory structure, and can create new files or data as needed. The agents can communicate with each other through a shared Git repository hosted by a Streamlit server. The can also share the same data via clarifai and yaml log files.

This approach allows for distributed and collaborative processing of tasks within the directory structure. Agents follow instructions provided in specific files, and these instructions guide their actions and interactions with the data and other agents.

## Security

The application has mutliple deployments, one per role and each role can have a different set of credentials, either user and clarifai api key.


## User interactives

* List Applications/List datasets
* List unclassified inputs and assign them to datasets
* Create prompt models from inputs (assign to dataset of prompt models)
* Define new rules and macros interactivly from inputs(assign to set of rule datasets)
* Define new dialogs interactivly from protobuf or yaml(assign to dialog datasets)
* Execute metaprograms defined in workspace(interpret inputs with prompt models to create effects)

* Be able to load them from wiki or git or from datasets or inputs(resolve urls, assign to dataaset of urls and have them injested)
* Read this file or any other markdown file, select it as a dataaset. (choose between docuements we have, list datasets)
* Dataset of git repos, objects files/versions, commits, python objects (details of git implementation as own datasets)
* Have a command line like repl (eval loop using emoji language to call code)
* Define new emojis and find them (introspect objects from python to emoji)
* Be able to clone public git repos into workspace via urls(url as git repo dataset to injest)
