import time
import psutil
import GPUtil
from threading import Thread
from statistics import mean

running = True

def get_baseline_ram():
    ram_info = psutil.virtual_memory()
    return ram_info.used / (1024 ** 3)  # RAM in GB

def monitor_resources(interval=5, max_samples=100, output_file="resource_monitoring.txt"):
    cpu_frequencies = []
    memory_used = []
    used_rams = []

    baseline_ram = get_baseline_ram()

    cpu_count = psutil.cpu_count(logical=True)
    print(f"CPU Count: {cpu_count}")
    ram_info = psutil.virtual_memory()
    total_ram = ram_info.total / (1024 ** 3)
    print(f"Total RAM: {total_ram:.2f} GB")

    sample_count = 0

    try:
        while sample_count < max_samples and running:
            # CPU
            cpu_freq = psutil.cpu_freq().current
            cpu_frequencies.append(cpu_freq)

            # RAM information
            ram_info = psutil.virtual_memory()
            current_used_ram = ram_info.used / (1024 ** 3)
            additional_used_ram = current_used_ram - baseline_ram
            used_rams.append(additional_used_ram)

            # GPU information
            gpus = GPUtil.getGPUs()
            if gpus:
                memory_used_by_gpus = sum(gpu.memoryUsed for gpu in gpus)
                memory_used.append(memory_used_by_gpus)
            else:
                memory_used.append(0)

            sample_count += 1
            time.sleep(interval)

        # Write results to file
        with open(output_file, "w") as file:
            file.write("Summary of measurements:\n")
            file.write(f"Max CPU Frequency: {max(cpu_frequencies)} MHz\n")
            file.write(f"Average CPU Frequency: {mean(cpu_frequencies):.2f} MHz\n")
            file.write(f"Max Additional RAM Used: {max(used_rams):.2f} GB\n")
            file.write(f"Average Additional RAM Used: {mean(used_rams):.2f} GB\n")
            file.write(f"Max GPU Memory Used: {max(memory_used):.2f} MB\n")
            file.write(f"Average GPU Memory Used: {mean(memory_used):.2f} MB\n")

    except KeyboardInterrupt:
        print("Monitoring stopped by user")

def stop_monitoring():
    global running
    running = False

# Only to illustrate how to implement in your python script:
# Start the monitoring thread with the correct arguments
thread = Thread(target=monitor_resources, args=(5, 100, "my_resource_log.txt"))
thread.start()
# to stop measuring just paste the following line:
stop_monitoring()
