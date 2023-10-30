import numpy as np
import matplotlib.pyplot as plt
import sys

PLOT_SAMPLES = 300
files = ["logs/a3c.txt","logs/sac.txt","logs/ppo.txt"]
colors = ["blue","red","green"]
linear = []
log = []
hd = []
bit = []
buffer = []
rebuffer = []

# fig, (ax1, ax2, ax3, ax4,ax5,ax6) = plt.subplots(6, sharex=True)
fig, (ax1,ax4,ax5,ax6) = plt.subplots(4, sharex=True)


for index in range(0,3):
    file = sys.argv[1] + files[index]
    color = colors[index]

    time_stamp = []
    bit_rates = []
    buffer_occupancies = []
    rebuffer_times = []
    linear_rewards = []
    log_rewards = []
    hd_rewards = []
    with open(file, 'r') as f:
        flag = 1
        for line in f:
            if flag:
                flag = 0
                continue
            if line.isspace():
                break
            
            parse = line.split()
            time_stamp.append(float(parse[0]))
            bit_rates.append(float(parse[1]))
            buffer_occupancies.append(float(parse[2]))
            rebuffer_times.append(float(parse[3]))
            linear_rewards.append(float(parse[6]))
            log_rewards.append(float(parse[7]))
            hd_rewards.append(float(parse[8]))

    time_stamp = [x - time_stamp[0] for x in time_stamp]
    linear.append(round(np.mean(linear_rewards[-PLOT_SAMPLES:]),5))
    log.append(round(np.mean([x for x in log_rewards[-PLOT_SAMPLES:] if x != float('-inf')]),5))
    hd.append(round(np.mean(hd_rewards[-PLOT_SAMPLES:]),5))
    bit.append(round(np.mean(bit_rates[-PLOT_SAMPLES:]),5))
    buffer.append(round(np.mean(buffer_occupancies[-PLOT_SAMPLES:]),5))
    rebuffer.append(round(np.mean(rebuffer_times[-PLOT_SAMPLES:]),5))

    ax1.plot(time_stamp[-PLOT_SAMPLES:], linear_rewards[-PLOT_SAMPLES:] , color=color)
    ax1.set_ylabel('Linear Reward')

    # ax2.plot(time_stamp[-PLOT_SAMPLES:], log_rewards[-PLOT_SAMPLES:], color=color)
    # ax2.set_ylabel('Log Reward')

    # ax3.plot(time_stamp[-PLOT_SAMPLES:], hd_rewards[-PLOT_SAMPLES:] , color=color)
    # ax3.set_ylabel('HD Reward')

    ax4.plot(time_stamp[-PLOT_SAMPLES:], bit_rates[-PLOT_SAMPLES:] , color=color)
    ax4.set_ylabel('bit rate (Kpbs)')

    ax5.plot(time_stamp[-PLOT_SAMPLES:], buffer_occupancies[-PLOT_SAMPLES:] , color=color)
    ax5.set_ylabel('buffer occupancy (sec)')

    ax6.plot(time_stamp[-PLOT_SAMPLES:], rebuffer_times[-PLOT_SAMPLES:] , color=color)
    ax6.set_ylabel('rebuffer time (sec)')
    # ax6.yaxis.set_label_coords(-0.04,0)

    ax6.set_xlabel('Time (sec)')


ax1.set_title('Average linear reward: ' + str(linear[0]) + "," + str(linear[1]) + "," + str(linear[2]))
# ax2.set_title('Average log reward: ' + str(log[0]) + "," + str(log[1]) + "," + str(log[2]))
# ax3.set_title('Average hd reward: ' + str(hd[0]) + "," + str(hd[1]) + "," + str(hd[2]))
ax4.set_title('Average bitrate: ' + str(bit[0]) + "," + str(bit[1]) + "," + str(bit[2]))
ax5.set_title('Average buffer occupancy: ' + str(buffer[0]) + "," + str(buffer[1]) + "," + str(buffer[2]))
ax6.set_title('Average rebuffer time: ' + str(rebuffer[0]) + "," + str(rebuffer[1]) + "," + str(rebuffer[2]))

fig.suptitle("Averages are in order A3C(Blue) , SAC(Red) , PPO(Green)")
fig.subplots_adjust(hspace=0.5)
plt.savefig(sys.argv[1] + 'plot.png')
plt.close()