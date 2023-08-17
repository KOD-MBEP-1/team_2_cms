# Why?
Example project for scaffolding a python + postgresql project

# Important links:
[Repo](https://github.com/KOD-MBEP-1/team_2_cms)
[Board](https://github.com/orgs/KOD-MBEP-1/projects/1/views/2)
[Brainstorming](https://excalidraw.com/#room=8a50ee05e2de9b83e81b,EMOOTXL9t4sAqB1HWbvirA)

# System requirements:

- Python 3.10.12
- Postgresql 14.8

# Get started

1. Check your python version
`````bash
python3 -V
`````

2. Initialize your virtual environment
`````bash
python3 -m venv .venv
`````

3. Allow executable permissions to the current user
````bash
chmod -R +rwx .
````

4. Activate virtual environment and install required pip dependencies
`````bash
./start_dev.sh
`````

5. Init your psql server
   
6. Create a new .env file with the variables in .env.example
   
7. Code like your life depends on it

# Dev process: 
1. Run `./start_dev.sh` to:
   1. Activate virtual environment
   2. Install/update dependencies if necessary
2. Code


# Feature development process: 
1. Create a new branch with the following syntax: `YOUR-NAME_NAME-OF-THE-FEATURE--#ISSUE-NUMBER`. EG: `juan_create-articles--#5`
2. Code
3. When you finilized the feature merge your code to master branch on local
4. Test
5. [Create a PR](https://github.com/KOD-MBEP-1/team_2_cms/pulls)


# New dependencies
1. Run `./install.sh NAME_OF_YOUR_DEPENDENCY` to save the new dependency into the requirements file. EG: `./install.sh ipython`
   - You can also run `pip install NAME_OF_YOUR_DEPENDENCY` and then run `./freeze.sh`
