import json
import matplotlib.pyplot as plt

with open("assets/vmaf.json") as f:
    result = json.load(f)
  
plt.figure(figsize=(10, 5))  
frames = result['frames']
keys = frames[0]['metrics'].keys()
x = [frame['frameNum'] for frame in frames]
y = [[frame['metrics'][key] for frame in frames] for key in keys]

for i, key in enumerate(keys):
    plt.plot(x, y[i], label=key)
    
plt.title("vmaf evaluation")
plt.legend(keys, bbox_to_anchor=(0.85, 1), loc=2, borderaxespad=0)
        
# show and save
plt.show()
plt.savefig('assets/vmaf.png')