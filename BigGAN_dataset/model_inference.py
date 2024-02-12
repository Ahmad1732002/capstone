from transformers import BlipForConditionalGeneration
import pandas as pd
import torch
from PIL import Image

# Load the fine-tuned model
model = BlipForConditionalGeneration.from_pretrained("fine_tuned_model")

# Specify the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Load optimizer's state_dict
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
optimizer.load_state_dict(torch.load("optimizer_state.pth"))
testing_dataset=pd.read_csv('validated_test_data_csv')

# Provide an image to the model for captioning
def generate_caption(model, processor, image_path, device):
    image = Image.open(image_path).convert('RGB')
    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)

    # Generate caption
    outputs = model.generate(pixel_values=pixel_values)
    caption = processor.batch_decode(outputs, skip_special_tokens=True)

    return caption

# Example usage:
img_path = testing_dataset.iloc[3]['image']
caption = generate_caption(model, processor, img_path, device)
print("Generated Caption:", caption[0])