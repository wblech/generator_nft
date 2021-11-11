import hashlib
import json
import math
import os
import random
from pathlib import Path

from PIL import Image
from config import STRUCT


def main():

    name = 'Teste'
    description = 'Descrição teste'

    output_img = 'final_img'
    output_json = 'final_json'
    final_image = None
    layer_dict = STRUCT.get('layer_order')
    size = 100
    all_dna = []
    fail_list_nbr = []

    is_possible_to_create_all(layer_dict, size)

    os.makedirs(f'./{output_img}', exist_ok=True)
    os.makedirs(f'./{output_json}', exist_ok=True)
    for nbr in range(1, size+1):
        current_dna = []
        attributes = []
        for index, layer in enumerate(layer_dict):
            index_file, file_path = randon_choose_file(layer)
            current_dna.append(str(index_file))

            value = file_path.split('/')[-1].split('.')[0].split('#')[0]
            att_dict = {
                'trait_type': layer.get('name', ""),
                'value': value
            }
            attributes.append(att_dict)

            if index == 0:
                final_image = Image.open(f'{file_path}')
            else:
                current_image = Image.open(f'{file_path}')
                final_image.paste(current_image, (0, 0), current_image)
        dna_str = ''.join(current_dna)
        hash_dna = hashlib.md5(dna_str.encode()).hexdigest()
        if hash_dna in all_dna:
            print(f"DNA already exists! => {nbr}")
            fail_list_nbr.append(nbr)
            continue

        all_dna.append(hash_dna)
        final_image.save(f'{output_img}/{nbr}.png')

        metadata = {
            'name': name,
            'description': description,
            "image": "https://storage.googleapis.com/opensea-prod.appspot.com/puffs/3.png",
            'attributes': attributes
        }

        with open(f'{output_json}/{nbr}.json', 'w') as fd:
            json.dump(metadata, fd, ensure_ascii=False, indent=4)

        print("DNA created!")

    #Todo: Needs a retry in an infinity loop


def is_possible_to_create_all(layer_dict, size):
    combinations = []
    for layer in layer_dict:
        _, qtd_files = count_files(layer)
        combinations.append(qtd_files)
    comb = math.prod(combinations)
    if size > comb:
        print(f'Qtd of NFT: {size}. Possible combinations: {comb}. You need more elements and layers!!')
        exit(1)


def count_files(layer):
    path_name = Path(__file__).parents[0]
    img_path_name = f"layers/{layer.get('name')}"
    posix_all_files = Path(f'{path_name}/{img_path_name}').glob('**/*')
    all_files_list = [str(x) for x in posix_all_files if x.is_file()]
    qtd_files = len(all_files_list)
    return all_files_list, qtd_files


def randon_choose_file(layer):
    all_files_list, qtd_files = count_files(layer)

    rarity = []
    for path_file in all_files_list:
        perc = path_file.split('/')[-1].split('.')[0].split('#')[1]
        rarity.append(int(perc))

    path_file_list = random.choices(all_files_list, weights=rarity, k=1)
    index_file = all_files_list.index(path_file_list[0])
    file_choose = path_file_list[0]
    return index_file, file_choose


if __name__ == '__main__':
    main()
