################################################## EUDR_MTP ##################################################
Riskevaluation-Software for EUDR Compliance in Deforestation Regulation
Master Team Project FSS 2024.
https://www.uni-mannheim.de/en/ines/teaching/european-master-team-project/projekt-riskevaluation-software-for-eudr-compliance-in-deforestation-regulation/
Supervisor: Felix Köhler (Osapiens)
Students: Tomas Muça, Jusztina Judak, Siddharth Prakash Pai (University of Mannheim- Germany)
          Boloş Darius Ionut, Petru Adelin Cojocaru, Szilard Farkas (Babeș-Bolyai University- Cluj, Romania)

# Introduction


# Architecture
We used a PostgreSQL version 16 (will not work for older versions) for the project because it supports the Insert or Update on conflict command. 
The database is hosted on the University of Mannheim server: inestp03@dws-student-01.informatik.uni-mannheim.de
The installation is done via conda. Firstly, connect to University of Mannheim VPN if you are not using the University internet and login to the aforementioned cluster. Create/Activate eudr_conda environment and see the postgres database present there. You can execute postgres related commands to view the database and tables.
Installing PostgreSQL version 16: https://gist.github.com/gwangjinkim/f13bf596fefa7db7d31c22efd1627c7a
To make the database accessible outside the cluster, we made some configuration changes.
    1. /home/inestp03/mylocal_db/postgresql.conf: edited the following `listen_addressed = "*"` and `port = 5432`
    2. /home/inestp03/mylocal_db/pg_hba.conf: added a line `host all all 0.0.0.0/0 trust`
Restarted the server using `pg_ctl -D mylocal_db -l logfile restart` command.
Now, the database should be accessible from any DB application (pgAdmin 4) if you connect using the parameters found in the Training/credentials.properties.
Sometimes, if the database is not used for a long time, it hibernates. In such situations, you need to restart the database server: `pg_ctl -D mylocal_db -l logfile restart`. This will re-run the database and activate it.

The risk score calculation was done via Python and in some cases, we also used the OpenAI LLM API. We designed the frontend UI using ReactJS and the backend using the Spring module.

# Code Documentation
The code base is structured such that the folders and filenames are self explanatory as well as the tree structure of directories making any file easily accessible. We have 5 main directories which run the respective files:
A] Database:
This directory stores all SQL files which constitute the table struture and some also explaining the rows stored within the tables. The following tables are present in the database:
    1. commodities.sql: stores the 7 commodity names and its respective IDs. No need for any further updates.
    2. commodity_risks.sql: stores commodity based risk scores per country. Gets updated and inserted via training modules.
    3. country_standard_dimension.sql: stores official country names and their 2 character ISO codes. No need for any further updates.
    4. customers.sql: stores the customer details which are entered via UI as well as the overall risk score.
    5. publiceye_inserts.sql: contains and insert statements manually run for this particular dataset. No need for any further updates.
    6. risk_categories.sql: stores all 11 category names, its IDs and weightage required for calculations. No need for any further updates.
    7. risk_sources.sql: stores all risk source names per category, the respective IDs and the confidence scores of the source. Whenever a new source is ingested into database, create a new INSERT statement in this file and run it manually in the database query tool.
    8. risks.sql: stores the country-wise risk score per source per category. Gets updated and inserted via training modules.

B] Datasets:
As the name suggests, this directory maintains all the data sources downloaded from the internet. These sources are fetched from this directory for processing and calculating category and/or commodity specific risk score. If any new source is used for risk score calculation, that file needs to be saved in this directory.

C] FrontEnd:
The UI of the project is designed using ReactJS. This directory holds all the code files required to build the User-Interface, which currently runs on the local server as localhost:3000.

D] Java:
The backend of the project is implemented using Springboot modules. This directory stores all backend related code files. Please open this directory via IntelliJ for easier navigation.

E] Training:
This directory stores all python files which process the data files within the Datasets/ directory. Each file is names such that the reader can find out the source, category and/or the commodity being processed in it.
    1. credentials.properties: a file which stores all the environment variables used by the training modules at any time in the code. Please edit the parameters according to your local PC settings wherever needed.
    2. country_standard.py: a common file imported in all training modules, which returns the 2 character ISO codes for the country name being sent as a prompt to the LLM.
    3. database_operations.py: a common file imported in all training modules, which performs table insertions via Python.

# Execution Steps
In order to execute this project on your local laptop, perform the following steps:
    1. Clone the repository.
    2. Edit the Training/credentials.properties file parameters, especially the OpenAI API key.
    3. Connect to the University of Mannheim server.
    4. Open the FrontEnd/ directory in VSCode; Java/ directory via IntelliJ.
    5. Execute "npm run dev" in the terminal of FrontEnd/ in VSCode.
    6. Click on "Run" button for the Java/demo/src/main/java/com/example/demo/DemoApplication.java in IntelliJ.
    7. Open a new browser window and go to localhost:3000 link which will take you to the Supplier Registration page.
    8. The project is up and running on your local system now.

In order to stop the project:
    1. Press Ctrl+D in VSCode terminal to stop the FrontEnd execution.
    2. Click the "Stop" button in IntelliJ to gracefully stop the backend.
    3. Refreshing the browser window should show a Not Reachable error for the localhost:3000 link.