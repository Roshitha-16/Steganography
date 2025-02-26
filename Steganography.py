import cv2
import numpy as np
import argparse

# Function to encode multiple messages into an image
def encode_image(image_path, output_path):
    while True:
        secret_data = input("Enter your secret message (or type 'exit' to stop): ")  
        if secret_data.lower() == "exit":
            break  # Stop entering messages
        
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to load")

        binary_data = ''.join(format(byte, '08b') for byte in secret_data.encode('utf-8'))
        binary_data += '1111111111111110'  # End marker
        data_index = 0

        for row in image:
            for pixel in row:
                for channel in range(3):
                    if data_index < len(binary_data):
                        pixel[channel] = (pixel[channel] & 254) | int(binary_data[data_index])
                        data_index += 1
                    else:
                        break

        cv2.imwrite(output_path, image)
        print(f"✅ Message saved in {output_path}")

# Function to decode data from an image and append to a text file
def decode_image(image_path):
    image = cv2.imread(image_path)
    binary_data = ""

    for row in image:
        for pixel in row:
            for channel in range(3):
                binary_data += str(pixel[channel] & 1)
    
    # Stop at the end marker
    if "1111111111111110" in binary_data:
        binary_data = binary_data[:binary_data.index("1111111111111110")]
    
    # Convert binary to text
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = bytes([int(byte, 2) for byte in all_bytes]).decode('utf-8', errors='ignore')
    
    # Append message to the text file
    with open("decoded_message.txt", "a", encoding="utf-8") as file:
        file.write(f"{decoded_data}\n")  

    print(f"✅ Decoded Message: {decoded_data}")
    print("✅ Message appended to decoded_message.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Steganography - Hide and Retrieve Data in Images")
    parser.add_argument("mode", choices=["encode", "decode"], help="Choose encode or decode mode")
    parser.add_argument("image", help="Path to image file")
    parser.add_argument("-o", "--output", help="Output image file (required for encoding)")
    
    args = parser.parse_args()
    
    if args.mode == "encode":
        if not args.output:
            parser.error("Encoding requires --output argument.")
        encode_image(args.image, args.output)
    elif args.mode == "decode":
        decode_image(args.image)

