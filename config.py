import subprocess
from datetime import datetime
import logging
import re
import matplotlib.pyplot as plt
import argparse
import json
import os

# Load configuration from a JSON file
def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ping_address(department, address, ping_count, timeout):
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output = subprocess.run(['ping', '-n', str(ping_count), '-w', str(timeout * 1000), address],
                                capture_output=True, text=True, timeout=timeout * ping_count)
        if "Reply from" in output.stdout:
            rtt_match = re.search(r'Average = (\d+ms)', output.stdout)
            avg_rtt = rtt_match.group(1) if rtt_match else "N/A"
            logging.info(f"{current_time}: Ping to {department} at {address} successful.\n{output.stdout}")
            return True, output.stdout, current_time, avg_rtt
        else:
            logging.error(f"{current_time}: Ping to {department} at {address} failed.\n{output.stdout}")
            return False, output.stdout, current_time, "N/A"
    except subprocess.CalledProcessError as e:
        logging.error(f"{current_time}: Ping to {department} at {address} failed: {e}")
        return False, str(e), current_time, "N/A"
    except subprocess.TimeoutExpired:
        logging.error(f"{current_time}: Ping to {department} at {address} timed out.")
        return False, "Ping timed out", current_time, "N/A"
    except Exception as e:
        logging.error(f"{current_time}: An error occurred while pinging {department} at {address}: {e}")
        return False, str(e), current_time, "N/A"

def main(config_file, log_file, ping_count, timeout, save_graph):
    config = load_config(config_file)
    departments = config['departments']
    setup_logging(log_file)

    ping_results = {}
    for department, address in departments.items():
        success, output, ping_time, avg_rtt = ping_address(department, address, ping_count, timeout)
        ping_results[department] = {'success': success, 'output': output, 'time': ping_time, 'avg_rtt': avg_rtt}

    # Visualization
    fig, ax = plt.subplots()
    y_pos = range(len(departments))
    success_colors = ['green' if ping_results[dept]['success'] else 'red' for dept in departments]

    bars = ax.barh(y_pos, [1] * len(departments), color=success_colors)

    # Add department names, timestamps, and RTT inside the bars
    for i, dept in enumerate(departments):
        label = f"{dept}\n{ping_results[dept]['time']}\nAvg RTT: {ping_results[dept]['avg_rtt']}"
        ax.text(0.5, i, label, ha='center', va='center', color='white')

    ax.set_yticks(y_pos)
    ax.set_yticklabels([])  # Hide y-axis labels
    ax.set_xlabel('Ping Status')
    ax.set_title('Ping Results per Department')

    # Add legend
    success_patch = plt.Line2D([0], [0], color='green', lw=4, label='Successful')
    failed_patch = plt.Line2D([0], [0], color='red', lw=4, label='Failed')
    ax.legend(handles=[success_patch, failed_patch], loc='upper center')

    if save_graph:
        graph_file = f'ping_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(graph_file)
        logging.info(f"Graph saved to {graph_file}")

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ping multiple departments and display results.')
    parser.add_argument('--config', type=str, default='config.json', help='Path to configuration file')
    parser.add_argument('--log', type=str, default='ping.log', help='Path to log file')
    parser.add_argument('--count', type=int, default=4, help='Number of ping attempts per address')
    parser.add_argument('--timeout', type=int, default=5, help='Timeout for each ping attempt in seconds')
    parser.add_argument('--save', action='store_true', help='Save the graph as an image file')
    args = parser.parse_args()

    main(args.config, args.log, args.count, args.timeout, args.save)
