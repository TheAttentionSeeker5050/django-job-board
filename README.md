# **Panda Jobs Job Board Website**

## **Description**

Panda Jobs is a comprehensive job board platform developed using Django, Django Templates, jQuery, and MySQL. It bridges job seekers and employers with features like job postings, applications, resume uploads, and user-friendly dashboards. Visit live demo of the site at: https://panda-jobs.nicolas-castellano.com 

## **Prerequisites**

- Docker and Docker Compose
- Node.js (for Tailwind CSS)

## **Setting Up the Project**

1. **Clone the Repository**
    
    Clone this repository to get started.
    
2. **Environment Variables**
    
    Copy the contents from **`templateEnv`** into **`.env`** or **`deploy.env`** depending on your environment. Adjust these files as needed for your specific configuration.
    
3. **Building Tailwind CSS Styles**
    
    Run **`npm run build-tailwind`** to compile the Tailwind CSS styles.
    
4. **Creating Users**
    - **Superuser**: Use **`DJANGO_SUPERUSER_USERNAME`**, **`DJANGO_SUPERUSER_EMAIL`**, and **`DJANGO_SUPERUSER_PASSWORD`** in the environment file to create a Django superuser.
    - **Dummy User**: Create a dummy user for demos. Set **`DUMMY_USER`** and **`DUMMY_PASSWORD`** in the environment file for the dummy login functionality. This user can be created via the Django admin console.
5. **Docker Compose**
    - **Development**: Run **`docker-compose -f docker-compose.yml up`** to start the development environment.
    - **Production**: Use **`docker-compose -f docker-deploy.yml up`** for production. Make necessary changes for Docker network configurations, domain settings, etc.
6. **Reverse Proxy Using Nginx**
    
    In production, Nginx serves as a reverse proxy. Configure this in **`nginx.Dockerfile`** and the Nginx configuration files.
    

## **Customizing for Production**

- Customize **`CSRF_TRUSTED_ORIGINS`** and **`ALLOWED_HOSTS`** in the environment files to match your domain when deploying.
- Modify Docker network settings and domain configurations in the Docker Compose files to fit your environment.
- Review and adjust the volume mappings and port settings in the Docker Compose files as needed.

## **Running the Application**

- **Development**: Visit **`localhost:8085`**.
- **Production**: Access the production server at **`localhost:82`**.

## **Additional Setup Details**

- The database service uses PostgreSQL on port 5434. Adjust **`POSTGRES_PORT`** as needed.
- Ensure **`DEBUG`** is **`False`** in production for security.
- Keep the **`SECRET_KEY`** secret and secure.
- Jenkins setup is optional for CI/CD.

## **Troubleshooting**

- Ensure all environment variables are set correctly.
- Verify Docker and Docker Compose installation.
- Check Docker Compose logs for startup errors.

## **Conclusion**

With these instructions, you can set up Panda Jobs for development and production. Be sure to customize the Docker configuration
