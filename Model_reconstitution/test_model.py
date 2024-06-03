import requests
import torch
from model import JigSolver
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

def preprocess_image(image_path):
    preprocess = transforms.Compose([
        transforms.Resize((350, 350)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    img = Image.open(image_path).convert("RGB")
    img = preprocess(img).unsqueeze(0) 
    return img

def fragment_image(image_path):
    img = Image.open(image_path).convert("RGB")
    h = img.height
    w = img.width
    h = h - h % 3
    w = w - w % 3
    h_3 = h // 3
    w_3 = w // 3
    h_2 = int((2 / 3) * h)
    w_2 = int((2 / 3) * w)
    img = np.array(img)

    img_dict = {
        1: img[0: h_3, 0: w_3, :],
        2: img[0: h_3, w_3: w_2, :],
        3: img[0: h_3, w_2: w, :],
        4: img[h_3:h_2, 0: w_3, :],
        5: img[h_3:h_2, w_3: w_2, :],
        6: img[h_3:h_2, w_2: w, :],
        7: img[h_2:h, 0: w_3, :],
        8: img[h_2:h, w_3: w_2, :],
        9: img[h_2:h, w_2: w, :],
    }

    return img_dict

def preprocess_fragments(img_dict):
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((224, 224)),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    preprocessed_fragments = [preprocess(Image.fromarray(fragment)) for fragment in img_dict.values()]
    return torch.stack(preprocessed_fragments)

def reorganize_fragments(img_dict, predicted_positions):
    h_3 = list(img_dict.values())[0].shape[0]
    w_3 = list(img_dict.values())[0].shape[1]
    zeros = np.zeros((h_3 * 3, w_3 * 3, 3), dtype=np.uint8)

    for idx, position in enumerate(predicted_positions):
        row, col = divmod(position - 1, 3)
        zeros[row * h_3:(row + 1) * h_3, col * w_3:(col + 1) * w_3] = list(img_dict.values())[idx]

    return zeros

def insert_prediction(predictions, img_id):
    conn = sqlite3.connect('puzzle2.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO predict2 (image_puzzle_id, piece1_prediction, piece2_prediction, piece3_prediction, piece4_prediction, piece5_prediction,
                                 piece6_prediction, piece7_prediction, piece8_prediction, piece9_prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (img_id,) + tuple(predictions))

        conn.commit()

    except Exception as e:
        print(f"Erreur lors de l'insertion des prédictions : {e}")

    finally:
        conn.close()

def get_image_path_from_api(fragment_id):
    url = 'http://127.0.0.1:5000/hint'  
    response = requests.post(url, json={'fragment_id': fragment_id})
    
    if response.status_code == 200:
        return response.json()['image_path']
    else:
        print(f"Erreur API: {response.json().get('error')}")
        return None

checkpoint_path = "/content/drive/MyDrive/train_model/model5.pth"  # Mettre à jour le chemin si nécessaire
checkpoint = torch.load(checkpoint_path)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = JigSolver().to(device)
model.load_state_dict(checkpoint["best_model_wts"])
model.eval()

fragment_id = 1  
image_path = get_image_path_from_api(fragment_id)

if image_path:
    img = preprocess_image(image_path).to(device)

    with torch.no_grad():
        outputs = model(img)

    predicted = []
    for i, output in enumerate(outputs):
        predicted_position = output.argmax(dim=1).item()
        predicted.append(predicted_position + 1)
        print(f"Piece {i+1}: Predicted position - {predicted_position+1}")

    img_dict = fragment_image(image_path)
    preprocessed_fragments = preprocess_fragments(img_dict).to(device)
    reorganized_image = reorganize_fragments(img_dict, predicted)
    reorganized_image_pil = Image.fromarray(reorganized_image)

    plt.imshow(reorganized_image_pil)
    plt.axis('off')
    plt.show()

    image_complete_id = 1  
    insert_prediction(predicted, image_complete_id)
else:
    print("Erreur : chemin de l'image non trouvé")
