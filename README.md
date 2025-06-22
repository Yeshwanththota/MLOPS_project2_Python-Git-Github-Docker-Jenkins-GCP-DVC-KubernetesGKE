
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)
![GCP](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![DVC](https://img.shields.io/badge/DVC-945DD6?style=for-the-badge&logo=dvc&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)

**Summary:** A full MLOps workflow on Google Cloud Platform, starting with data storage in GCP buckets and progressing through environment setup, data ingestion, and processing. The project integrates experiment tracking with Comet ML, data versioning using DVC connected to cloud storage, and code versioning with Git and GitHub. A user-facing Flask web app is developed for predictions, and the entire pipeline is automated and deployed using Docker, Jenkins, and Kubernetes, resulting in a scalable, production-ready machine learning application on GKE.

**Go to MLops2_project_results for outputs**


Step  1
1.	Come to GCP console
2.	Create a bucket (untick enforce).
3.	Upload the data (.csv files to bucket)

Step 2
Project setup
1.	Creating virtual Environment in project folder.
2.	Creating required folders and files. (artifacts for outputs, config for path configurations and yaml files, pipeline folder, src where main project code lies, (static , templates for html,css,js and flask automatically finds them in project directory), utils for common functions, requirements and setup file. To make a folder a package we need to create a __init__.py file inside it so that the methods/files can be accessed from other places.
3.	Next, we code for setup, custom exceptions, logger, requirements files (basic things at first like numpy, pandas) .
4.	Then we run setup.py in venv in cmd using pip install -e . This will install all the required dependencies for the project make the project directory ready for next steps. This step automatically created a folder with project name given in the setup.py
   
Step 3
Data Ingestion
1.	Create data_ingestion.py in src. Then install google cloud cli from web and check in the venv with gcloud –version to know whether it is installed or not.
2.	Add google-cloud-storage to requirements. And run pip install -e .
3.	Now go to gcp – IAM & Admin -service accounts- create one (give the name, and permissions (storage object viewer,  storage Admin, owner) and done. Go to actions (tripe dots). Add keys-new key-and download json file.
4.	Now we want to give permissions to service account to access buckets. So go to buckets – tripe dots- edit access- add principle-select service account and assign the roles as before (except owner) and save.
5.	Now go to json file and copy path, open vscode and paste in some where then remove the “”. Now in terminal venv set GOOGLE_APPLICATION_CREDENTIAL= PASTE.
6.	Now we set google application credentials to our environment. So now we got the access to service account and from this account to access data in bucket.
7.	Create a config.yaml file in config and write configuration for accessing our buckets. Then add pyyaml in requirements and run pip install -e .
8.	Create common_function.py in utils and code it to read config.yaml.
9.	Now in config.yaml we write the data_ingestion code like the bucket name and file names inside it.
10.	Next create paths_config.py to write the data ingestions paths. Like raw_dir for artifacts and config path to read yaml file.
11.	Now come to data ingestion file and code. Write the imports and then code for getting data from cloud bucket to local (vscode).
12.	 Then in terminal run the cmd python src/data_ingestion.py
13.	 Now you should see the files under artifacts.
14.	Note: if using pwsh need use different cmd $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account-file.json"
But for cmd prompt it is like
Set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-file.json

Step 4
1.	Jupiter notebook testing
2.	Data ingestion code
3.	Data processing code
4.	Base model code
5.	Model training code
6.	Now go to web and search for comet ml. register an account (better to go with github account). Login and create a project. Then go to profile and copy the API key. Now come to model training file ,import it on top of all and then in code set the experiment variable with apikey, workspace name and project name. now write the required code for comet-ml in the same file for experiment tracking.
7.	Run the model training file, you will see the experiment logged in comet-ml UI under workspace-experiments where you can track all the info about the model.
8.	Now creating a training_pipeline file and code it and run.

Step 5

Data versioning using DVC and code using github

What we did initially is data in bucket to PC.

Now we create another bucket (as before, give permissions to service account) to push all the artifacts to it. Now come to vscode and in requirements add dvc and install using pip install -e .

Now initialize the git and also dvc. You will see a dvc directory created automatically.

Next create a .gitignore and put the directory that you don’t want to push. Usually env, artifacts, checkpoints, data, and other mlruns etc. typically large files because git wont support and not a good practise.

1.	Now create a github repo and push the code from vscode. 
2.	Now in terminal add the artifacts to dvc using dvc add artifacts/raw like that for all other artifacts whichever required.
3.	We want github to track dvc files but not normal artifacts file.
4.	We check the status of dvc by dvc status (it should show data and pipeline are up to date).
5.	So we push this dvc files to git hub.
6.	Time to connect out new bucket to dvc
7.	Now go to requirements and add dvc-gs (here gs is google storage)
8.	And run the pip install -e .
9.	Now in terminal dvc remote add -d myremote gs://my_dvc_bucket11/ 
10.	This will connect dvc to gcp bucket.
11.	Now push to bucket using dvc push.
12.	If you get some bucket access error, then try setting "C:\Users\yashw\Downloads\lofty-voyage-461011-f1-412fe972f7d3.json" again and then push.
13.	So, it’s done now
14.	Let’s say we deleted a data file in vs code and we want it back then we just use dvc pull cmd and it will get the files from bucket. This is how it can be used.
15.	Now we create helper functions in helper.py

STEP 6
USER APP building using flask and chatgpt
1.	Create a prediction_pipeline.py and code ,run and test.
2.	Now create a application.py at root. Then go to requirements then add the flask and run.
3.	Import the flask and prediction pipeline to application.py and code the app.
4.	Now create a index.html under templates and code it for UI.
5.	Also, at the bottom of index.html file we write jinja template code which will help display flask results to website.
6.	Now run python application.py
7.	You will get a url to application where you can input userID and get the recommendations.
8.	Now we will add css to it. Create a style.css under static and code it. Save it.
9.	Run again the application.
10.	Done

STEP 7
CI/CD using Docker, Jenkins and Kubernetes. (Follow CI/CD Material)
1.	Open Docker application and let it run in background.
2.	In vs code create a custom_jenkins folder and Dockerfile in it. Code it to download the docker files and certifications. (Code can be found in (CI/CD Material from project folder.)
3.	Now go inside custom_jenkins and run the cmds one by one
a.	docker build -t jenkins-dind . 
b.	docker images
c.	Follow the steps in Material until docker restart.
4.	Now we want to integrate Jenkins with github. Go to github-settings(top right)-devloper settings- personal access tokens- tokens(classic)-create new token(classic)- give name- give permissions(repo,admin:repo_hook)-generate token- copy it- go to Jenkins – manage tokens- credentials-system-global-give the details-username(github top right)-pwd(paste the token)-give some ID and description- create.
5.	Now come to dashboard – item – give name-choose pipeline-then under configuration choose “pipeline script from SCM”)-select Git under SCM – go to github repository and under code -copy the https url-paste it under repository url in Jenkins-select the credentials “our token” – choose the brain if it’s main- then click apply - Save.
6.	Now we have our pipeline visible on dashboard. Go inside this and to pipeline syntax. Select “checkout” thing from the sample step-paste the url-then credentials- main-click generate pipeline script- save the script.
7.	Now create a Jenkinsfile in root in vscode. And code it.
8.	While coding we paste the script in the Jenkinsfile somewhere.
9.	Now let’s push the changes into github. Open a new terminal so that you are outside of custom_jenkins while pushing the changes to github. Now use  add, commit and push.
10.	Now go to Jenkins and build now. See the console output and it should integrate github into it (Jenkins) and will show success message at the end in output.
11.	Jenkin and github are integrated now.
12.	Now create another Dockerfile in root and paste some code (to cloning from Github) from material.
13.	Now come to Jenkins dashboard – Manage Jenkins – Credentials – global- add credentials – choose secret file- upload service account json file – give some id-description -create.
14.	Now you can access GCP also from Jenkins.
15.	 Come back to Jenkins file and code for Setting up our Virtual Environment and Installing dependencies. 
16.	Next, we code for DVC pull. And push the changes to github. Should give the credentialsId that we created in Jenkins (secret key). Then build the pipeline again in Jenkins and it should run successfully.
17.	Now come to the terminal (custom_exceptions) and install google cloud and Kubernetes cli on Jenkins container. You can do this from the material. Run one by one.
18.	Then exit the bash. Restart Jenkins using cmd.
19.	Now set the required enivormental variables in jenkinsfile and write code for pushing the docker images to GCR.
20.	Then give docker permissions to Jenkins user (from material).
21.	Now come to GCP – API – enable Artifact registry API , Kubernetes Engine API and google container Registry API.
22.	 Now come to home page – Kubernetes engine -clusters -create- cluster basics-fleet registration – networking (enable the “access using DNS”)-advanced settings- review and create.
23.	Now come to vscode. Create a deployment.yaml in root and paste the code from material. Save
24.	Now in Jenkins we code for “Deploying to GKE”.
25.	Now push the changes to git.
26.	When cluster is successfully created in GCP.
27.	Now go to the Jenkins. Build the pipeline now.
28.	If SUCCESS. Now we need to check what happened.
29.	Go to GCR in gcp. You will see your project. Which means building and pushing was successful.
30.	Now go to GKE. Go to cluster – workloads – YOUR ml app
31.	At the end of the Page, you will see the link to live app.
32.	Now clean up.
