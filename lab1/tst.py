import math


class Manipulator:
    def __init__(self, devices) -> None:
        self.devices = devices
        self.nose_coordinates = None
        self.length_1 = self.devices[1]['length']
        self.length_2 = self.devices[2]['length']
        self.angle_0 = None
        self.angle_1 = self.devices[1]['rotation_boundaries'][0]
        self.angle_2 = self.devices[2]['rotation_boundaries'][0]
        self.lever_1_end = None
        self.lever_2_end = None

    def forward_kinematic(self, angle_1, angle_2):
        x = self.length_1 * math.cos(angle_1) + self.length_2 * math.cos(angle_1 + angle_2)
        y = self.length_1 * math.sin(angle_1) + self.length_2 * math.sin(angle_1 + angle_2)
        return x, y

    def back_kinematic(self, x: float, y: float) -> tuple[float, float]:
        distance = math.sqrt(x ** 2 + y ** 2)
        max_len = self.length_1 + self.length_2
        if distance > max_len:
            raise ValueError(
                f"Can't reach destination {(x, y)} due to distance ({distance}) being bigger than length of all levers ({max_len})"
            )

        cos_angle_2 = (x ** 2 + y ** 2 - self.length_1 ** 2 - self.length_2 ** 2) / (2 * self.length_1 * self.length_2)
        cos_angle_2 = max(-1, min(1, cos_angle_2))
        self.angle_2 = math.acos(cos_angle_2)

        self.angle_1 = math.atan2(y, x) - math.atan2(
            self.length_2 * math.sin(self.angle_2), self.length_1 + self.length_2 * math.cos(self.angle_2)
        )

        return math.degrees(self.angle_1), math.degrees(self.angle_2)

    def go_to_destination(self, destination: (float, float, float)) -> None:
        tan_val = destination[1] / destination[0]
        plane_projection_rad = math.atan(tan_val)
        print("Degree of the plane", math.degrees(plane_projection_rad))

        destination_horizontal_projection = math.sqrt(destination[0] ** 2 + destination[1] ** 2)
        destination_vertical_projection = destination[2]
        print("Spot coords on the plane", destination_horizontal_projection, destination_vertical_projection)
        self.angle_1, self.angle_2 = self.back_kinematic(destination_horizontal_projection, destination_vertical_projection)

        # Compute end of lever 1
        x_coord_1 = math.cos(self.angle_1) * self.length_1
        y_coord_1 = math.sin(self.angle_1) * self.length_1
        self.lever_1_end = (x_coord_1, y_coord_1)
        print("Endpoint of the first lever on the plane", self.lever_1_end)

        # Compute end of lever 2
        x_coord_2 = math.cos(self.angle_1 + self.angle_2) * self.length_2 + x_coord_1
        y_coord_2 = math.sin(self.angle_1 + self.angle_2) * self.length_2 + y_coord_1
        self.lever_2_end = (x_coord_2, y_coord_2)
        print("Endpoint of the second lever on the plane", self.lever_2_end)

    def print_current_state(self):
        print(self.lever_1_end)
        print(self.lever_2_end)
        print(self.angle_1, self.angle_2)


manipulator_parts = [
    {
        "device_type": "rotor",
        "order": 1,
        "rotation_boundaries": None,
        "static_x": 45,
        "static_y": 50,
    },
    {
        "device_type": "lever",
        "order": 2,
        "rotation_boundaries": (0, 270),
        "length": 120,
        "static_x": 45,
        "static_y": 50,
    },
    {
        "device_type": "lever",
        "order": 3,
        "rotation_boundaries": (0, 270),
        "angle_range": (0, 160),
        "length": 135,
        "static_x": 0,
        "static_y": 0,
    },
]

destination = (50, 40, 30)  # xyz

manipulator = Manipulator(manipulator_parts)
manipulator.go_to_destination(destination)
