from helpers import get_locations, read_input

DAY = 15

locations = get_locations(f"day{DAY}")

content = read_input(locations.input_file)
inputs = content.split(",")


def hash(input: str) -> int:
    output = 0
    for c in input:
        output += ord(c)
        output *= 17
        output %= 256
    return output


# part 1

sum_inputs = sum([hash(input) for input in inputs])
print(f"Part 1 sum of hashes is: {sum_inputs}")


# Part 2
class Lens:
    def __init__(self, label: str, focal: int):
        self.label = label
        self.focal = focal

    def change_focal(self, newfocal: int):
        self.focal = newfocal


boxes: dict[int, list[Lens]] = {}

for input in inputs:
    if input.find("=") != -1:
        label, focalstr = input.split("=")
        box_num = hash(label)
        same_label = False
        if box_num in boxes:
            for lens in boxes[box_num]:
                if lens.label == label:
                    # If there is already a lens in the box with the same label
                    # remove the old lens and put the new lens in its place
                    lens.change_focal(int(focalstr))
                    same_label = True
                    break
            # if not a lens with same label
            # add the lens to the box immediately behind any lenses already in the box
            if same_label is False:
                boxes[box_num].append(Lens(label, int(focalstr)))
        else:
            # If there aren't any lenses in the box
            # the new lens goes all the way to the front of the box.
            boxes[box_num] = [Lens(label, int(focalstr))]

    else:
        box_num = hash(input.split("-")[0])
        label = input.split("-")[0]
        # go to the relevant box
        if box_num in boxes:
            # remove the lens with the given label if present
            new_box = list(filter(lambda lens: lens.label != label, boxes[box_num]))
            boxes[box_num] = new_box


def get_power(box_num, slot_num, focal_length):
    return (1 + box_num) * slot_num * focal_length


results = 0
for box_num in boxes.keys():
    for slot_num, lens in enumerate(boxes[box_num], 1):
        results += get_power(box_num, slot_num, lens.focal)

print(f"Part 2: sum of focusing powers is: {results}")
