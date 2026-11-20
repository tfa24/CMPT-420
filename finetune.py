import argparse
import json

import torch
from datasets import Dataset, load_dataset
from peft import LoraConfig, prepare_model_for_kbit_training
from transformers import (
    AutoTokenizer,
    BitsAndBytesConfig,
    Glm4vForConditionalGeneration,
)
from trl import SFTConfig, SFTTrainer

from config import FinetuneConfig


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-file",
        default="./train.jsonl",
    )
    parser.add_argument(
        "--output-dir",
        default="./result/",
    )
    parser.add_argument(
        "--model-dir",
        default="./model/",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config = FinetuneConfig()

    tokenizer = AutoTokenizer.from_pretrained(
        "zai-org/GLM-4.6V-Flash",
        cache_dir=args.model_dir,
    )

    model = Glm4vForConditionalGeneration.from_pretrained(
        "zai-org/GLM-4.6V-Flash",
        cache_dir=args.model_dir,
        low_cpu_mem_usage=True,
        attn_implementation="flash_attention_2",
        quantization_config=BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        ),
        torch_dtype=torch.bfloat16,
    )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(model)

    def preprocess(example):
        encoded = tokenizer.apply_chat_template(
            example["messages"],
            tools=json.loads(example["tools"]),
            truncation=True,
            max_length=config.max_length,
            tokenizer_kwargs={
                "stride": config.stride,
                "return_overflowing_tokens": True,
            },
        )
        encoded.pop("token_type_ids", None)
        encoded.pop("overflow_to_sample_mapping", None)

        if isinstance(encoded["input_ids"][0], int):
            return [encoded]

        return [
            {
                "input_ids": input_ids,
                "attention_mask": attention_mask,
            }
            for input_ids, attention_mask in zip(
                encoded["input_ids"],
                encoded["attention_mask"],
            )
        ]

    raw_dataset = load_dataset("json", data_files=args.data_file, split="train")
    dataset = Dataset.from_list(
        [window for example in raw_dataset for window in preprocess(example)]
    )

    trainer = SFTTrainer(
        model=model,
        args=SFTConfig(
            output_dir=args.output_dir,
            per_device_train_batch_size=config.per_device_train_batch_size,
            num_train_epochs=3,
            learning_rate=config.learning_rate,
            lr_scheduler_type=config.lr_scheduler_type,
            optim=config.optim,
            gradient_accumulation_steps=config.gradient_accumulation_steps,
            max_grad_norm=config.max_grad_norm,
            bf16=True,
            logging_steps=1,
            save_strategy="no",
            dataloader_pin_memory=False,
            max_length=None,
        ),
        train_dataset=dataset,
        processing_class=tokenizer,
        peft_config=LoraConfig(
            task_type="CAUSAL_LM",
            r=config.lora_r,
            target_modules=list(config.lora_target_modules),
            lora_alpha=config.lora_alpha,
            lora_dropout=config.lora_dropout,
        ),
    )
    trainer.train()
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    trainer.state.save_to_json(f"{args.output_dir}/trainer_state.json")


if __name__ == "__main__":
    main()
