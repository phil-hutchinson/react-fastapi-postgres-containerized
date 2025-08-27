You are helping a user set up a new project from the react-fastapi-postgres-containerized template repository. Follow these steps in order:

1. **Get project information**: Get initial information from the user
    - Ask the user for the name/purpose of their new project. Use this to create a short prefix (e.g., "todo-app", "inventory-system"). Convert spaces to hyphens and ensure lowercase.
    - Ask a user for a new port number to use for the nginx port.

2. **Update docker-compose.yml**: Add `container_name` properties to all services using the prefix:
   - backend service: `{prefix}-backend`
   - frontend service: `{prefix}-frontend` 
   - database service: `{prefix}-database`
   - nginx service: `{prefix}-nginx`

3. **Update nginx port** in docker-compose.yml to avoid potential conflicts, update nginx port:
   - Nginx external port (currently 1111) → update to nginx-port provided by user.
   - Other references to port 1111 in docker-compose.yml → update to nginx-port provided by user.
   
4. **Update network name** in docker-compose-migrate.yml using the prefix. This appears in 2 locations in the file.

5. **Guide stack startup**: Provide commands to:
   - Bring up main stack: `docker-compose up -d`
   - Run migrations: `docker-compose -f docker-compose-migrate.yml up`
   - Check status: `docker-compose ps`

6. **Suggest testing**: Direct user to navigate to `localhost:{nginx-port}` and test basic app functionality.

Execute each step sequentially, showing the actual file changes needed and waiting for user confirmation before proceeding to the next step.