import subprocess
import os

def is_docker_available():
    try:
        subprocess.run(['docker', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def wait_for_elasticsearch():
    subprocess.check_output(["bash", "-c", "until curl -s -o /dev/null http://localhost:9200; do sleep 3; done"])

    
def start():
    curr_path= os.getcwd()
    es_dir= os.path.join(curr_path, "./elastic-dir")
    pid_file="./es-pid"
    no_docker=False
    if not is_docker_available() or no_docker:
        print("Docker is not available. Trying to start elasticsearch locally.")
        subprocess.run([
                f"/usr/bin/elasticsearch",
                "-Ediscovery.type=single-node",
                "-Eindices.query.bool.max_clause_count=16438",
                "-d",
                "-p", pid_file
                ], check=True)
    else:
        subprocess.run(["docker", "rm", "-f", "inc-rel-es"], check=True)
        print("Trying to start elasticsearch in docker.")
        subprocess.run([
                "docker", "run", "-d",
                "--name", "inc-rel-es",
                "-p", "9200:9200",
                "-e", 'discovery.type=single-node',
                "-e", "xpack.security.enabled=false",
                "-d", "elasticsearch:8.10.2"
                ], check=True)
        wait_for_elasticsearch()