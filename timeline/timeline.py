import matplotlib.pyplot as plt
import math
import random

class Line:
    def __init__(self, type, start, end, seq, drop):
        self.type = type
        self.start = start
        self.end = end
        self.seq = seq
        self.drop = drop
    
    def __eq__(self, other):
        if isinstance(other, Line):
            return self.type == other.type and self.start == other.start and self.end == other.end and self.seq == other.seq and self.drop == other.drop
        return False

def gen_question():
    rtt = random.choice([4,6,8])
    bw = random.choice([0.5,1])
    to = random.choice([rtt+1, rtt+2])
    drop_seq = random.randint(1,4)
    drop_type = random.choice([1,2])
    return [rtt, bw, to, drop_seq, drop_type]


def gen_answer_lines(question):
    rtt = question[0]
    t = 1/question[1]
    to = question[2]
    drop_seq = question[3]
    drop_type = question[4]
    lines = []
    n = 0
    for i in range(drop_seq-1):
        start = t*i + 1
        end = start + rtt/2
        line1 = Line("Data", start, end, i+1, False)
        line2 = Line("ACK", end, end +rtt/2, i+1, False)
        lines.append(line1)
        lines.append(line2)
        n = i+1
    start = t*n + 1
    end = start + rtt/2
    if drop_type == 1:
        dropline = Line("Data", start, end, n+1, True)
        lines.append(dropline)
    else:
        line3 = Line("Data", start, end, n+1, False)
        dropline = Line("ACK", end, end+rtt/2, n+1, True)
        lines.append(line3)
        lines.append(dropline)
    for i in range(drop_seq-1, 4):
        start = t*i + 1 + to
        end = start + rtt/2
        line1 = Line("Data", start, end, i+1, False)
        line2 = Line("ACK", end, end +rtt/2, i+1, False)
        lines.append(line1)
        lines.append(line2)

    i = 0
    j = 0
    for l in lines:
        if l.drop:
            j = i + 1
            break
        i += 1
    s = lines[j].start
    e = lines[j].end
    return lines


def draw_graph(lines):

    # draw background
    nodes = {"Sender": 0, "Receiver": 10}
    plt.clf()
    plt.axvline(0)
    plt.axvline(10)
    plt.xlim((0, 1))
    # for line in lines:

    ymin = 0
    for line in lines:
        y1 = line.start
        y2 = line.end
        ymin = int(min([-y1, -y2, ymin]))
        if line.type == 'Data':
            x1 = 0
            x2 = 10
        else:
            x1 = 10
            x2 = 0
        plt.plot([x1, x2], [-y1, -y2], "b")

        if line.drop:
            plt.annotate("X", [x2, -y2], ha="center", va="center", color="b")


        height = y1 - y2
        width = abs(x1 - x2)
        angle = math.degrees(math.atan(height/width))
        align = "left"
        offset = 1.5
        if (x1 > x2):
            angle = -angle
            align = "right"
            offset = -offset
        plt.annotate(line.type + str(line.seq), [x1 + offset, -y1+0.5], ha=align, rotation=angle, va="top")

    ymin = -25
    plt.ylim((ymin, 0))
    plt.yticks(range(ymin, 1), labels=range(-ymin, -1, -1))
    plt.xticks(list(nodes.values()), labels=nodes.keys())
    plt.grid(axis='y')
    plt.gcf().set_figwidth(2 * (len(nodes) - 1))
    plt.gcf().set_figheight(-ymin/5)
    plt.savefig("correct_timeline.jpg", bbox_inches='tight')
    

def compare(input_lines, answer_lines):
    if len(input_lines) != len(answer_lines):
        return False
    for i in range(len(input_lines)):
        if input_lines[i] != answer_lines[i]:
            return False
    return True
