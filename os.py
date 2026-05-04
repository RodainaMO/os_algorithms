import matplotlib.pyplot as plt

import numpy as np

# ==========================================
# 1. CPU SCHEDULING: ROUND ROBIN 

def round_robin_scheduling():
    print("\n-- CPU Scheduling: Round Robin --")
    try:
        n = int(input("Enter number of processes: "))
        tq = int(input("Enter Time Quantum: "))
        
        processes = []
        for i in range(n):
            print(f"Process {i+1}:")
            at = int(input("  Arrival Time: "))
            bt = int(input("  Burst Time: "))
            processes.append({'id': i+1, 'at': at, 'bt': bt, 'rem_bt': bt, 'ct': 0})

        processes.sort(key=lambda x: x['at'])
        time, completed = 0, 0
        ready_queue = []
        gantt_data = []

        print("\nStep-by-step execution:")
        
        while completed < n:
            for p in processes:
                if p['at'] <= time and p['rem_bt'] > 0 and p not in ready_queue:
                    ready_queue.append(p)
            
            if not ready_queue:
                time += 1
                continue
                
            curr = ready_queue.pop(0)
            exec_time = min(curr['rem_bt'], tq)

            print(f"Time {time} → P{curr['id']} runs for {exec_time}")

            gantt_data.append((f"P{curr['id']}", time, exec_time))
            
            time += exec_time
            curr['rem_bt'] -= exec_time
            
            for p in processes:
                if p['at'] <= time and p['rem_bt'] > 0 and p not in ready_queue and p != curr:
                    ready_queue.append(p)
            
            if curr['rem_bt'] > 0:
                ready_queue.append(curr)
            else:
                curr['ct'] = time
                completed += 1

        print("\nFinal Results:")
        total_wt = total_tat = 0

        for p in processes:
            tat = p['ct'] - p['at']
            wt = tat - p['bt']
            total_wt += wt
            total_tat += tat
            print(f"P{p['id']} -> CT={p['ct']} TAT={tat} WT={wt}")

        print(f"Average WT = {total_wt/n:.2f}")
        print(f"Average TAT = {total_tat/n:.2f}")

        # Plotting Gantt Chart
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Track all time points to create custom ticks
        all_times = [0]
        
        for pid, start, duration in gantt_data:
            end_time = start + duration
            all_times.append(end_time)
            
            # Use different colors for different processes to make it "pretty"
            color = 'tab:blue' if int(pid[1:]) % 2 == 0 else 'tab:orange'
            
            ax.broken_barh([(start, duration)], (10, 9), facecolors=color, edgecolor='black')
            ax.text(start + duration/2, 14.5, pid, ha='center', va='center', color='white', fontweight='bold')
        
        # Set ticks to the EXACT times where processes start/stop
        ax.set_xticks(list(set(all_times))) # Remove duplicates
        ax.set_xlabel('Time (Units)')
        ax.set_yticks([])
        ax.set_title('CPU Scheduling: Round Robin Gantt Chart')
        
        # Show vertical lines at every time transition
        plt.grid(True, axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

   

    except ValueError:
        print("Invalid input.")

# ==========================================
# First Fit 


def first_fit_memory():

    print("\n-- Memory Allocation: First Fit --")
    print("1. Dynamic (with splitting)")
    print("2. Static (no splitting)")
    
    mode = input("Choose mode: ")

    try:
        b_count = int(input("Enter number of memory blocks: "))
        blocks = []

        # Initialize blocks with IDs
        for i in range(b_count):
            size = int(input(f"Block {i+1} size: "))
            blocks.append({
                'id': f"B{i+1}",
                'size': size,
                'pid': None
            })

        p_count = int(input("Enter number of processes: "))

        print("\nStep-by-step allocation:")

        internal_frag = 0

        for i in range(p_count):
            p_size = int(input(f"Process {i+1} size: "))
            allocated = False

            for j in range(len(blocks)):
                if blocks[j]['pid'] is None and blocks[j]['size'] >= p_size:

                    print(f"P{i+1} allocated in {blocks[j]['id']} (size {blocks[j]['size']})")

                    # ======================
                    # DYNAMIC (SPLITTING)
                    # ======================
                    if mode == '1':
                        remaining = blocks[j]['size'] - p_size
                        original_id = blocks[j]['id']

                        # Assign process to first part
                        blocks[j] = {
                            'id': original_id + "A",
                            'size': p_size,
                            'pid': f"P{i+1}"
                        }

                        # Create remaining split block
                        if remaining > 0:
                            blocks.insert(j + 1, {
                                'id': original_id + "B",
                                'size': remaining,
                                'pid': None
                            })

                    # ======================
                    # STATIC (NO SPLITTING)
                    # ======================
                    elif mode == '2':
                        waste = blocks[j]['size'] - p_size
                        internal_frag += waste
                        blocks[j]['pid'] = f"P{i+1}"

                    allocated = True
                    break

            if not allocated:
                print(f"P{i+1} cannot be allocated")

        # ======================
        # FINAL OUTPUT
        # ======================
        print("\nFinal Memory Layout:")
        external_frag = 0

        for b in blocks:
            if b['pid']:
                print(f"{b['id']} -> {b['pid']} | Size = {b['size']}")
            else:
                print(f"{b['id']} -> Free | Size = {b['size']}")
                external_frag += b['size']

        print(f"\nTotal Internal Fragmentation = {internal_frag}")
        print(f"Total External Fragmentation = {external_frag}")

        # ======================
        # VISUALIZATION
        # ======================
        

        # Adjust figure size based on block count to prevent crowding
        fig_width = max(12, len(blocks) * 1.5)
        fig, ax = plt.subplots(figsize=(fig_width, 4))

        current_pos = 0
        for b in blocks:
            color = 'tab:red' if b['pid'] else 'tab:green'
            label = b['pid'] if b['pid'] else "FREE"
            
            # Draw the block as a horizontal rectangle
            ax.barh(0, b['size'], left=current_pos, color=color, edgecolor='black', height=0.5)
            
            # Place text in the middle of the block
            # Only show text if the block is wide enough to be readable
            if b['size'] > 0:
                ax.text(current_pos + b['size']/2, 0, f"{b['id']}\n({label})\n{b['size']}", 
                        ha='center', va='center', color='white', fontweight='bold', fontsize=9)
            
            current_pos += b['size']

        # Formatting
        title_mode = "Dynamic (Splitting)" if mode == '1' else "Static (No Splitting)"
        ax.set_title(f"Memory Layout: {title_mode}", fontsize=14, pad=20)
        ax.set_xlabel("Memory Address / Size")
        ax.set_yticks([]) # Hide Y axis as it's a single bar
        ax.set_xlim(0, current_pos) # Set limit to total memory size
        
        # Add a legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='tab:red', label='Allocated'),
                           Patch(facecolor='tab:green', label='Free')]
        ax.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()
        plt.show()

    except ValueError:
        print("Invalid input.")

# ==========================================
# 3. PAGE REPLACEMENT: LRU 

def lru_page_replacement():


    print("\n-- Page Replacement: LRU --")
    try:
        capacity = int(input("Enter number of frames: "))
        pages = list(map(int, input("Enter reference string: ").split()))
        
        frames = []
        history = []
        faults = 0
        hits = 0

        # store snapshots for visualization
        frame_states = []

        print("\nStep-by-step:")
        print("Page | Frames | Result")

        for page in pages:
            if page not in frames:
                if len(frames) < capacity:
                    frames.append(page)
                else:
                    lru = history.pop(0)
                    frames[frames.index(lru)] = page
                faults += 1
                result = "Fault"
            else:
                history.remove(page)
                hits += 1
                result = "Hit"

            history.append(page)

            # save snapshot
            frame_states.append(frames.copy())

            print(f"{page} -> {frames} -> {result}")

        print(f"\nTotal Faults = {faults}")
        print(f"Total Hits = {hits}")

        # =========================
        # PIE CHART (your original)
        # =========================
        plt.figure()
        plt.pie([faults, hits], labels=['Faults', 'Hits'], autopct='%1.1f%%')
        plt.title("LRU Performance")
        plt.show()

        # =========================
        # VISUAL FRAME EVOLUTION
        # =========================
        max_frames = capacity
        time_steps = len(frame_states)

        matrix = np.full((max_frames, time_steps), "", dtype=object)

        for t, state in enumerate(frame_states):
            for f in range(len(state)):
                matrix[f][t] = str(state[f])

        
        fig, ax = plt.subplots(figsize=(12, 5))
        
        # Create a background color array (0 for empty, 1 for fault, 2 for hit)
        color_map = np.zeros((capacity, len(pages)))
        
        # We need to track which steps were hits/faults for the colors
        is_hit = []
        frames_temp = []
        history_temp = []
        
        # Re-run a quick logical check just for the color grid
        for p in pages:
            if p in frames_temp:
                is_hit.append(True)
            else:
                is_hit.append(False)
                if len(frames_temp) < capacity:
                    frames_temp.append(p)
                else:
                    # Simple LRU logic for color mapping
                    lru = history_temp.pop(0)
                    frames_temp[frames_temp.index(lru)] = p
            if p in history_temp: history_temp.remove(p)
            history_temp.append(p)

        # Draw the grid
        for t, state in enumerate(frame_states):
            for f_idx in range(len(state)):
                # Color code: Light Red for Fault, Light Blue for Hit
                color = '#ffcccc' if not is_hit[t] else '#cce5ff'
                
                # Draw a rectangle for the frame
                rect = plt.Rectangle((t - 0.5, f_idx - 0.5), 1, 1, facecolor=color, edgecolor='black')
                ax.add_patch(rect)
                
                # Add the page number text
                ax.text(t, f_idx, str(state[f_idx]), ha='center', va='center', fontweight='bold')

        # Formatting the plot
        ax.set_xlim(-0.5, len(pages) - 0.5)
        ax.set_ylim(-0.5, capacity - 0.5)
        ax.set_xticks(range(len(pages)))
        ax.set_xticklabels(pages) # Show the reference string on X-axis
        ax.set_yticks(range(capacity))
        ax.set_yticklabels([f"Frame {i+1}" for i in range(capacity)])
        
        ax.set_title("LRU Step-by-Step Evolution (Red=Fault, Blue=Hit)")
        ax.set_xlabel("Page Reference String")
        ax.set_ylabel("Memory Frames")
        
        plt.gca().invert_yaxis() # Put Frame 1 at the top
        plt.show()

    except ValueError:
        print("Invalid input.")

# ==========================================
# MAIN

def main():
    while True:
        print("\n" + "="*30)
        print(" OS algorithms")
        print("="*30)
        print("1. CPU Scheduling (Round Robin)")
        print("2. Memory Allocation (First Fit)")
        print("3. Page Replacement (LRU)")
        print("4. Exit")
        choice = input("Select Option: ")
        
        if choice == '1': round_robin_scheduling()
        elif choice == '2': first_fit_memory()
        elif choice == '3': lru_page_replacement()
        elif choice == '4': break

if __name__ == "__main__":
    main()


