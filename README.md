# Fill the Form

The project aims at creating an automated tool to fill web forms with valid input values by inferring the feedback from the website. The feedback can be in the form of error messages, placeholder and other other different attributes of the different input elements. Existing systems navigate webformz by filling arbitrary values into the input values and come to an halt on being faced with an input validation or an alert box from the system. The proposed system will infer the message from the error messages/ alert box to generate valid input for that particular input field.

## Workflow
![System Workflow](project_artifacts/"SystemDesign.png "System Workflow")


## Setting up the environment
#### Pre-requisites
#### Setting Codebase and running Application
Open a terminal and clone the repository by using the following command:
```sh
https://github.com/ajithnair20/fill-the-form.git
```
Traverse to the root directory of the project in a terminal window and execute the below commands:
```sh
$ python.exe --url <url of the web form>
```
