import docker
import os
import time
import http.client
import urllib.parse

def calculate_cpu_percentage(previous_stats, current_stats):
    cpuPercent = 0.0
    cpu_delta = current_stats['cpu_usage']['total_usage'] - previous_stats['cpu_usage']['total_usage']
    system_delta = current_stats['system_cpu_usage'] - previous_stats['system_cpu_usage']
    if system_delta > 0.0 and cpu_delta > 0.0 :
        cpuPercent = (cpu_delta / system_delta) * len(current_stats['cpu_usage']['percpu_usage']) * 100.0
    return cpuPercent

def save(amf_id, percentage):
    conn = http.client.HTTPConnection(os.environ['MONITOR_HOST'], os.environ['MONITOR_PORT'])
    params = urllib.parse.urlencode({'cpu_usage': percentage})
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn.request('POST','/entry/' + amf_id, params, headers)



if __name__ == "__main__":
    print("Starting probe", flush=True)
    client = docker.DockerClient(base_url=os.environ['DOCKER_URL'])
    last_cpu_stats = {}
    label = 'amf'

    while (True) :
        print("Getting...", flush=True)
        container_filter = {'label': label}
        current_containers = client.containers.list(filters=container_filter)
        for container in current_containers:
            amf_id = container.labels[label]
            cpu_stats = container.stats(stream=False)['cpu_stats']
            if container.id in last_cpu_stats:
                percentage = calculate_cpu_percentage(last_cpu_stats[container.id], cpu_stats)
                save(amf_id, percentage)

            last_cpu_stats[container.id] = cpu_stats
        time.sleep(int(os.environ['VERIFICATION_PERIOD']))

