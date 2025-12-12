import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.local_project_dir = os.getenv("LOCAL_PROJECT_PATH")
        self.local_jar_name = os.getenv("LOCAL_JAR_NAME")
        self.local_java_home = os.getenv("LOCAL_JAVA_HOME")
        self.remote_host = os.getenv("REMOTE_HOST")
        self.remote_port = int(os.getenv("REMOTE_PORT", "22"))
        self.remote_user = os.getenv("REMOTE_USER")
        self.remote_pass = os.getenv("REMOTE_PASS")
        self.remote_path = os.getenv("REMOTE_PATH")
        self.remote_log_file = os.getenv("REMOTE_LOG_FILE")
        self.mvn_cmd = os.path.normpath(os.getenv("MVN_CMD"))
        self.maven_settings = os.path.normpath(os.getenv("MAVEN_SETTINGS"))
        self.maven_repo = os.path.normpath(os.getenv("MAVEN_REPO"))
        self.java_exec = os.getenv("JAVA_EXEC", "java")
        self.jps_exec = os.getenv("JPS_EXEC", "jps")

        self.validate()

    def validate(self):
        missings = []
        for attr in [
            "local_project_dir", "local_jar_name", "remote_host", "remote_port",
            "remote_user", "remote_pass", "remote_path", "remote_log_file",
            "mvn_cmd", "maven_settings", "maven_repo"
        ]:
            if getattr(self, attr) in [None, ""]:
                missings.append(attr)
        if missings:
            raise ValueError(f"缺少必要配置项：{', '.join(missings)}")

    def get_local_target_jar(self):
        import os
        return os.path.join(self.local_project_dir, "target", self.local_jar_name)

    def get_remote_jar_path(self):
        return f"{self.remote_path}/{self.local_jar_name}"