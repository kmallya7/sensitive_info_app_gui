import os

def set_env_variables():
    user = 'kmallya7'
    password = 'Udumalpet@7'
    account = 'hfgwbta-cf08090'
    warehouse = 'COMPUTE_WH'
    database = 'ABCINC'
    schema = 'ABCINC.PUBLIC'
    role = 'ACCOUNTADMIN'

    os.environ['SNOWSQL_USER'] = user
    os.environ['SNOWSQL_PWD'] = password
    os.environ['ACCOUNT'] = account
    os.environ['WAREHOUSE'] = warehouse
    os.environ['DATABASE'] = database
    os.environ['SCHEMA'] = schema
    os.environ['ROLE'] = role

    print("Environment variables set successfully.")

if __name__ == "__main__":
    set_env_variables()
