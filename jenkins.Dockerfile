FROM jenkins/jenkins:lts

# Switch to root to install additional tools
USER root



# Install necessary tools, e.g., git, Docker CLI
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common \
    git \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# add password and username for jenkins with the init.groovy.d scripts
COPY set-admin-password.groovy /usr/share/jenkins/ref/init.groovy.d/set-admin-password.groovy

# Copy the plugins list
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

# Install the listed plugins
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt

# add password and username for jenkins with the init.groovy.d scripts
COPY default-user.groovy /usr/share/jenkins/ref/init.groovy.d/

# Switch back to Jenkins user
USER jenkins