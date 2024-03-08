import matplotlib.pyplot as plt

from box_luck_example import run_box_hits
from time import time




num_runs =10000
num_box_hits=2367
bin_size =1

target_gun_array=[]
i=0
t0=time()
while i< num_runs:
    count_dict=run_box_hits(num_box_hits)
    target_gun_array.append(count_dict["tgun"])
    
    i+=1
    print(i)
    # if i % 1000==0:
    #     t1=time()
    #     multiple=num_runs/1000
    #     minutes=multiple*(t1-t0)/60
    #     print(minutes)
    
# Calculate the bin edges
min_value = min(target_gun_array)
max_value = max(target_gun_array)
num_bins = int((max_value - min_value) / bin_size) + 1
bin_edges = [min_value + i * bin_size for i in range(num_bins)]

sorted_array=sorted(target_gun_array)

# index=sorted_array.index(143)
# print(f"Out of {num_runs} games, games worse: {index}\n, games better: {len(target_gun_array)-index}")

# Create histogram
plt.hist(target_gun_array, bins=bin_edges ,color='skyblue', edgecolor='black')

# Add labels and title
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram of Sample Data')

# Show plot
plt.show()