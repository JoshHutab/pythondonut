import math
import time
import os

# Screen dimensions
screen_width = 98
screen_height = 33

# Torus parameters
R1 = 5       # Major radius
R2 = 3    # Minor radius
K1 = 16     # Distance from viewer to torus
K2 = 25      # Scaling factor for projection
aspect_ratio = 2  # Aspect ratio adjustment

# Light direction (normalized)
light_dir = (0, 1, -1)
length = math.sqrt(sum(c**2 for c in light_dir))
lx, ly, lz = (c / length for c in light_dir)

# Luminance characters from dark to bright
lum_chars = " .,-~:;=!*#$@"

def main():
    A = 0.0  # Rotation around X-axis
    B = 0.0  # Rotation around Z-axis

    while True:
        # Initialize screen and z-buffer
        screen = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]
        z_buffer = [[0 for _ in range(screen_width)] for _ in range(screen_height)]

        cosA, sinA = math.cos(A), math.sin(A)
        cosB, sinB = math.cos(B), math.sin(B)

        # Generate torus points
        theta = 0.0
        while theta < 2 * math.pi:
            theta += 0.07
            costheta = math.cos(theta)
            sintheta = math.sin(theta)

            phi = 0.0
            while phi < 2 * math.pi:
                phi += 0.02
                cosphi = math.cos(phi)
                sinphi = math.sin(phi)

                x = (R1 + R2 * costheta) * cosphi
                y = (R1 + R2 * costheta) * sinphi
                z = R2 * sintheta

                # Normal vector components
                nx = costheta * cosphi
                ny = costheta * sinphi
                nz = sintheta

                # Apply rotations
                # X-axis rotation
                x1 = x
                y1 = y * cosA - z * sinA
                z1 = y * sinA + z * cosA

                # Z-axis rotation
                x2 = x1 * cosB - y1 * sinB
                y2 = x1 * sinB + y1 * cosB
                z2 = z1

                # Rotate normal vectors
                nx1 = nx
                ny1 = ny * cosA - nz * sinA
                nz1 = ny * sinA + nz * cosA

                nx2 = nx1 * cosB - ny1 * sinB
                ny2 = nx1 * sinB + ny1 * cosB
                nz2 = nz1

                # Project to 2D
                ooz = 1 / (z2 + K1)
                xp = int(screen_width/2 + K2 * ooz * x2 * aspect_ratio)
                yp = int(screen_height/2 + K2 * ooz * y2)

                if 0 <= xp < screen_width and 0 <= yp < screen_height:
                    # Calculate luminance
                    dot = nx2 * lx + ny2 * ly + nz2 * lz
                    if dot > 0:
                        lum = int(dot * 8)
                        lum = min(lum, len(lum_chars)-1)
                        if ooz > z_buffer[yp][xp]:
                            z_buffer[yp][xp] = ooz
                            screen[yp][xp] = lum_chars[lum]

        # Clear screen and render
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in screen:
            print(''.join(row))

        # Update angles
        A += 0.06
        B += 0.02
        time.sleep(0.001)

if __name__ == "__main__":
    main()