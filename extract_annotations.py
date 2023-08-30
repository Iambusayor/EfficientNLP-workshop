import json
import os
import argparse
from tqdm import tqdm
import logging

logger = logging.getLogger()


def find_tag(specific_token, dict_tags):
    for str_of_chars in dict_tags:
        token_set = set(specific_token.split("_"))
        chars_set = set(str_of_chars.split("_"))
        common_ele = token_set.intersection(chars_set)
        if len(common_ele) > 0:
            return dict_tags[str_of_chars]
    return "O"


def extract_from_json(file_path: str, output_dir: str) -> str:
    """

    :param output_dir:
    :type file_path: object

    """
    with open(file_path) as f:
        dict_ann = json.loads(f.read())

    per_ann_sentences = {}
    for s, dict_sent in enumerate(dict_ann["annotations"]):
        content = dict_sent["text_snippet"]["content"]
        reference = int(dict_sent["reference"])
        tokens_annot = dict_sent["annotations"]
        start_end_offset = {}
        for dict_token in tokens_annot:
            start_idx = dict_token["text_extraction"]["text_segment"]["start_offset"]
            end_idx = dict_token["text_extraction"]["text_segment"]["end_offset"]
            start_end_str = "_".join([str(i) for i in range(start_idx, end_idx)])
            start_end_offset[start_end_str] = dict_token["display_name"]

        tokens = content.split()
        beg_idx = 0
        annotated_words = []
        for tok in tokens:
            tok_start_end_str = "_".join(
                [str(i) for i in range(beg_idx, beg_idx + len(tok))]
            )
            tag = find_tag(tok_start_end_str, start_end_offset)
            annotated_words.append((tok, tag))
            beg_idx += len(tok) + 1

        per_ann_sentences[reference] = annotated_words

    output_file = os.path.join(output_dir, "train.txt")

    with open(output_file, "w") as f:
        for reference, annotations in tqdm(
            per_ann_sentences.items(),
            desc=f"Writing data into {output_file}",
            total=len(per_ann_sentences),
        ):
            for word, tag in annotations:
                f.write(f"{word} {tag}\n")
            f.write("\n")
    logger.info(f"Extraction done and written into {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract NER data from JSON annotations."
    )
    parser.add_argument("--input_path", type=str, help="Path to the input JSON file")
    parser.add_argument("--output_path", type=str, help="Path to the output txt file")

    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path

    # lang = os.path.splitext(os.path.basename(input_path))[0]
    extract_from_json(input_path, output_path)
