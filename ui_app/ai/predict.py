from pathlib import Path
import torch  # pytorch
from PIL import Image  # image manipulation (Pillow)
from torch import nn, save, load
from torch.optim import Adam
from torchvision import transforms

from DigitClassifier_API.model import mnistModel
def load_model(model_class, model_path, device):

    classifier = model_class().to(device)
    if Path(model_path).exists():
        try:
            classifier.load_state_dict(torch.load(model_path, map_location=device))
            print(f"Successfully loaded model from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print("No saved model found. Starting from scratch.")
    return classifier


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the model
classifier = load_model(mnistModel, "DigitClassifier_API/weight/modelState.pth", device)  
if classifier is None:
    print("Model loading failed. Exiting.")
    exit()
# ai_
#    |_DigitClassifier_API
#    |_predict.Py
#    |_mnistexample.png

# DigitClassifier_API_
#                     |_data/
#                     |_weight
def preprocess_image(image_path, device):
 
    img = Image.open(image_path)
    img_transform = transforms.Compose([
        transforms.Resize((28, 28)),  # Resize to MNIST image size (if needed)
        transforms.Grayscale(),        # Convert to grayscale (if needed)
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)) # Normalize the image, adjust if necessary
    ])
    img_tensor = img_transform(img).unsqueeze(0).to(device)  
    return img_tensor

def predict_digit(img_tensor):
    output = classifier(img_tensor)
    predicted_label = torch.argmax(output)
    print(f"Predicted label: {predicted_label}")
   # return predicted_label


def main(image_path):

    img_tensor = preprocess_image(image_path, device)
    predicted_label = predict_digit(img_tensor)
    print(f"Predicted digit: {predicted_label}")

if __name__ == "__main__":
 
    image_path = '/home/melo/Desktop/projects/apps/Mnist-UI/ui_app/ai/mnistexample.png'
    main(image_path)
