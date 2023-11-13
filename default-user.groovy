import jenkins.model.*
import hudson.security.*

def env = System.getenv()

def jenkins = Jenkins.getInstance()
def hudsonRealm = new HudsonPrivateSecurityRealm(false)

hudsonRealm.createAccount(env.JENKINS_USER, env.JENKINS_PASS)
jenkins.setSecurityRealm(hudsonRealm)
jenkins.setAuthorizationStrategy(new GlobalMatrixAuthorizationStrategy())

jenkins.save()
