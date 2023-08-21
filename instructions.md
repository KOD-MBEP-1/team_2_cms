# Instructions for the CLI
1. Complete the get started instructions from `readme.md`
   1. Creating virtual environment
   2. Activate virtual environment
   3. Install dependencies
   4. Create .env file
   5. Initialize psql server
3.(At root level of this project) Run commands with the following syntax:

## Perform an action against one table
`python main.py NAME_OF_TABLE -a NAME_OF_ACTION ***INDIVIDUAL_ENTITY_OPTIONS`

EG 
````bash
 python main.py category -a update --category_id=2  --name=Duper --description="This is one in a zillion category"
````


### Where: 
#### NAME_OF_TABLE
Is one of the following
1. author
2. category
3. article

#### NAME_OF_ACTION
Is the specific action from the table

You can see the available options by running:

`python main.py NAME_OF_TABLE --help`

#### INDIVIDUAL_ENTITY_OPTIONS
Is the specific options from the table action you selected

You can see the available options by running:

`python main.py NAME_OF_TABLE --action --help` 

## Important:

- If the ``table_name`` inside your ``.env`` file doesn't exist, it'll be created on the fly
- If the table you select on your command execution options doesn't exist, it'll be created on the fly
- Some `INDIVIDUAL_ENTITY_OPTIONS` will not be considered if the action doesn't support it. EG: Adding primary_key in an INSERT/create operation
- The format of all the date fields is: YYYY-MM-DD