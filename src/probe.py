import docker
import os
import time
import http.client
import urllib.parse
from threading import Thread
import argparse
import yaml

class MonitorHandler:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def save(self, amf_id, percentage):
        print('Saving: amf[' +str(amf_id)+'] percentage['+str(percentage)+']', flush=True)
        conn = http.client.HTTPConnection(self.host, self.port)
        params = urllib.parse.urlencode({'cpu_usage': percentage})
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        conn.request('POST','/entry/' + amf_id, params, headers)


class MonitoringThread(Thread):
    def __init__ (self, monitor:MonitorHandler, container):
        print('New Thread for AMF', container.labels['amf'], flush=True)
        Thread.__init__(self)
        self.container = container
        self.monitor = monitor

    def run(self):
        amf_id = self.container.labels['amf']
        last_stats = None
        while (True) :
            start_time = int(time.time())
            stats = self.container.stats(stream=False)
            if last_stats != None:
                percentage = self.calculate_cpu_percentage(last_stats['cpu_stats'], stats['cpu_stats'])
                print(amf_id, 'percentage: ' + str(percentage), flush=True)
                self.monitor.save(amf_id, percentage)
            last_stats = stats

            end_time = int(time.time())
            execution_time = end_time-start_time
            sleep_time = int(os.environ['MONITOR_INTERVAL']) - execution_time

            if sleep_time > 0:
                time.sleep(sleep_time)

    def calculate_cpu_percentage(self, previous_stats, current_stats):
        cpuPercent = 0.0
        cpu_delta = current_stats['cpu_usage']['total_usage'] - previous_stats['cpu_usage']['total_usage']
        print('CPU_DELTA', cpu_delta, flush=True)
        system_delta = current_stats.get('system_cpu_usage', 0) - previous_stats.get('system_cpu_usage',0)
        if system_delta > 0.0 and cpu_delta > 0.0 :
            cpuPercent = (cpu_delta / system_delta) * len(current_stats['cpu_usage']['percpu_usage']) * 100.0
        return cpuPercent



class DockerCommunicationHandler:
    def __init__ (self, docker_config):
        docker_remotely = docker_config['remotely']

        if docker_remotely:
            self.client = docker.DockerClient(docker_config['url'])
        else:
            self.client = docker.from_env()

    def get_containers(self):
        container_filter = {'label': 'amf'}
        return self.client.containers.list(filters=container_filter)

class Probe:
    def __init__(self, config):
        self.containers_ids = []

        docker_config = config.get('docker', {'remotely': False})
        self.docker_handler = DockerCommunicationHandler(docker_config)

        monitor_config = config.get('monitor', {'host': 'localhost', 'port': 5000, 'interval': 2})

        self.monitor = MonitorHandler(monitor_config['host'], monitor_config['port'])

        self.monitor_interval = monitor_config['interval']

    def run(self):
        while (True) :
            print('Serching new containers...', flush=True)
            current_containers = self.docker_handler.get_containers()

            for container in current_containers:
                if container.id not in self.containers_ids:
                    print('New container added', container.id, container.labels['amf'], flush=True)
                    self.containers_ids.append(container.id)
                    thread = MonitoringThread(self.monitor, container)
                    thread.start()
            time.sleep(self.monitor_interval)

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Elastic5GC Probe')
    parser.add_argument('--config', help="Configuration File")
    args = parser.parse_args()
    yml_file = open(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', args.config)))
    config = yaml.load(yml_file, Loader=yaml.CLoader)

    probe = Probe(config)
    probe.run()

