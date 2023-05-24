import json
import matplotlib.pyplot as plt
import configargparse

parser = configargparse.ArgParser()
parser.add_argument('-i', '--input', default='assets/vmaf.json')
args = parser.parse_args()

with open(args.input, "r") as f:
    result = json.load(f)
  
plt.figure(figsize=(10, 5))  
frames = result['frames']
keys = frames[0]['metrics'].keys()
x = [frame['frameNum'] for frame in frames]
y = [[frame['metrics'][key] for frame in frames] for key in keys]

for i, key in enumerate(keys):
    plt.plot(x, y[i], label=key)
    
plt.title("vmaf evaluation")
plt.xlabel("Frame")
plt.ylabel("Metrics")
plt.legend(keys, bbox_to_anchor=(0.85, 1), loc=2, borderaxespad=0)
        
# show and save
output_name = args.input.split("/")[-1].split(".")[0]
plt.show()
plt.savefig(f'assets/vmaf_{output_name}.png')