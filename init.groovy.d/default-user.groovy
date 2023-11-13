import jenkins.model.*
import hudson.security.*
import org.jenkinsci.plugins.matrixauth.AuthorizationMatrixNodeProperty
import org.jenkinsci.plugins.matrixauth.Authority

def env = System.getenv()

def jenkins = Jenkins.getInstance()
def hudsonRealm = new HudsonPrivateSecurityRealm(false)

hudsonRealm.createAccount(env.JENKINS_USER, env.JENKINS_PASS)
jenkins.setSecurityRealm(hudsonRealm)
strategy.add(Jenkins.ADMINISTER, env.JENKINS_USER)
jenkins.setAuthorizationStrategy(strategy)

jenkins.save()
