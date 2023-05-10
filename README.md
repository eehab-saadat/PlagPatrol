# PlagPatrol - The Ultimate Plagirism Checker
The ultimate responsive web-based plaigirism checker which generates PDF plaigirism analysis reports. This was created as an end-of-semester project. 

## Installation & Setup
1. [Install python](https://www.python.org/downloads/), if you haven't already.
2. Download either the [Github Command Line Interface (CLI)]() or the [Github Desktop]() app, if you prefer a more visual apporach. You will be needing the either of these tools much often as will be seen ahead.
3. Once done, clone this repository onto your local device. There are multiple ways to do this. You can install and use any of the [CLI](https://github.com/cli/cli#installation), [Desktop App](https://desktop.github.com/) or click the top-left greenish button to do so.
4. After having the repository cloned, open up a terminal and navigate (`cd`) to the cloned directory, such that you're within the directory. 
5. Now create a *virtual environment*, by running the following command (assuming you have a Windows device):
```
> py -3 -m venv venv
```
6. Virtual environments help bundle up dependencies and manage them more effectively and better. Before you work on your project, you need to activate the corresponding environment:
```
> .\venv\Scripts\activate
```
7. Now install all the required dependencies:
```
> pip install -r requirements.txt
```
8. Now you're all setup to run the project. To run it, run the following set of commands:
```
> SET CONFIGURATION_SETUP="config.DevelopmentConfig"
> python app.py
```
9. The app would be up and running in debug mode now, which allows for hot reload during development, and can be accessed by clicking the link(s) being showed up on the terminal (e.g. http://127.0.0.1:5000).
10. Kill the app by closing the terminal or by interrupting the process by pressing <kbd>CTRL</kbd> + <kbd>C</kbd> once you're done.

Feel free to contact me in case of any queries.

## Project Structuring
### static
This directory holds all the static assets such as all the css, javascript and image files related to the project. 
### templates
This directory holds all the HTML files and templates related to the project and is further segregated into two sub-directories: `main` and `errors` for holding children templates, for mainstream usage and error pages respectively, which inherit and extend from the parent templates, such as `index.html`, to render views to the frontend.
### utils
This directory holds all relevant packaged functionality to be utilized in the core `app.py` file where the application instance lies in. The `__init__.py` helps python recognize this as a python package and to be used as module for common utility.
### tmp
This directory holds all the temporary files, i.e. where the user-uploaded file is downloaded to and from where the generated PDF report is sent from. This directory only acts as a temporary file buffer zone and remains ideally empty. The `placeholder.txt` exists only to facilitate git tracking for the folder.

## Collaboration
We use Github to collaborate and maintain an effective workflow. This section provides easy-to-follow instructions for our team to work collaboratively and keep our work synced across the team by using Github.

As was mentioned earlier, you'll be using either the Github Desktop app or the Github CLI to follow through the following content. It's recommended to use the CLI as it easens redundant tasks and navigation but feel free to use whatever works with you.

[Here](https://uoftcoders.github.io/studyGroup/lessons/git/collaboration/lesson/)'s a good guide to get started with the CLI and for the App refer to [here](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop). Be sure to read [this](https://www.freecodecamp.org/news/how-to-use-git-and-github-in-a-team-like-a-pro/) and [this](https://medium.com/@jonathanmines/the-ultimate-github-collaboration-guide-df816e98fb67), along with the aforementioned gudes, before following through, to help stuff make sense.

### Issues
Issues are used to track todos, bugs, feature requests, and more. As issues are created, they’ll appear in the `Issues` section as a searchable and filterable list. Each issue has a label indicating its nature and can be assigned to the dedicated resource, who closes the issue once it's resolved.

### Branch, Commit & Push
There are multiple ways to do this so be sure to read the aforementioned guides before following along. Be sure to see the following section on pull requests before starting to work as well.

Once you're working on an issue, create a branch for it using a suitable and appropriate naming convention, such as `add-ocr-support`, `add-web-scraper`, `add-frontend`, `add-pdf-gen` and etc. 

Now, on your local device, switch to that branch, as mentioned in your relevant guide, and **commit** to it as you make progress through your feature(s). Be sure to include appropriate messages with the commit such as *"added ocr support to detect handwriting and the utility to parse input documents"*. 

> **Note:** Remember to **ALWAYS** branch from the main branch, to keep up with updated code and to **NOT** work on the same file or place as others to avoid a crucial merge conflict.

### Pull Requests
Finally when you're done with your feature, submit a **pull request** (click [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) for more info) for your branch to be merged with the **main branch**, which is the trunk branch for stable, production-ready and deployable code. Be sure to include relevant name and description for this telling about what it's for and what issue it fixes such as *"Adds OCR support and file parsing, fixes #3"* where the `#3` indicates that it fixes the Issue with the ID of 3. 

### Code Reviews & Merge
The submitted pull request would then be submitted for code review to be done by the project administrator or merge master ([@eehab-saadat](https://github.com/eehab-saadat)) and merged with the main branch if no merge conflicts or problems are found. Relevant feedback would be provided via comments otherwise.

Once the pull request is approved and merged with the main, the submitted branch would then be deleted by the merge master, after which you can start working on a new feature by just repeating through the aforementioned. That's it!

You can see the demo [here](https://medium.com/@jonathanmines/the-ultimate-github-collaboration-guide-df816e98fb67) for further info and illustration.

## Code Standards
Every collarborator is advised to write well indented and documented code. This includes writing explanatory code comments and docstrings for every function and class defined. Be sure to write efficient and concise code with meaningful names and type hints where possible. You can view the already submitted code for reference. A vscode extension was used to auto-generate docstrings in google formate, hence providing automation.

This would not only improve the code's readability and understandability but also improve the code's maintainibility and malleability. 

## Contact & Suggestions
Feel free to contact me in case of any queries or suggestions.
