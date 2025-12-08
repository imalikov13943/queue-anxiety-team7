import random
import csv
import numpy as np

# Adding simulation configuration constants
NUM_EPISODES = 5000
MIN_QUEUES = 2
MAX_QUEUES = 6

MIN_CUSTOMERS = 1
MAX_CUSTOMERS = 12

SERVICE_MIN = 5
SERVICE_MAX = 25

# Adding delay probabilities and delay duration configuration
P_COUPON = 0.10
P_PRICE_CHECK = 0.05
P_RETURN_TO_SHELF = 0.03

# delay durations (seconds)
COUPON_DELAY = (5, 15)
PRICE_CHECK_DELAY = (20, 40)
RETURN_TO_SHELF_DELAY = (30, 60)

OUTPUT_FILE = "queue_dataset.csv"

# Implementing probabilistic delay generation
def generate_delay():
    r = random.random()
    if r < P_COUPON:
        return random.randint(*COUPON_DELAY)
    elif r < P_COUPON + P_PRICE_CHECK:
        return random.randint(*PRICE_CHECK_DELAY)
    elif r < P_COUPON + P_PRICE_CHECK + P_RETURN_TO_SHELF:
        return random.randint(*RETURN_TO_SHELF_DELAY)
    else:
        return 0


# Adding episode generation logic
def generate_episode():
    num_queues = random.randint(MIN_QUEUES, MAX_QUEUES)
    episode_data = []

    for q in range(num_queues):
        n_customers = random.randint(MIN_CUSTOMERS, MAX_CUSTOMERS)

        # Generate service and delay times for each customer in the queue
        service_times = np.random.randint(SERVICE_MIN, SERVICE_MAX+1, size=n_customers).tolist()
        delay_times = [generate_delay() for _ in range(n_customers)]

        # Compute actual waiting time including delays
        predicted_wait = sum(service_times)
        actual_wait = sum(service_times[i] + delay_times[i] for i in range(n_customers))

        # Added small noise to make the simulation more realistic
        actual_wait = max(actual_wait + np.random.uniform(-3, 5), 0)

        episode_data.append(
            (q, n_customers, service_times, delay_times, predicted_wait, actual_wait)
        )

    return episode_data

# Implemented CSV export for storing generated dataset
def save_dataset():
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "episode_id", "queue_id", "customers",
            "service_times", "delay_times",
            "predicted_wait", "actual_wait"
        ])
        # Loop through all episodes and write queue data to CSV file
        for ep in range(NUM_EPISODES):
            episode = generate_episode()
            for row in episode:
                writer.writerow([
                    ep,
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                ])

    print(f"Dataset saved to {OUTPUT_FILE}")

# Added script entry point to run dataset generation
if __name__ == "__main__":
    save_dataset()